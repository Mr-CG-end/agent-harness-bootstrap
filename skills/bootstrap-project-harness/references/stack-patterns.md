# Stack and enforcement patterns

Select only the detected ecosystem. Verify current commands and supported versions against primary documentation before editing the repository.

## Verification contract

Compose a single verification entry point from applicable stages:

```text
dependency integrity -> format check -> lint -> type/static check
-> unit/integration tests -> production build -> artifact assertions
```

Order stages by dependency, not by a universal template. For example, a generated-manifest assertion must run after the production build even if ordinary unit tests run earlier.

## Ecosystem defaults

| Ecosystem | Prefer existing native surfaces | Common verification components |
|---|---|---|
| JavaScript / TypeScript | `package.json` scripts and the detected lockfile | format check, ESLint/Biome, `tsc --noEmit`, test runner, production build |
| Python | `pyproject.toml`, locked environment, existing task runner | Ruff format/check, type checker when adopted, pytest, package build |
| Rust | Cargo workspace configuration | `cargo fmt --check`, Clippy with project policy, tests, build |
| Go | Go modules and repository scripts/Makefile | formatting check, `go vet`, tests, build |
| JVM | checked-in Maven/Gradle wrapper | formatting/lint plugin, tests, package/build |
| .NET | solution/project files and pinned SDK | format check when configured, analyzers, tests, build/publish |

Do not add all listed tools automatically. In brownfield repositories, reuse what exists. In greenfield repositories, choose a minimal coherent set before implementation grows.

## CI provider routing

| Evidence | Configuration target |
|---|---|
| GitHub remote or explicit GitHub request | `.github/workflows/` |
| GitLab remote or explicit GitLab request | `.gitlab-ci.yml` |
| Azure DevOps request | `azure-pipelines.yml` |
| Existing CI provider | Extend the existing provider |
| No provider selected | Create local verification only and report CI as pending |

Apply least privilege, dependency caching supported by the package manager, explicit timeouts, and concurrency cancellation where useful. Treat third-party actions as dependencies; select current supported versions from official sources and follow the repository's pinning policy.

## Instruction adapters

- Keep `AGENTS.md` canonical when supported by the intended tools.
- Create `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, or editor rules only when the user names those tools or the repository already uses them.
- Put tool-specific permissions, hooks, or commands in the adapter.
- Do not duplicate general architecture and testing rules across adapters. Link to or instruct the tool to read the canonical source when reliable.

## Hooks

Add hooks only after the underlying commands pass independently.

- Pre-commit: formatting or very fast deterministic checks.
- Pre-push: moderately expensive checks only when team latency accepts them.
- Commit message: only when the repository has an explicit convention.
- Never put the only security, test, or release gate in a local hook.
- Prefer a cross-platform hook manager only when the project already has the relevant runtime; otherwise document native setup or defer.

## Manual and external gates

Always report these separately because repository files cannot prove them:

- required status checks / branch rules;
- environment secrets and deployment approvals;
- protected environments and release permissions;
- browser, mobile device, hardware, accessibility, or visual QA;
- third-party service configuration;
- legal, policy, or product judgment.

## Greenfield minimum

For a small new project, a sufficient first harness is often:

```text
AGENTS.md
locked dependencies / pinned runtime
formatter + static check + one discovered smoke test
one verify command
one CI workflow
manual acceptance section in the active plan or README
```

Add architecture maps, ADRs, nested instructions, hooks, eval harnesses, observability, or autonomous orchestration only when project risk or complexity justifies them.
