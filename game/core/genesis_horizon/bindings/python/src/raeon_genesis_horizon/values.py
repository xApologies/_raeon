"""Typed local value-binding ABI for the pinned Section-14 interpreter.

Only declared INT CONST leaves are rebound. Source/CFG/opcodes/exports stay fixed;
the instantiated program is encoded, decoded and verified before every run.
This is an application binding, not additional Genesis syntax.
"""
import copy
from dataclasses import replace
import sys

from .toolchain import digest


class IntegerInterpreter:
    def __init__(self, upstream, directory):
        path = upstream / 'language/14 Control Flow & Data Algebra/12_REFERENCE_IMPLEMENTATION'
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))
        from genesis_control import parse_source, Compiler, encode, decode, verify, VM
        self.encode, self.decode, self.verify, self.vm = encode, decode, verify, VM
        self.programs = {}
        self.receipts = []
        for name in ['equal', 'at_most', 'add']:
            source = directory / (name + '.gen')
            compiler = Compiler(parse_source(source.read_text(encoding='utf8'), file='bindings/values/' + source.name))
            program = compiler.compile()
            self.verify(program)
            slots = {key: compiler.top[key][0] for key in ['left', 'right']}
            self.programs[name] = (program, slots)

    def run(self, operation, left, right):
        if any(type(v) is not int or abs(v) > 2**53 for v in [left, right]):
            raise ValueError('ADMISSION_REJECTED')
        return self.run_integer(operation, left, right)

    def run_integer(self, operation, left, right):
        """Native INT values; wire/frame resource bounds are a separate ABI.

        The pinned VM supports arbitrary precision INT. This entry does not
        silently convert through floating point or impose a domain magnitude.
        """
        if any(type(v) is not int for v in [left, right]):
            raise ValueError('ADMISSION_REJECTED')
        template, slots = self.programs[operation]
        program = copy.deepcopy(template)
        replacements = {slots['left']: left, slots['right']: right}
        for i, instruction in enumerate(program.instructions):
            if instruction.out in replacements:
                if instruction.op.name != 'CONST' or instruction.result_type.value != 'INT':
                    raise ValueError('VALUE_ABI_INTEGRITY')
                program.instructions[i] = replace(instruction, attrs={'value': replacements[instruction.out]})
        program = self.decode(self.encode(program))
        self.verify(program)
        result = self.vm().run(program, max_steps=64)
        value = next(iter(result.exports.values())).value
        self.receipts.append({'operation': operation, 'inputs_commitment': digest([left, right]),
                              'receipt': result.receipt, 'value': value})
        return value
