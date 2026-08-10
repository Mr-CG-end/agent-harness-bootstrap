# Contributing

Contributions should make repository harnesses smaller, more deterministic, or easier to adopt across stacks.

## Before opening a change

1. Open an issue for new ecosystems, write behavior, external integrations, or changes to permission boundaries.
2. Keep fixes and documentation improvements narrowly scoped.
3. Do not include secrets, private repository content, generated audit reports, or identifying local paths in fixtures.

## Development workflow

1. Make the change.
2. Add or update a deterministic test.
3. Run `python scripts/verify.py`.
4. Review the diff for unintended generated files and permission expansion.

Pull requests should state the supported use case, verification commands, compatibility impact, and any manual acceptance still required.
