# Repository Guidelines

## Purpose

This repository maintains a portable Skill and dependency-free audit tooling for bootstrapping engineering harnesses in other repositories.

## Structure

- `skills/bootstrap-project-harness/` is the distributable Skill. Keep it self-contained and free of repository-level README, changelog, or contribution files.
- `.codex-plugin/plugin.json` packages the repository as a Codex Plugin and points to the distributable Skill.
- `scripts/verify.py` is the single local verification entry point.
- `tests/` contains deterministic tests for the packaged audit script, Skill, and Plugin structure.
- `docs/v0.1-plan.md` records the current product boundary and acceptance criteria.

## Commands

- `python scripts/verify.py` runs the complete local verification suite.
- `python -m unittest discover -s tests -v` runs unit tests directly.
- `python skills/bootstrap-project-harness/scripts/audit_repo.py <repo>` performs a read-only audit.
- `python skills/bootstrap-project-harness/scripts/generate_harness.py <repo>` previews the minimal generated contract; add `--apply` to create missing files without overwriting.

## Change Rules

- Keep Python compatible with 3.10 and newer and use only the standard library unless a dependency is explicitly justified.
- Keep the auditor read-only. It must not modify the inspected repository, invoke package managers, inspect credentials, or contact remote services.
- Keep generation preview-only by default. Apply mode may create missing documented artifacts but must never overwrite or delete existing files.
- Keep `SKILL.md` concise and route detailed ecosystem guidance through `references/`.
- Add or update tests for behavior changes.
- Do not add automatic commit, push, deployment, secret management, hook installation, or repository-settings mutation.

## Style

Use four-space indentation in Python, type hints for public helpers, and descriptive snake_case names. Prefer small pure functions and stable JSON output fields.

## Pull Requests

Explain the failure mode or use case, describe the smallest change, and list verification evidence. Call out any new filesystem, subprocess, network, or permission behavior explicitly.
