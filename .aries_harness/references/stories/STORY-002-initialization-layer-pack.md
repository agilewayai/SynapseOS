# Story Slice Pack

## Document Control

- Pack ID: `STORY-002`
- Artifact type: `story-pack`
- Objective mode: `functional_capability`
- Parent request: `REQ-002`
- Parent spec: `SPEC-002`
- Owner: `Arthur`
- Current sprint or increment: `synapse-cli-baseline-implementation`
- Last reviewed: `2026-05-21`
- Child refs: `ARCH-002`, `ADR-0004`, `DOM-002`
- Source of truth: `this file`

## Belongs Here

- Thin vertical slices for the SynapseOS initialization layer
- Acceptance anchors for `synapse-cli`
- Verification expectations for prerequisite checks and host installation
- Boundaries that keep installation work separate from the cognitive skill corpus

## Keep Out

- Full CLI implementation details
- Exact host filesystem paths before implementation verification
- Release packaging process

## Slice Overview

| Story ID | Story statement | User value | Acceptance anchor | Status | Linked design artifacts |
| --- | --- | --- | --- | --- | --- |
| `STORY-002A` | As a maintainer, I need a governed initialization-layer spec so implementation can start from stable acceptance and architecture | Lower implementation drift | `REQ-002`, `SPEC-002`, `STORY-002`, `ARCH-002`, `ADR-0004`, register, trace, and audit rows exist | `accepted` | `ARCH-002`, `ADR-0004` |
| `STORY-002B` | As an operator, I need a runnable `synapse-cli` skeleton so I can inspect install commands before host-specific logic lands | Clear CLI entrypoint | CLI help, command parser, `doctor`, `list-agents`, and `--json` shape exist | `accepted` | `ARCH-002`, `DOM-002` |
| `STORY-002C` | As an operator, I need prerequisite checks before installation so I can understand what is missing and what is safe to install | Safer first-run setup | `doctor` reports runtime readiness, missing prerequisites, permissions, and remediation hints | `accepted` | `ARCH-002`, `DOM-002` |
| `STORY-002D` | As an agent user, I need named host installers so SynapseOS can be installed into my target agent environment | Multi-agent adoption | Adapters exist for `claude-code`, `codex`, `cursor`, `opencode`, `openclaw`, and `hermes` | `accepted-baseline` | `ARCH-002`, `DOM-002` |
| `STORY-002E` | As an integrator, I need a generic host installer so non-listed agent hosts can still consume SynapseOS | Open-ended host support | `install --agent generic --target <path>` writes a manifest and places expected entrypoints | `accepted` | `ARCH-002`, `DOM-002` |
| `STORY-002F` | As a maintainer, I need install verification so support issues can distinguish install drift from skill content issues | Faster diagnosis | `verify --agent <agent>` checks installed entrypoints and reports actionable failures | `accepted-baseline` | `ARCH-002`, `DOM-002` |

## Story Details

### Story:

- Story ID: `STORY-002A`
- User story: As a maintainer, I need a governed initialization-layer spec so implementation can start from stable acceptance and architecture
- Slice type: `artifact_shaping`
- Why this slice matters now: the requested installation layer affects repository shape, CLI behavior, and external host writes, so it needs explicit acceptance and architecture before coding
- Acceptance criteria:
  - `REQ-002`, `SPEC-002`, `STORY-002`, `ARCH-002`, and `ADR-0004` exist
  - register, traceability, and audit surfaces include the new artifact family
  - the spec lists supported agent hosts and the generic host route
  - the architecture describes prerequisite checking, install planning, host adapters, and verification
- Verification plan: inspect the new artifact files and run search checks for all new artifact IDs
- Before or after evidence expectation: after-state file inspection only
- Domain artifacts touched: `DOM-002`
- Architecture artifacts touched: `ARCH-002`, `ADR-0004`
- ADR impact: `ADR-0004`
- Release or rollout note: `n/a`
- Refresh trigger: if initialization layer scope, CLI commands, or supported hosts change
- Audit log entry: `AUDIT-001`

### Story:

- Story ID: `STORY-002B`
- User story: As an operator, I need a runnable `synapse-cli` skeleton so I can inspect install commands before host-specific logic lands
- Slice type: `implementation`
- Why this slice matters now: it creates the executable entrypoint and command shape for all later host adapters
- Acceptance criteria:
  - `synapse-cli --help` lists the supported command groups
  - `synapse-cli doctor`, `synapse-cli init`, `synapse-cli list-agents`, `synapse-cli install`, and `synapse-cli verify` parse successfully
  - commands support `--json` where output is expected
  - unimplemented host actions fail with clear messages, not stack traces
- Verification plan: run CLI help and command parser smoke checks
- Before or after evidence expectation: local command output in the implementation checkpoint or run artifact
- Domain artifacts touched: `DOM-002`
- Architecture artifacts touched: `ARCH-002`
- ADR impact: `none expected`
- Release or rollout note: CLI remains local and unreleased; named adapters provide baseline target resolution and need host-native smoke checks later
- Refresh trigger: when command names or global options change
- Audit log entry: `AUDIT-001`

### Story:

- Story ID: `STORY-002C`
- User story: As an operator, I need prerequisite checks before installation so I can understand what is missing and what is safe to install
- Slice type: `implementation`
- Why this slice matters now: prerequisite checks are the safety gate for any installation flow
- Acceptance criteria:
  - `doctor` distinguishes required, optional, missing, detected, and installable prerequisites
  - `doctor` is read-only by default
  - remediation hints explain manual and CLI-assisted options
  - any automatic install path requires explicit confirmation or a documented `--yes` mode
- Verification plan: run `doctor` on the local machine and inspect structured output
- Before or after evidence expectation: local command output in the implementation checkpoint or run artifact
- Domain artifacts touched: `DOM-002`
- Architecture artifacts touched: `ARCH-002`
- ADR impact: `possible if prerequisite policy changes`
- Release or rollout note: prerequisite installation remains approval-gated
- Refresh trigger: when runtime dependency assumptions change
- Audit log entry: `AUDIT-001`

## Follow-on Slices

- Next likely slice: harden named host adapters with host-native smoke checks where available
- Secondary next slice: add uninstall or rollback planning if operator workflow needs it
- Deferred slice: package `synapse-cli` for global invocation or release-channel installation

## Implementation Evidence

- Code: `synapse-cli`, `init/SKILL.md`, `init/synapse_cli/`
- Tests: `tests/test_synapse_cli.py`
- Domain package: `.aries_harness/references/domain/DOM-002-synapseos-initialization-domain.md`
- Verification: `python3 -m unittest discover -s tests`; `./synapse-cli --help`; `./synapse-cli doctor --json`; generic dry-run, install, and verify smoke checks
