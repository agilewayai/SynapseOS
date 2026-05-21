# Architecture Design Pack

## Document Control

- Architecture ID: `ARCH-004`
- Artifact type: `architecture`
- Title: `Hermes direct-SKILL chatbox installation architecture`
- Status: `active`
- Owner: `Arthur`
- Related request: `REQ-004`
- Related spec: `SPEC-004`
- Child refs: `ADR-0006`
- Last reviewed: `2026-05-21`
- Source of truth: `this file`

## Design Drivers

- Primary outcome: make SynapseOS installable and learnable inside Hermes from a direct installer-skill link pasted into chat
- Quality attributes:
  - Hermes-native
  - safe by default
  - low-friction
  - auditable
  - readable as Markdown
  - no SSH key dependency
- Constraints:
  - existing `synapse-cli` install behavior remains the stable local baseline
  - Hermes configuration is not silently mutated
  - direct-link installer skill delegates writes to `synapse-cli` dry-run and approved install
  - SynapseOS remains a grouped skills family, not a single flattened instruction file

## Current And Target Shape

- Current state:
  - `synapse-cli` has a `hermes` adapter that resolves a default target under `~/.hermes/skills`
  - `install --agent hermes` can copy the SynapseOS payload into a Hermes skills target group
  - Hermes v0.14.0 in this environment supports `hermes skills install <identifier-or-http-url-to-SKILL.md>`
  - public docs do not yet have a dedicated Hermes install guide
- Target state:
  - `install/hermes-chat-install/SKILL.md` is a direct-link Hermes installer skill
  - public docs expose a copy-paste Hermes channel prompt
  - local baseline install remains `./synapse-cli install --agent hermes --dry-run` followed by `--yes`
  - Hermes-native verification is part of the acceptance path through `hermes skills list` and `hermes skills check`
  - future packaging can add a Hermes registry/native source install without breaking the direct-link baseline

## Hermes Interface Mapping

| Hermes concept | SynapseOS mapping | Design note |
| --- | --- | --- |
| Direct URL to `SKILL.md` | `install/hermes-chat-install/SKILL.md` raw GitHub URL | Native bootstrap path |
| Skill frontmatter | `name`, `description`, `version`, `platforms`, `metadata.hermes` | Installer skill is Hermes-compatible |
| Skills root | `~/.hermes/skills` by default | Adapter target can be overridden |
| Grouped skill family | `~/.hermes/skills/synapseos/<layer>/SKILL.md` | Keeps SynapseOS layers together |
| `hermes skills list` | Host-native visibility check | Confirms whether Hermes can see installed skills |
| `hermes skills check` | Host-native update/health check | Complements SynapseOS payload verification |

## Proposed Installation Modes

| Mode | User command shape | Status | Tradeoff |
| --- | --- | --- | --- |
| Hermes chatbox installer skill | Paste raw `install/hermes-chat-install/SKILL.md` URL and prompt into Hermes | available baseline | Native to Hermes; depends on Hermes tool permissions |
| Local safe baseline | `./synapse-cli install --agent hermes --dry-run`; then `--yes` | available baseline | Inspectable and safe, but requires checkout |
| Hermes native registry/package | `hermes skills install <identifier>` | future packaging slice | Native, but requires publication/package shape |

## Component Boundaries

- `Hermes installer skill`: `install/hermes-chat-install/SKILL.md`, the direct-link bootstrap skill
- `Hermes install guide`: public operator instructions, troubleshooting, and first-use prompt
- `Hermes adapter`: target resolution, dry-run/install plan, and payload verification for Hermes
- `Hermes-native verifier`: future integration that runs or summarizes `hermes skills list/check`
- `Package surface`: future Hermes registry/package shape if direct registry install becomes preferred

## Decisions

| Decision | Why | Tradeoff | Linked ADR |
| --- | --- | --- | --- |
| Use a direct `SKILL.md` installer skill for Hermes chatbox install | Hermes natively supports direct URL skill installation | Adds one installer skill artifact to maintain | `ADR-0006` |
| Keep `synapse-cli` as the write/verify engine | It already owns dry-run, manifest, and adapter target behavior | Installer skill is a wrapper, not a standalone installer | `ADR-0006` |
| Require Hermes-native verification in guide and future adapter hardening | File presence does not prove Hermes skill visibility | Full verification requires Hermes binary | `ADR-0006` |
| Preserve grouped SynapseOS skill family layout | SynapseOS has multiple canonical layers | Native registry publication may need later package decisions | `ADR-0006` |

## Delivery Impact

- Affected stories: `STORY-004A`, `STORY-004B`, `STORY-004C`, `STORY-004D`
- Verification impact: combine SynapseOS payload checks with Hermes-native skill checks where available
- Documentation impact: add `docs/HERMES_INSTALL.md` and link it from public onboarding docs
- Future code impact: likely changes to `init/synapse_cli/installer.py`, `init/synapse_cli/adapters.py`, or `verify` output if Hermes-native checks are integrated

## Risks And Open Questions

- Risk: Hermes session may not reload newly installed skills until a new session starts.
- Risk: Hermes skill metadata or direct-URL install behavior may change.
- Risk: grouped install under `~/.hermes/skills/synapseos` may need category-specific reshaping for ideal Hermes listing.
- Open question: should Hermes-native verification be part of `verify` by default or behind a flag?
- Open question: should a future registry package install a bootstrap skill only or the full family as separate category-scoped skills?
- Refresh trigger: Hermes docs/CLI, adapter behavior, installer skill, or package layout changes.
- Audit log entry: `AUDIT-001`
