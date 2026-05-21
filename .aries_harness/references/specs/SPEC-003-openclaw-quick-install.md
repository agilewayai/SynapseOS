# Spec Package

## Document Control

- Spec ID: `SPEC-003`
- Artifact type: `spec`
- Objective mode: `functional_capability`
- Title: `OpenClaw one-link quick learning-and-installation`
- Status: `active`
- Owner: `Arthur`
- Parent request: `REQ-003`
- Child refs: `STORY-003`, `ARCH-003`, `ADR-0005`, `TRACE-001`
- Last reviewed: `2026-05-21`
- Source of truth: `this file`

## External Interface Evidence

This spec is grounded in the current OpenClaw public documentation:

- OpenClaw install and local verification: `https://docs.openclaw.ai/install`
- OpenClaw skills concept, skill roots, precedence, allowlists, and `SKILL.md` loading behavior: `https://docs.openclaw.ai/tools/skills`
- OpenClaw skills CLI commands: `https://docs.openclaw.ai/cli/skills`
- OpenClaw skills configuration surface: `https://docs.openclaw.ai/tools/skills-config`
- OpenClaw skill creation and install modes: `https://openclawdoc.com/docs/skills/creating-skills`

## Belongs Here

- Objective: define what must be true for SynapseOS to provide a smooth OpenClaw installation and learning path that feels native to OpenClaw's skill system
- In scope:
  - OpenClaw-specific installation guide
  - current safe baseline using `synapse-cli install --agent openclaw`
  - paste-link chatbox installation prompt for OpenClaw
  - optional future shell one-link quick install UX
  - OpenClaw skill-root and skill-interface compatibility expectations
  - OpenClaw-native verification using `openclaw skills list` and `openclaw skills check`
  - first-use learning prompt and entrypoint guidance after installation
  - safety policy for remote one-link installers
- Out of scope:
  - publishing to ClawHub during this spec pass
  - changing canonical SynapseOS layer content
  - guaranteeing OpenClaw behavior without running OpenClaw-native checks
  - implementing a destructive overwrite or uninstall path
  - installing OpenClaw automatically without explicit approval
- Primary actors:
  - OpenClaw user installing SynapseOS as local skills
  - maintainer validating SynapseOS OpenClaw compatibility
  - support operator helping an OpenClaw user diagnose install drift
  - future release operator publishing a one-link installer or registry package

## OpenClaw Interface Assumptions

- A skill is a directory with a `SKILL.md` file containing YAML frontmatter and Markdown instructions.
- OpenClaw can load skills from several roots, including workspace-level, agent-scoped, shared managed, bundled, and configured extra directories.
- OpenClaw checks skill state through `openclaw skills list`, `openclaw skills info`, and `openclaw skills check`.
- OpenClaw supports CLI-based skill installation from known sources, local paths, GitHub repositories, or managed sources depending on package shape.
- OpenClaw's current skill metadata reference documents `name` as a required unique identifier using snake_case; any OpenClaw-specific package or overlay must pass `openclaw skills check --json` rather than assuming SynapseOS source names are sufficient.
- SynapseOS is a multi-skill stack, so the OpenClaw install target should behave like a managed group containing `xuan-master`, `archon`, `prism`, and `init`, not like a single flat skill.

## Required User Flows

### Flow 1: Safe Baseline Install From A Local Checkout

```sh
./synapse-cli doctor --json
./synapse-cli install --agent openclaw --dry-run --json
./synapse-cli install --agent openclaw --yes --json
./synapse-cli verify --agent openclaw --json
openclaw skills check --json
```

Required behavior:

- dry-run renders writes before applying them
- approved install writes into the OpenClaw adapter target, defaulting to the managed shared skill root
- `synapse-cli verify` checks SynapseOS files and manifest
- `openclaw skills check --json` confirms OpenClaw's native view

### Flow 2: Chatbox Paste-Link Quick Install

Target UX:

```text
Install the SynapseOS skills family for OpenClaw from this installation prompt:
https://raw.githubusercontent.com/agilewayai/SynapseOS/main/install/openclaw-chat-install.md

Follow the prompt exactly. Show me the target directory and dry-run plan first, then complete the install and verification if the plan is safe.
```

Required behavior:

- show the resolved OpenClaw skill target before writing
- clone or update SynapseOS from GitHub over HTTPS
- run `synapse-cli doctor --json`
- run `synapse-cli install --agent openclaw --dry-run --json`
- install or update SynapseOS under an OpenClaw-compatible group directory only after the plan is safe
- run `synapse-cli verify --agent openclaw`
- run `openclaw skills check --json` when `openclaw` is available
- print a first-use learning prompt after successful verification

### Flow 3: Optional Shell One-Link Installer

Target future UX:

```sh
curl -fsSL https://raw.githubusercontent.com/agilewayai/SynapseOS/main/install/openclaw.sh | bash
```

Required behavior for a future shell implementation:

- support `--dry-run`
- support `--target <path>` for custom OpenClaw skill roots
- refuse to overwrite an existing non-SynapseOS target unless `--force` is explicitly passed
- delegate installation and verification to `synapse-cli`
- print the same first-use learning prompt as the chatbox mode

### Flow 4: Quick Learning After Install

After verification, the guide should instruct the user to ask OpenClaw:

```text
Load SynapseOS. Explain when I should use Xuan Master, Archon, Prism, and Init, then recommend the first skill for my current task.
```

Expected learning output:

- Xuan Master is the 27-model cognition core
- Archon is the enabler layer for calibration, orchestration, actions, and generation
- Prism is the specialist routing layer
- Init owns setup, installation, and verification

## Acceptance Conditions

- `docs/OPENCLAW_INSTALL.md` exists and includes prerequisites, safe install, one-link target UX, verification, troubleshooting, and update guidance.
- `install/openclaw-chat-install.md` exists and provides the paste-link chatbox install prompt.
- The guide references OpenClaw-native commands instead of relying only on SynapseOS self-verification.
- The spec defines the chatbox installer behavior and shell one-link safety contract before further automation.
- The OpenClaw install target is described as a multi-skill group, not a single opaque file copy.
- Any future shell one-link script supports dry-run and explicit target override.
- OpenClaw verification includes `openclaw skills check --json` where available.
- OpenClaw metadata compatibility is verified through OpenClaw itself; if the current source frontmatter does not satisfy the active OpenClaw interface, a future package overlay must provide OpenClaw-compatible aliases without renaming the canonical SynapseOS layers.
- Installation failures must produce actionable diagnostics for missing OpenClaw, missing Git, target permission failure, existing target conflict, and skill validation failure.
- The existing `synapse-cli install --agent openclaw` baseline remains valid.
- The first-use learning prompt is included so users can immediately learn the layered skill system inside OpenClaw.

## NFRs

- Installation path should be copy-pasteable and understandable in under one minute.
- One-link mode must be safe enough for public docs and support contexts.
- Operators must be able to inspect the local-install path without running remote shell.
- Verification must distinguish SynapseOS payload integrity from OpenClaw skill visibility.
- The approach must not require network access when installing from an already-cloned local checkout.

## Regression Guardrails

- Do not make OpenClaw the only supported host.
- Do not silently mutate OpenClaw allowlists or config files.
- Do not replace the repo-local `synapse-cli` contract with a remote-only installer.
- Do not publish a one-link command that bypasses dry-run, target display, and conflict checks.
- Do not rename canonical SynapseOS layers just to satisfy one host adapter.

## Slice Candidates

| Slice ID | User value | Acceptance anchor | Priority | Notes |
| --- | --- | --- | --- | --- |
| `STORY-003A` | OpenClaw users get a detailed guide and governed quick-install spec | `REQ-003`, `SPEC-003`, `STORY-003`, `ARCH-003`, `ADR-0005`, and guide exist | `now` | This pass |
| `STORY-003B` | OpenClaw users get a paste-link chatbox installer | `install/openclaw-chat-install.md` provides a simple prompt and executable install workflow for OpenClaw chat | `now` | This pass |
| `STORY-003C` | OpenClaw users get deeper native verification | `synapse-cli verify --agent openclaw` can optionally run or summarize OpenClaw-native checks | `next` | Requires coding slice |
| `STORY-003D` | OpenClaw users get native package installation | SynapseOS package shape works with OpenClaw's native `skills install` source formats | `later` | May require an OpenClaw-specific package surface |
| `STORY-003E` | Maintainers get metadata compatibility confidence | CI or local checklist runs SynapseOS verification plus OpenClaw skill check where OpenClaw is installed | `later` | Includes `SKILL.md` metadata compatibility |
| `STORY-003F` | OpenClaw users get shell one-link install | `install/openclaw.sh` supports dry-run, target override, safety checks, install, verify, and learning prompt | `later` | Optional after chatbox mode is proven |

## Linked Artifacts

- Request brief: `.aries_harness/references/requests/REQ-003-openclaw-quick-install.md`
- Story-slice pack: `.aries_harness/references/stories/STORY-003-openclaw-quick-install.md`
- Architecture design pack: `.aries_harness/decisions/architecture/ARCH-003-openclaw-quick-install.md`
- ADR: `.aries_harness/decisions/adrs/ADR-0005-openclaw-quick-install.md`
- User guide: `docs/OPENCLAW_INSTALL.md`
- Chatbox install prompt: `install/openclaw-chat-install.md`
- Traceability matrix: `.aries_harness/references/VALUE-TRACEABILITY-MATRIX.md`

## Open Questions And Risks

- Open question: should the future one-link script live under `install/openclaw.sh`, `scripts/install-openclaw.sh`, or a release artifact path?
- Open question: should SynapseOS add an OpenClaw-specific package surface with OpenClaw-safe metadata aliases for native Git install, or keep the multi-skill group layout as the primary path?
- Risk: OpenClaw skill roots or CLI behavior can change, so the guide must link to current OpenClaw docs and stay refreshable.
- Risk: remote one-link scripts can reduce friction but increase trust concerns; the guide must always include a local inspectable path.
- Refresh trigger: any OpenClaw interface change, SynapseOS OpenClaw adapter change, or hosted one-link implementation.
- Audit log entry: `AUDIT-001`
