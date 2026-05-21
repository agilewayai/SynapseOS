# Spec Package

## Document Control

- Spec ID: `SPEC-001`
- Artifact type: `spec`
- Objective mode: `documentation_alignment`
- Title: `Current repository behavior and structure baseline`
- Status: `active`
- Owner: `Arthur`
- Parent request: `REQ-001`
- Child refs: `STORY-001`, `ARCH-001`, `ADR-0002`, `ADR-0003`, `TRACE-001`
- Last reviewed: `2026-05-21`
- Source of truth: `this file`

## Belongs Here

- Objective: define what must remain true about the current repository’s product contract, system layers, and operator-facing usage model
- In scope:
  - the repository as an agent-agnostic layered skills stack
  - the `Xuan Master` meta-cognition core and its 27-model kernel
  - the `Archon` enabler layer and its calibration/execution surfaces
  - the `Prism` specialist layer and its routing/mapping role
  - the `optimization` self-improvement loop
  - the small helper scripts and templates that support those layers
  - the Aries Harness artifact baseline that now records the contract
- Out of scope:
  - changing the meaning of existing model content
  - creating a domain package
  - implementing CI, packaging automation, or release tooling
  - renaming the repository or harmonizing all public naming in this pass
- Primary actors:
  - human maintainer curating the knowledge base
  - AI coding agent or LLM loading the skills as context
  - downstream integrator wiring the repository into an agent environment
- Key flows:
  - agent or operator starts at `AGENTS.md` or `xuan-master/00-entry/SKILL.md`
  - `Xuan Master` catalog or scene recommendations route the user to one or more model `SKILL.md` files
  - `Archon` can calibrate ambiguous problems through `interview/SKILL.md`
  - `Archon` can orchestrate structured execution, actions, and generation through `enabled/SKILL.md` and its helper references/scripts
  - `Prism` maps work into deeper, more specialized domain paths
  - corpus quality and recovery work can be handled through `optimization/`
- Acceptance conditions:
  - the repository is describable as a layered, docs-first system rather than a generic Markdown dump
  - each cognitive model remains independently loadable from its own `SKILL.md`
  - `Xuan Master`, `Archon`, and `Prism` are the canonical layer names in the design surface
  - the current repo mapping of those layers is explicit and loadable through dedicated layer entrypoints
  - helper scripts remain supporting surfaces rather than the primary product runtime
  - the harness artifact pack captures the current contract and links it to architecture decisions
- NFRs:
  - inspectability by file inspection alone
  - portability across multiple agent environments
  - composability of model pipelines
  - low coupling between models
  - concise recovery for future operators
- Quality heuristics or target qualities:
  - the fastest way to understand the repo should be reading Markdown, not tracing code
  - each top-level layer should own one clear responsibility
  - scripts should reflect the documented architecture instead of silently redefining it
  - public identity drift, layer-name drift, and legacy assumptions should be visible as explicit risks
- Regression guardrails:
  - preserve the `Xuan Master` 27-model kernel and scene-routing concept
  - preserve the documented split between `Xuan Master`, `Archon`, `Prism`, and `optimization`
  - do not move canonical product truth into generated history or run logs
  - do not let a helper script become the only place where routing logic or corpus policy is knowable
- Touched surfaces:
  - `AGENTS.md`
  - `xuan-master/SKILL.md`
  - `xuan-master/00-entry/SKILL.md`
  - `xuan-master/001-layered-architecture/SKILL.md`
  - `enabled/SKILL.md`
  - `enabled/scripts/model-selector.py`
  - `interview/SKILL.md`
  - `optimization/SKILL.md`
  - `optimization/scripts/full_audit.py`
  - `optimization/scripts/recover_from_session.py`
  - `.aries_harness/`
- Operational concerns:
  - some scripts still assume legacy Hermes paths
  - public identity is not yet fully aligned across local path, repo remote, and product docs
  - verification is mostly structural today because the product is knowledge-first
- Rollout or migration concerns:
  - if the repository is published more broadly, a GitHub-facing `README.md` and naming alignment become release-blocking
  - if helper scripts are expected to run in this repo directly, legacy path assumptions must be fixed before claiming local operability

## Slice Candidates

| Slice ID | User value | Acceptance anchor | Priority | Notes |
| --- | --- | --- | --- | --- |
| `STORY-001A` | Maintainers get a canonical baseline artifact pack | Request, spec, story, architecture, ADR, register, traceability, and audit surfaces exist and cross-link | `now` | This pass |
| `STORY-001B` | External readers see one coherent internal architecture | Entry docs and architecture artifacts align on `Xuan Master`, `Archon`, and `Prism` | `now` | Layer naming clarification |
| `STORY-001C` | Operators can trust helper scripts locally | Script path assumptions and verification rules are explicit and repo-local | `next` | Operability hardening |
| `STORY-001D` | Maintainers can see how `Prism` materializes in the repo | The specialist layer has an explicit layer entrypoint and future-domain placeholder surface | `done` | Specialist-layer clarity |

## Keep Out

- Marketing copy beyond what is needed to describe the contract
- Live backlog state or delivery evidence
- Detailed release plan

## Design Implications

- Domain implications: a formal domain package is still pending, but the current domain concepts are `cognitive_model`, `scene_pipeline`, `specialist_domain_mapping`, `agent_integration`, `operator`, and `corpus_optimization`
- Architecture implications: the repository should be treated as a layered documentation system with small helper runtimes, not as a monolithic application
- Expected ADRs: `ADR-0002`, `ADR-0003`

## Linked Artifacts

- Story-slice pack: `.aries_harness/references/stories/STORY-001-baseline-alignment-pack.md`
- Domain package: `pending`
- Architecture design pack: `.aries_harness/decisions/architecture/ARCH-001-repository-layered-architecture.md`
- Traceability matrix: `.aries_harness/references/VALUE-TRACEABILITY-MATRIX.md`

## Open Questions And Risks

- Open question: how much of the `Prism` specialist layer should be formalized next beyond the new entrypoint and placeholder domain surface?
- Risk: if public identity and internal layer naming stay mixed together, future README, packaging, and artifact work will drift
- Refresh trigger: any meaningful change to model count, layer boundaries, agent integration guidance, or helper-script contract
- Audit log entry: `AUDIT-001`
