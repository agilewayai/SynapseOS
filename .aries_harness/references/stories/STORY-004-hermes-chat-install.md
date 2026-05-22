# Story Slice Pack

## Document Control

- Pack ID: `STORY-004`
- Artifact type: `story-pack`
- Objective mode: `functional_capability`
- Parent request: `REQ-004`
- Parent spec: `SPEC-004`
- Owner: `Arthur`
- Current sprint or increment: `hermes-chat-install`
- Last reviewed: `2026-05-21`
- Child refs: `ARCH-004`, `ADR-0006`
- Source of truth: `this file`

## Belongs Here

- Hermes-specific installation and learning slices
- Acceptance anchors for direct-URL `SKILL.md` installer behavior
- Verification expectations that combine SynapseOS and Hermes-native evidence

## Keep Out

- Non-Hermes host behavior
- Registry publication until direct-link and local install paths are stable
- Destructive uninstall or force-overwrite behavior without a separate story

## Slice Overview

| Story ID | Story statement | User value | Acceptance anchor | Status | Linked design artifacts |
| --- | --- | --- | --- | --- | --- |
| `STORY-004A` | As a Hermes user, I need a direct-link installer skill and guide so Hermes can install the SynapseOS skill family from chat | Low-friction adoption | `install/hermes-chat-install/SKILL.md`, `docs/HERMES_INSTALL.md`, and artifact package exist | `accepted` | `SPEC-004`, `ARCH-004`, `ADR-0006` |
| `STORY-004B` | As a Hermes user, I need Hermes-native verification so I know the host can actually see SynapseOS | Trustworthy install | `synapse-cli verify --agent hermes` can include or guide `hermes skills list/check` evidence | `ready` | `ARCH-004` |
| `STORY-004E` | As an existing Hermes user, I need the paste-link installer to update an existing grouped install safely | Smooth upgrade | dry-run reports existing grouped or old-version state, approved install refreshes the payload, and unrecognized payloads are blocked | `implemented` | `ARCH-004`, `ADR-0006` |
| `STORY-004C` | As a Hermes user, I need native package or registry installation so I can install SynapseOS through Hermes' own registry flow when available | Host-native UX | SynapseOS has a Hermes-supported package or registry source | `planned` | `ARCH-004` |
| `STORY-004D` | As a maintainer, I need Hermes compatibility checks so install drift is caught early | Lower support load | Checklist or test validates payload and Hermes skill visibility where Hermes is installed | `planned` | `ARCH-004` |

## Story Details

### Story

- Story ID: `STORY-004A`
- User story: As a Hermes user, I need a direct-link installer skill and guide so Hermes can install the SynapseOS skill family from chat
- Slice type: `documentation_alignment`
- Why this slice matters now: Hermes can install direct `SKILL.md` URLs, so SynapseOS can provide a native installer skill instead of relying only on manual file copy
- Acceptance criteria:
  - `REQ-004`, `SPEC-004`, `STORY-004`, `ARCH-004`, and `ADR-0006` exist
  - `install/hermes-chat-install/SKILL.md` exists with Hermes frontmatter and install workflow
  - `docs/HERMES_INSTALL.md` exists
  - public docs link the Hermes guide
  - traceability and audit surfaces include the new artifact family
- Verification plan: file inspection, artifact ID search, `hermes skills install --help`, `./synapse-cli install --agent hermes --dry-run --json`, and unit tests
- Before or after evidence expectation: after-state file inspection and local command output
- Domain artifacts touched: `none in this slice`
- Architecture artifacts touched: `ARCH-004`, `ADR-0006`
- ADR impact: `ADR-0006`
- Refresh trigger: Hermes skill interface or install command changes
- Audit log entry: `AUDIT-001`

### Story

- Story ID: `STORY-004E`
- User story: As an existing Hermes user, I need the paste-link installer to update an existing grouped install safely
- Slice type: `implementation`
- Why this slice matters now: Hermes one-link mode should support both first install and repeat update without asking users to manually remove `~/.hermes/skills/synapseos`
- Acceptance criteria:
  - dry-run reports `install_mode: update` for an existing grouped SynapseOS payload
  - dry-run reports `previous_installation.status: existing_grouped_payload`
  - dry-run reports `previous_installation.payload.version_status` before refresh
  - approved install refreshes the grouped payload in place
  - unrecognized existing `synapseos/` directories are blocked as `conflict_existing_payload`
  - verification passes after update
- Verification plan: unit tests for Hermes update and unrecognized payload blocking plus `synapse-cli verify --agent hermes`
- Architecture artifacts touched: `ARCH-004`
- ADR impact: `ADR-0006`
- Refresh trigger: Hermes install target or grouped payload marker changes

### Story

- Story ID: `STORY-004B`
- User story: As a Hermes user, I need Hermes-native verification so I know the host can actually see SynapseOS
- Slice type: `implementation`
- Why this slice matters now: file presence does not prove Hermes skill visibility
- Acceptance criteria:
  - `synapse-cli verify --agent hermes` can detect whether `hermes` is available
  - verification can run or instruct `hermes skills list` and `hermes skills check`
  - output distinguishes payload integrity from Hermes visibility
  - missing Hermes produces a clear warning when payload verification passes
- Verification plan: unit tests plus manual smoke on a host with Hermes installed
- Domain artifacts touched: `DOM-002` may need refresh if verification report fields change
- Architecture artifacts touched: `ARCH-004`
- ADR impact: `none expected`
- Refresh trigger: Hermes CLI command shape changes
- Audit log entry: `future`

## Follow-On Slices

- Next likely slice: implement Hermes-native verification in the adapter
- Secondary next slice: evaluate a Hermes registry/native package distribution path
- Deferred slice: add automated Hermes compatibility checks where Hermes is installed

## Implementation Evidence

- Current evidence: `install/hermes-chat-install/SKILL.md`, `docs/HERMES_INSTALL.md`, `SPEC-004`, `ARCH-004`, `ADR-0006`
- Existing related implementation: `synapse-cli`, `init/synapse_cli/adapters.py`, `init/synapse_cli/installer.py`
- Current implementation evidence: `tests/test_synapse_cli.py` covers Hermes update mode and unrecognized payload blocking
- Future evidence: Hermes-native verification output and optional registry/package artifacts
