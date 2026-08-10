# Agent Harness Bootstrap

[简体中文](README.zh-CN.md) | English

Bootstrap a small, executable engineering harness for greenfield and existing repositories.

The project packages repository-audit tooling and an installable Codex Skill that turns project conventions into a layered contract:

1. concise repository instructions;
2. versioned sources of truth;
3. deterministic format, lint, type, test, build, and artifact checks;
4. one local verification entry point;
5. CI using the same verification path;
6. optional local hooks;
7. explicit human approval and acceptance boundaries.

The default workflow is read-only first. It audits the target repository, proposes the smallest useful harness, and only changes files after the user has authorized implementation.

## Status

Version `0.1` is an early, usable foundation. It currently provides:

- a dependency-free, read-only repository auditor;
- a preview-first, non-overwriting `AGENTS.md` generator;
- a portable `bootstrap-project-harness` Skill;
- guidance for JavaScript/TypeScript, Python, Rust, Go, JVM, .NET, Ruby, and PHP repositories;
- tests and cross-platform CI for the packaged tooling.

It does not automatically create remote repositories, change branch protection, install hooks, manage secrets, deploy software, commit, or push.

## Quick start

Audit a repository without modifying it:

```shell
python skills/bootstrap-project-harness/scripts/audit_repo.py /path/to/repository
```

Emit machine-readable output:

```shell
python skills/bootstrap-project-harness/scripts/audit_repo.py /path/to/repository --json
```

Preview a minimal repository contract without changing files:

```shell
python skills/bootstrap-project-harness/scripts/generate_harness.py /path/to/repository
```

Create a missing `AGENTS.md` after reviewing the plan:

```shell
python skills/bootstrap-project-harness/scripts/generate_harness.py /path/to/repository --apply
```

The generator never overwrites an existing file. It deliberately avoids inventing formatter, linter, test, build, CI, or hook configuration that the repository cannot support yet.

Install the Skill by copying `skills/bootstrap-project-harness` into your Codex skills directory. Restart or reload Codex so it can discover the Skill, then ask:

```text
Use $bootstrap-project-harness to establish a minimal engineering harness for this repository.
```

## Development

The repository has no third-party runtime dependencies. Python 3.10 or newer is required.

```shell
python scripts/verify.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution rules and [docs/v0.1-plan.md](docs/v0.1-plan.md) for the initial product boundary.

## Design principles

- Inspect before changing.
- Reuse native project tooling.
- Prefer executable checks over prose.
- Keep one canonical repository contract.
- Keep CI and local verification aligned.
- Treat hooks as feedback, not enforcement.
- Keep permissions and remote operations human-controlled.
- Preview generation by default and never overwrite existing project contracts.

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE).
