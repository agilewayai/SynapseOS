# Story Slice Pack

## Document Control

- Pack ID: `STORY-003`
- Artifact type: `story-pack`
- Objective mode: `functional_capability`
- Parent request: `REQ-003`
- Parent spec: `SPEC-003`
- Owner: `Arthur`
- Current sprint or increment: `openclaw-install-shaping`
- Last reviewed: `2026-05-21`
- Child refs: `ARCH-003`, `ADR-0005`
- Source of truth: `this file`

## Belongs Here

- OpenClaw-specific installation and learning slices, including chatbox paste-link install mode
- Acceptance anchors for a one-link quick install experience
- Verification expectations that combine SynapseOS and OpenClaw-native evidence
- Guardrails for remote install convenience versus safety

## Keep Out

- Non-OpenClaw host behavior
- ClawHub publication work until the local and one-link paths are stable
- Destructive uninstall or force-overwrite behavior without a separate approval-gated story

## Slice Overview

| Story ID | Story statement | User value | Acceptance anchor | Status | Linked design artifacts |
| --- | --- | --- | --- | --- | --- |
| `STORY-003A` | As an OpenClaw user, I need a detailed install guide and governed quick-install spec so I can install SynapseOS confidently | Faster onboarding | OpenClaw guide and artifact package exist with current-safe and target chatbox paths | `accepted` | `SPEC-003`, `ARCH-003`, `ADR-0005` |
| `STORY-003B` | As an OpenClaw user, I need a paste-link chatbox installer so OpenClaw can finish installing the SynapseOS skill family from chat | Low-friction adoption | `install/openclaw-chat-install.md` provides the link prompt, safe dry-run path, install commands, verification, and learning prompt | `accepted` | `ARCH-003`, `ADR-0005` |
| `STORY-003C` | As an OpenClaw user, I need OpenClaw-native verification so I know the host can actually see SynapseOS | Trustworthy install | `synapse-cli verify --agent openclaw` can include or guide `openclaw skills check --json` evidence | `ready` | `ARCH-003` |
| `STORY-003D` | As an OpenClaw user, I need native package/source install compatibility so I can use OpenClaw's own skill installer when possible | Host-native UX | SynapseOS has a package shape compatible with OpenClaw's supported install sources and metadata rules | `planned` | `ARCH-003` |
| `STORY-003E` | As a maintainer, I need an OpenClaw compatibility check so install drift is caught before support issues | Lower support load | Checklist or test validates SynapseOS payload, `SKILL.md` metadata compatibility, and OpenClaw skill visibility where OpenClaw is installed | `planned` | `ARCH-003` |
| `STORY-003F` | As an OpenClaw user, I need an optional shell one-link installer so I can install outside chat when appropriate | Low-friction shell setup | `install/openclaw.sh` supports dry-run, target override, conflict checks, install, verify, and learning prompt | `planned` | `ARCH-003`, `ADR-0005` |

## Story Details

### Story

- Story ID: `STORY-003A`
- User story: As an OpenClaw user, I need a detailed install guide and governed quick-install spec so I can install SynapseOS confidently
- Slice type: `documentation_alignment`
- Why this slice matters now: the baseline OpenClaw adapter exists, but OpenClaw users need a host-native guide and a clear one-link target before more automation is added
- Acceptance criteria:
  - `REQ-003`, `SPEC-003`, `STORY-003`, `ARCH-003`, and `ADR-0005` exist
  - `docs/OPENCLAW_INSTALL.md` exists
  - the guide includes prerequisites, chatbox paste-link mode, safe local install, OpenClaw-native verification, learning prompt, update path, and troubleshooting
  - traceability and audit surfaces link the new artifact family
- Verification plan: file inspection, link scan, and markdown diff review
- Before or after evidence expectation: after-state file inspection
- Domain artifacts touched: `none in this slice`
- Architecture artifacts touched: `ARCH-003`, `ADR-0005`
- ADR impact: `ADR-0005`
- Refresh trigger: OpenClaw interface or SynapseOS OpenClaw adapter changes
- Audit log entry: `AUDIT-001`

### Story

- Story ID: `STORY-003B`
- User story: As an OpenClaw user, I need a paste-link chatbox installer so OpenClaw can finish installing the SynapseOS skill family from chat
- Slice type: `documentation_alignment`
- Why this slice matters now: the requested install mode is OpenClaw-channel driven, so users need one stable link plus a minimal prompt that tells OpenClaw how to complete installation safely
- Acceptance criteria:
  - `install/openclaw-chat-install.md` exists
  - the prompt includes the raw GitHub link, source repo, default OpenClaw target, safety policy, install commands, verification commands, success response, and failure response
  - `docs/OPENCLAW_INSTALL.md` includes the exact chatbox prompt users should paste
  - public docs and traceability link the prompt
- Verification plan: file inspection, artifact link scan, OpenClaw dry-run through `synapse-cli install --agent openclaw --dry-run --json`
- Domain artifacts touched: `none in this slice`
- Architecture artifacts touched: `ARCH-003`
- ADR impact: `ADR-0005`
- Refresh trigger: raw prompt URL, repo URL, OpenClaw target, or install command changes
- Audit log entry: `AUDIT-001`

### Story

- Story ID: `STORY-003C`
- User story: As an OpenClaw user, I need OpenClaw-native verification so I know the host can actually see SynapseOS
- Slice type: `implementation`
- Why this slice matters now: SynapseOS file verification and OpenClaw skill visibility are different evidence surfaces
- Acceptance criteria:
  - `synapse-cli verify --agent openclaw` can detect whether `openclaw` is available
  - verification can run or instruct `openclaw skills check --json`
  - output distinguishes `payload_ok` from `openclaw_visible`
  - missing OpenClaw produces a clear warning instead of a hard failure when payload verification passes
- Verification plan: unit tests plus manual smoke on a host with OpenClaw installed
- Domain artifacts touched: `DOM-002` may need refresh if verification report fields change
- Architecture artifacts touched: `ARCH-003`
- ADR impact: `none expected`
- Refresh trigger: OpenClaw CLI command shape changes
- Audit log entry: `future`

## Follow-On Slices

- Next likely slice: implement OpenClaw-native verification in the adapter
- Secondary next slice: add the optional shell one-link installer script after safety review
- Deferred slice: publish or reshape SynapseOS for OpenClaw-native package installation

## Implementation Evidence

- Current evidence: `docs/OPENCLAW_INSTALL.md`, `install/openclaw-chat-install.md`, `SPEC-003`, `ARCH-003`, `ADR-0005`
- Existing related implementation: `synapse-cli`, `init/synapse_cli/adapters.py`, `init/synapse_cli/installer.py`
- Future evidence: one-link script, OpenClaw-native verification output, optional packaging artifacts
