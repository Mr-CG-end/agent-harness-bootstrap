# Agent Harness Bootstrap

[简体中文](README.md) | English

Bootstrap a small, executable engineering harness for greenfield and existing repositories.

The project packages repository-audit tooling and an installable Skill that turns project conventions into a layered contract:

1. concise repository instructions;
2. versioned sources of truth;
3. deterministic format, lint, type, test, build, and artifact checks;
4. one local verification entry point;
5. CI using the same verification path;
6. optional local hooks;
7. explicit human approval and acceptance boundaries.

The default workflow is read-only first. It audits the target repository, proposes the smallest useful harness, and only changes files after the user has authorized implementation.

## Status

Version `0.1.0` is an early, usable foundation. It currently provides:

- a dependency-free, read-only repository auditor;
- a preview-first, non-overwriting `AGENTS.md` generator;
- a portable `bootstrap-project-harness` Skill;
- distribution manifests for Codex and Claude Code;
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

### Install the Skill

The Skill is tool-agnostic. It works in Codex, Claude Code, or any coding agent that reads `SKILL.md`.

**Codex** — ask the built-in installer to install directly from GitHub:

```text
Use $skill-installer to install the bootstrap-project-harness skill from:
https://github.com/Mr-CG-end/agent-harness-bootstrap/tree/main/skills/bootstrap-project-harness
```

To pin the installation to this release, replace `main` with `v0.1.0` in the URL. Invoke it with `$bootstrap-project-harness`.

**Claude Code** — add the marketplace and install:

```text
/plugin marketplace add Mr-CG-end/agent-harness-bootstrap
/plugin install agent-harness-bootstrap@agent-harness
```

The full command is `/agent-harness-bootstrap:bootstrap-project-harness`. The bare `/bootstrap-project-harness` also works unless another command already uses that name.

**Manual** — copy the `skills/bootstrap-project-harness` directory into your agent's skills directory (`~/.claude/skills/` for Claude Code), then restart or reload the agent.

Once installed, describe what you need:

```text
Establish a minimal engineering harness for this repository.
```

The repository ships both `.codex-plugin/plugin.json` and `.claude-plugin/marketplace.json`. They live in separate directories and do not interfere with each other.

## Development

The repository has no third-party runtime dependencies. Python 3.10 or newer is required.

```shell
python scripts/verify.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution rules, [CHANGELOG.md](CHANGELOG.md) for release history, and [docs/v0.1-plan.md](docs/v0.1-plan.md) for the initial product boundary.

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
