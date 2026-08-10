# Open-source patterns to adapt

Use these projects as design evidence, not as templates to copy wholesale. Recheck their current primary documentation when implementation depends on versions or tool-specific behavior.

## Common principles

1. Keep intent and operating policy in version control.
2. Give agents a short navigation entry point and progressively disclose deeper context.
3. Separate specification, planning, execution, and verification artifacts.
4. Encode objective constraints in tests, static checks, schemas, and CI.
5. Keep tools and permissions least-privileged.
6. Preserve durable task state and evidence outside chat history.
7. Distinguish local feedback, remote merge gates, and human approval.
8. Support multiple agents through a canonical repository contract rather than duplicated rule sets.

## Sources and what to borrow

### OpenAI Codex: AGENTS.md

Source: https://learn.chatgpt.com/docs/agent-configuration/agents-md

- Borrow hierarchical instruction discovery and nearest-directory overrides.
- Keep root instructions compact because instruction size is bounded and competes with task context.
- Put exact executable commands in repository guidance only after those commands exist.

### AGENTS.md open format

Source: https://agents.md/

- Borrow a tool-neutral root contract covering setup, testing, style, security, and contribution workflow.
- Use nested instructions for materially different subprojects.
- Do not mistake Markdown guidance for mechanical enforcement.

### OpenAI Harness Engineering

Source: https://openai.com/index/harness-engineering/

- Borrow repository knowledge as the system of record, progressive disclosure, structural tests, custom remediation messages, and agent-legible observability.
- Promote recurring review feedback from prose into executable tooling.
- Avoid a giant instruction manual.

### GitHub Spec Kit

Sources:

- https://github.com/github/spec-kit
- https://github.github.com/spec-kit/

- Borrow the explicit `spec -> plan -> tasks -> implement` flow for changes complex enough to need durable artifacts.
- Keep the integration portable across coding agents.
- Do not force heavyweight specification ceremony onto tiny changes.

### OpenAI Symphony

Source: https://github.com/openai/symphony/blob/main/SPEC.md

- Borrow repository-owned workflow policy, isolated workspaces, durable task state, and explicit runtime configuration for long-running automation.
- Treat orchestration as an optional advanced layer, not a greenfield prerequisite.

### GitHub Awesome Copilot

Sources:

- https://github.com/github/awesome-copilot
- https://github.com/github/awesome-copilot/blob/main/AGENTS.md

- Borrow clear metadata contracts, least-privilege tool selection, representative-task validation, and explicit hook specifications.
- Inspect third-party skills and hooks before installation; natural-language packages are part of the supply chain.

## Canonical artifact strategy

Prefer this order:

1. `AGENTS.md` — short repository map and working contract.
2. Existing product, architecture, decision, and runbook documents — source of truth.
3. Native verification commands — executable contract.
4. CI configuration — remote enforcement.
5. Optional tool-specific adapters — short pointers or genuinely tool-specific behavior only.
6. Optional skills — reusable procedures loaded on demand.
7. Optional orchestration workflow — only when background or multi-task autonomy is required.

Never generate every possible artifact simply because an example project contains it.
