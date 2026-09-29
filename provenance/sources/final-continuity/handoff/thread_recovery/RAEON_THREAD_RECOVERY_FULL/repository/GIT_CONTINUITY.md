# Git Continuity

Canonical repository: https://github.com/xApologies/\_raeon
Canonical/default branch: main.

The repository was normalized so default access returns current project
state rather than obsolete bootstrap branches. Current architecture is
DESIGN -\> DATA -\> GAME -\> TESTS, with
mathematics/development/provenance as separate authority layers.

Normal future workflow: main -\> temporary working branch if needed -\>
validate -\> merge into main -\> delete temporary branch.

Do not accumulate permanent checkpoint branches.

New-thread recovery: 1. ingest this ZIP; 2. crawl GitHub default `main`;
3. confirm schema/current state; 4. reconcile package with Git; 5.
explicitly resolve conflicts rather than guessing; 6. resume from
foundational backlog.
