# Request Brief

## Document Control

- Request ID: `REQ-003`
- Artifact type: `request`
- Objective mode: `functional_capability`
- Title: `OpenClaw one-link quick learning-and-installation for SynapseOS`
- Status: `active`
- Owner: `Arthur`
- Review date: `2026-05-21`
- Parent refs: `REQ-002`, `SPEC-002`, `ARCH-002`
- Child refs: `SPEC-003`, `STORY-003`, `ARCH-003`, `ADR-0005`, `TRACE-001`
- Source of truth: `this file`

## Belongs Here

- Request source: operator request to optimize SynapseOS installation for OpenClaw using the OpenClaw skill interface spec and a smooth one-click or one-link quick learning-and-installation path
- Problem statement: the baseline `synapse-cli` can install into an OpenClaw target, but the OpenClaw-specific user experience needs a chatbox-friendly paste-link mode aligned with OpenClaw skill roots, CLI checks, and first-use learning workflow
- Intended user outcome: an OpenClaw user can paste one prompt with one link into the OpenClaw channel chatbox, let OpenClaw complete the SynapseOS skill-family installation, verify OpenClaw can see the installed skills, and immediately learn how to use `Xuan Master`, `Archon`, `Prism`, and `Init`
- Business value:
  - reduces OpenClaw onboarding friction
  - makes SynapseOS feel native to OpenClaw rather than manually copied
  - creates a shareable chatbox install link for docs, releases, and support
  - gives future ClawHub or GitHub distribution work a clear acceptance contract
- Interface references:
  - OpenClaw skill folders are `SKILL.md` directories with YAML frontmatter and instructions
  - OpenClaw loads skills from workspace, project-agent, personal-agent, shared managed, bundled, and extra skill roots with explicit precedence
  - OpenClaw CLI exposes `openclaw skills install`, `list`, `info`, and `check`
  - OpenClaw install verification includes `openclaw --version`, `openclaw doctor`, and gateway status
- Success signals:
  - a detailed OpenClaw installation guide exists in public docs
  - the target chatbox paste-link install UX is specified with safety constraints and verification expectations
  - the chatbox install prompt exists as `install/openclaw-chat-install.md`
  - the current `synapse-cli install --agent openclaw` path is documented as the safe baseline
  - OpenClaw-native verification commands are part of acceptance
  - follow-on implementation slices can add a hosted one-link script and deeper OpenClaw adapter verification
- Target quality attributes: `low-friction`, `safe-by-default`, `OpenClaw-native`, `auditable`, `reversible`, `agent-readable`
- Scope boundary: define and add the OpenClaw chatbox prompt mode and guide now; implement hosted shell one-link automation as a separate optional slice after review
- Constraints:
  - do not silently overwrite an existing OpenClaw skill folder
  - do not install OpenClaw itself without explicit operator approval
  - preserve the existing SynapseOS layer names and skill content
  - keep the existing `synapse-cli` local install contract valid
  - do not depend on ClawHub publication before the local path is usable
- Non-goals:
  - publishing SynapseOS to ClawHub in this spec pass
  - replacing OpenClaw's native skill visibility and allowlist controls
- making remote `curl | bash` mandatory for users who prefer local review or chatbox-guided install
  - adding destructive uninstall behavior without a separate approved slice

## Keep Out

- Low-level shell implementation details for a future shell one-link installer script
- Claims that OpenClaw has loaded a skill unless `openclaw skills check` or equivalent evidence supports it
- Host-specific behavior for non-OpenClaw adapters

## Delivery Links

- Spec package: `.aries_harness/references/specs/SPEC-003-openclaw-quick-install.md`
- Story-slice pack: `.aries_harness/references/stories/STORY-003-openclaw-quick-install.md`
- Architecture design pack: `.aries_harness/decisions/architecture/ARCH-003-openclaw-quick-install.md`
- ADR: `.aries_harness/decisions/adrs/ADR-0005-openclaw-quick-install.md`
- Installation guide: `docs/OPENCLAW_INSTALL.md`
- Chatbox install prompt: `install/openclaw-chat-install.md`
- Value traceability matrix: `.aries_harness/references/VALUE-TRACEABILITY-MATRIX.md`

## Refresh Triggers

- OpenClaw changes skill folder format, skill roots, CLI command names, or verification behavior
- SynapseOS changes OpenClaw adapter paths, payload layout, or install manifest behavior
- A hosted one-link installer is implemented
- SynapseOS is published to ClawHub or another OpenClaw-native registry
- Audit log entry: `AUDIT-001`
