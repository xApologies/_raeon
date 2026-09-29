from dataclasses import dataclass, field

@dataclass(frozen=True)
class GeneratorRef:
    card_id: str
    x: float = 0.0
    y: float = 0.0
    theta_deg: float = 0.0

@dataclass
class Sandbox:
    sandbox_id: str
    permanent: bool = True
    generators: list[GeneratorRef] = field(default_factory=list)
    committed: bool = False
    manifested_manifold_id: str | None = None

    def add_generator(self, generator: GeneratorRef):
        if self.manifested_manifold_id is not None:
            raise ValueError("cannot add directly to already manifested sandbox in this core model")
        self.generators.append(generator)
        self.committed = True

    def remove_generator(self, card_id: str):
        raise ValueError(
            "Field Generators cannot be independently extracted after commitment; "
            "merge whole sandbox domains instead."
        )

def merge_sandboxes(new_id: str, *sandboxes: Sandbox) -> Sandbox:
    """Combine committed Generator populations.

    This DOES NOT prove a valid manifold. The future topology solver must validate
    the union of Generator identities + poses/configuration.
    """
    merged = Sandbox(
        sandbox_id=new_id,
        permanent=any(s.permanent for s in sandboxes),
        generators=[g for s in sandboxes for g in s.generators],
        committed=True,
    )
    return merged
