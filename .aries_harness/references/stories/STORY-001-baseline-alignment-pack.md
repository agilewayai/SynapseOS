# Story Slice Pack

## Document Control

- Pack ID: `STORY-001`
- Artifact type: `story-pack`
- Objective mode: `documentation_alignment`
- Parent request: `REQ-001`
- Parent spec: `SPEC-001`
- Owner: `Arthur`
- Current sprint or increment: `baseline-distillation`
- Last reviewed: `2026-05-21`
- Child refs: `ARCH-001`, `ADR-0002`, `ADR-0003`
- Source of truth: `this file`

## Belongs Here

- Thin vertical slice boundaries
- Current and next increments for making the repository contract auditable
- Acceptance anchors and verification plans
- Dependencies on design artifacts
- Regression guardrails for each slice

## Keep Out

- Full business case restatement
- Whole-repository architecture narrative
- Raw execution logs

## Slice Overview

| Story ID | Story statement | User value | Acceptance anchor | Status | Linked design artifacts |
| --- | --- | --- | --- | --- | --- |
| `STORY-001A` | As a maintainer, I need a canonical request/spec/story/architecture pack so I can resume work without rediscovering the project contract | Faster recovery and lower drift | The artifact pack exists under `.aries_harness/` with stable IDs and cross-links | `accepted` | `ARCH-001`, `ADR-0002` |
| `STORY-001B` | As an external reader, I need one coherent internal architecture so I can understand what `Xuan Master`, `Archon`, and `Prism` mean | Better onboarding and architectural clarity | Entry docs and architecture artifacts align on the canonical layer names and their repo mapping | `accepted` | `ARCH-001`, `ADR-0003` |
| `STORY-001C` | As an operator, I need helper scripts to match the repo’s actual layout so I can trust local validation and recovery guidance | Better operability | Legacy path assumptions are either removed or clearly documented with local verification rules | `ready` | `ARCH-001`, `ADR-0002` |
| `STORY-001D` | As a maintainer, I need a clear decision on whether `Prism` becomes a dedicated repo surface so the specialist layer does not stay ambiguous | Better specialization roadmap clarity | The repo exposes a deliberate `Prism` surface through `prism/SKILL.md` and `prism/domains/` | `accepted` | `ARCH-001`, `ADR-0003` |

## Story Detail Template

### Story:

- Story ID: `STORY-001A`
- User story: As a maintainer, I need a canonical request/spec/story/architecture pack so I can resume work without rediscovering the project contract
- Slice type: `alignment`
- Why this slice matters now: the repo already has Git and Aries Harness state, but it still lacks a durable upstream design baseline
- Acceptance criteria:
  - `REQ-001`, `SPEC-001`, `STORY-001`, `ARCH-001`, and `ADR-0002` exist
  - the artifact register, traceability matrix, refresh policy, and audit log exist
  - the artifacts match the actual repository files and layers
- Verification plan: inspect the new `.aries_harness/` design surfaces and compare them against the current repo files
- Before or after evidence expectation: after-state file inspection only
- Domain artifacts touched: `none`
- Architecture artifacts touched: `ARCH-001`
- ADR impact: `ADR-0002`
- Release or rollout note: `n/a`
- Refresh trigger: once complete, only if the baseline meaning changes
- Audit log entry: `AUDIT-001`

### Story:

- Story ID: `STORY-001B`
- User story: As an external reader, I need one coherent internal architecture so I can understand what `Xuan Master`, `Archon`, and `Prism` mean
- Slice type: `alignment`
- Why this slice matters now: the layer naming model is now explicit and should be reflected in the canonical docs immediately
- Acceptance criteria:
  - `AGENTS.md`, `xuan-master/00-entry/SKILL.md`, and the architecture artifacts use `Xuan Master`, `Archon`, and `Prism` consistently
  - the mapping from conceptual layers to current repo surfaces is explicit
- Verification plan: inspect `AGENTS.md`, `xuan-master/SKILL.md`, `xuan-master/00-entry/SKILL.md`, `enabled/SKILL.md`, `interview/SKILL.md`, and the request/spec/architecture artifacts for layer-name and path consistency
- Before or after evidence expectation: before/after documentation diff
- Domain artifacts touched: `pending`
- Architecture artifacts touched: `ARCH-001`
- ADR impact: `ADR-0003`
- Release or rollout note: clarifies internal architecture before wider publication
- Refresh trigger: once the layer naming model or repo mapping changes
- Audit log entry: `AUDIT-001`

### Story:

- Story ID: `STORY-001C`
- User story: As an operator, I need helper scripts to match the repo’s actual layout so I can trust local validation and recovery guidance
- Slice type: `governance`
- Why this slice matters now: `optimization` scripts still show legacy Hermes assumptions that are inconsistent with the current repo root
- Acceptance criteria:
  - helper-script path assumptions are reviewed and made explicit
  - repo-local verification rules are written down
  - any remaining legacy assumptions are tracked as intentional debt
- Verification plan: inspect `enabled/scripts/` and `optimization/scripts/`, then run the relevant lightweight checks if scripts are changed
- Before or after evidence expectation: script review plus any local command output from future hardening work
- Domain artifacts touched: `none`
- Architecture artifacts touched: `ARCH-001`
- ADR impact: `possible`
- Release or rollout note: improves local operator trust before broader adoption
- Refresh trigger: when script behavior or runtime assumptions change
- Audit log entry: `AUDIT-001`

### Story:

- Story ID: `STORY-001D`
- User story: As a maintainer, I need a clear decision on whether `Prism` becomes a dedicated repo surface so the specialist layer does not stay ambiguous
- Slice type: `alignment`
- Why this slice matters now: `Prism` was canonical in the architecture but needed a concrete repo surface
- Acceptance criteria:
  - `prism/SKILL.md` exists as the layer entrypoint
  - `prism/domains/README.md` exists as the future specialist-domain placeholder surface
  - the new mapping is reflected in entry docs and design artifacts
- Verification plan: inspect the architecture pack, ADRs, and the new `prism/` surface
- Before or after evidence expectation: documentation diff or new directory structure
- Domain artifacts touched: `future domain package if needed`
- Architecture artifacts touched: `ARCH-001`
- ADR impact: `ADR-0003` or later
- Release or rollout note: improves long-term specialization clarity
- Refresh trigger: when the specialist layer gains real domain packs or changes its repo shape
- Audit log entry: `AUDIT-001`

## Follow-on Slices

- Next likely slice: `STORY-001C`
- Deferred slice: create a domain package if architecture work starts needing explicit bounded contexts
