---
name: bootstrap-project-harness
description: Bootstrap or retrofit a portable AI-ready engineering harness for software repositories. Use when starting a project, creating repository AI conventions, setting up AGENTS.md and source-of-truth docs, defining format/lint/typecheck/test/build/verify commands, adding CI and optional local hooks, establishing permission and manual-acceptance boundaries, or converting prose rules into executable checks. Support greenfield and existing repositories across languages and CI providers by inspecting the stack and consulting current primary documentation before choosing tools or versions.
---

# Bootstrap Project Harness

Create the smallest repository-owned control system that lets humans and coding agents understand, change, and verify a project reliably.

## Start with a read-only audit

1. Run `python scripts/audit_repo.py <repo>` from this Skill directory.
2. Inspect repository instructions, product/design documents, package manifests, lockfiles, test configuration, CI, hooks, and current git status.
3. Classify the repository as:
   - **Greenfield**: no meaningful implementation or established toolchain.
   - **Brownfield**: existing code, conventions, history, or user changes must be preserved.
4. Identify material unknowns only: intended stack, supported platforms, repository host, deployment target, and mandatory compliance rules. Infer everything else from repository evidence.
5. Read [open-source-patterns.md](references/open-source-patterns.md) before choosing the artifact layout. Read [stack-patterns.md](references/stack-patterns.md) only for the detected ecosystem and CI provider.
6. After the user approves creating a minimal root contract, preview `python scripts/generate_harness.py <repo>`. Use `--apply` only with explicit write authority. The generator creates a missing `AGENTS.md` and never overwrites existing files; build all other artifacts from verified project evidence.

## Design the harness in layers

Build only the layers the project can use now:

1. **Navigation** — Keep root `AGENTS.md` short. Record exact commands, repository map, invariants, safety boundaries, and links to deeper sources of truth. Add nested instruction files only where rules genuinely differ.
2. **Knowledge** — Store architecture, product intent, decisions, active plans, quality debt, and manual runbooks in versioned repository files. Do not copy volatile chat context into permanent rules without validation.
3. **Executable checks** — Encode objective rules as formatter checks, linters, type checks, tests, schema checks, structural assertions, build checks, or focused scripts. Prefer deterministic checks over prose and LLM judges.
4. **Single verification entry point** — Provide one documented command such as `npm run verify`, `make verify`, `just verify`, or a repository script. Compose existing native commands rather than introducing a task runner without need.
5. **CI** — Run the same verification path in a clean environment with locked dependencies, least token permissions, explicit timeouts, and correct artifact ordering.
6. **Local feedback** — Add hooks only when they materially shorten feedback. Keep them fast and deterministic; never treat hooks as the security or merge boundary.
7. **Governance** — Separate automated gates, manual acceptance, and external repository settings. Require explicit authority for secrets, deployment, branch protection, destructive actions, commits, and pushes.

## Produce a proposal before broad changes

Show a compact table containing:

- current evidence;
- gap or risk;
- proposed artifact or check;
- enforcement location;
- verification evidence;
- human-only follow-up.

Proceed directly when the user already authorized implementation and choices follow unambiguously from the repository. Pause when a language, CI provider, deployment target, compliance policy, or destructive migration would materially change the result.

## Implement greenfield projects

1. Establish package/dependency locking and supported runtime versions first.
2. Configure formatting, linting, typing, and baseline tests before code volume grows. Choose ecosystem-native tools from current primary documentation.
3. Create a small smoke test that proves the test runner is actually discovered.
4. Add the verification command and run it locally.
5. Add CI for the actual repository host. Do not add GitHub Actions to a GitLab-only project or vice versa.
6. Add a minimal `AGENTS.md` after commands are real, not aspirational.
7. Add only documentation required by current project complexity. Avoid empty architecture, security, or runbook theater.
8. Add vendor-specific AI instruction adapters only for tools the user intends to use. Keep one canonical source and avoid duplicated rules.

## Retrofit existing projects

1. Preserve user changes and existing conventions.
2. Reuse working commands and configurations before adding dependencies.
3. Avoid repository-wide formatting or lint churn. If unavoidable, isolate mechanical changes from behavioral changes.
4. Convert known failure modes and acceptance criteria into focused checks first.
5. Introduce CI incrementally. Do not enable a blocking gate that is already red without documenting and approving the migration path.
6. Update existing progress and handoff sources instead of creating parallel status documents.

## Apply non-negotiable integrity rules

- Keep evaluators, test expectations, merge policy, and approval rules outside agent-editable optimization surfaces when building autonomous loops.
- Make skipped checks visible with a reason and a command to enable them. If a check needs a generated artifact, rerun it after the build; never let clean CI skip it permanently.
- Do not claim CI is a merge gate until the remote workflow passes and branch protection or rulesets require it.
- Do not claim hooks are enforced; users can bypass them.
- Do not weaken tests, permissions, rubrics, or production safety to obtain a green run.
- Keep CI permissions read-only unless a job demonstrably needs more.
- Never place credentials in repository instructions, fixtures, workflow YAML, logs, or generated reports.
- Use current official documentation for action versions, language runtimes, and tool configuration. Do not copy stale version numbers from this Skill.

## Verify the harness

1. Run every new local check and the single verification command.
2. Prove important new gates can fail using a disposable fixture or a reversible temporary mutation; restore it before completion.
3. Validate a clean install/build path when practical.
4. Review the full diff for unrelated changes, generated artifacts, secrets, over-broad permissions, silent skips, and duplicated documentation.
5. Push only when authorized, then inspect the remote CI result and warnings.
6. Report separately:
   - automated checks completed;
   - skipped or environment-blocked checks;
   - external repository settings still required;
   - manual product acceptance the user must perform.

## Keep the harness healthy

When a recurring agent or human failure appears, prefer this order:

1. fix or add a deterministic check;
2. improve a tool or error message with remediation guidance;
3. update the relevant source-of-truth document;
4. add a concise instruction only when the rule cannot be encoded;
5. remove stale or duplicate guidance.

Treat the harness as product code: version it, review it, test it, and keep its feedback fast.
