# Architecture Design Pack

## Document Control

- Architecture ID: `ARCH-001`
- Artifact type: `architecture`
- Title: `Layered Xuan Master / Archon / Prism architecture for the current repository baseline`
- Status: `active`
- Owner: `Arthur`
- Related request: `REQ-001`
- Related spec: `SPEC-001`
- Child refs: `ADR-0002`, `ADR-0003`
- Last reviewed: `2026-05-21`
- Source of truth: `this file`

## Design Drivers

- Primary business outcome: keep the repository usable as an agent-agnostic cognitive model toolkit that another operator can understand and extend quickly
- Quality attributes:
  - inspectability
  - portability across agent environments
  - composability of model pipelines
  - low coupling between content modules
  - maintainable corpus evolution
- Constraints:
  - the corpus is primarily Markdown, not application code
  - the repository already exposes mixed naming between local path, product identity, and remote repo
  - helper scripts must remain subordinate to documented architecture

## Current And Target Shape

- Current state summary:
  - `AGENTS.md` and the harness now treat the repo as a layered skills stack
  - `xuan-master/SKILL.md` is the dedicated entrypoint for `Xuan Master`
  - `xuan-master/00-entry/SKILL.md` is the catalog and routing surface of that core
  - `xuan-master/001` through `xuan-master/027` form the 27-model `Xuan Master` kernel
  - `archon/SKILL.md` is the dedicated entrypoint for `Archon`
  - `archon/interview/` and `archon/enabled/` are the main current implementation surfaces of `Archon`
  - `prism/SKILL.md` is the dedicated entrypoint for `Prism`
  - `prism/domains/` is the placeholder surface for future specialist-domain assets
  - `optimization/` adds self-audit and recovery procedures as a cross-cutting loop
  - `.aries_harness/` now adds a governed recovery and design surface
- Target state summary: preserve the runtime/content layers above, keep the layer entrypoints explicit, keep the full `Xuan Master` corpus physically nested under `xuan-master/`, and make the request/spec/story/architecture truth explicit under `.aries_harness/` so future changes have one auditable upstream baseline
- Why the change is needed: without a canonical design baseline, the repository’s intent and seams remain distributed across multiple docs and scripts, which raises drift and resume cost

## Boundaries

- Domain links: no formal baseline domain package exists yet for `REQ-001`; working concepts implied by the repo are `cognitive_model`, `scene_combination`, `execution_pipeline`, `specialist_domain_mapping`, `agent_integration`, and `corpus_optimization`
- Component or module boundaries:
  - `Xuan Master core`: `xuan-master/SKILL.md`, `AGENTS.md`, `xuan-master/00-entry/SKILL.md`, `xuan-master/001-layered-architecture/` through `xuan-master/027-ai-native-mindset/`
  - `Archon calibration surface`: `archon/SKILL.md`, `archon/interview/SKILL.md`
  - `Archon execution surface`: `archon/enabled/SKILL.md`, `archon/enabled/references/`, `archon/enabled/templates/`, `archon/enabled/scripts/model-selector.py`
  - `Prism specialist layer`: `prism/SKILL.md` plus `prism/domains/` for future domain-specialization assets
  - `optimization loop`: `optimization/SKILL.md`, `optimization/references/`, `optimization/scripts/`
  - `governance layer`: `.aries_harness/`
- Integration boundaries:
  - agents consume Markdown directly by loading `SKILL.md` files
  - `Archon` may use `model-selector.py`, HTML templates, and future action helpers such as document or PDF generation, but does not replace the Markdown contract
  - `Prism` routes work into deeper specialist paths and domain-specific mapping logic, with a minimal dedicated repo surface now in place
  - optimization scripts analyze or recover corpus content rather than serve end-user runtime traffic
  - Aries Harness artifacts govern intent, design, and refresh rules but are not the product payload
- Data boundaries:
  - Markdown files are the primary knowledge source
  - helper scripts derive recommendations, audits, or recovery actions from files and session data
  - `history/` and `runs/` are secondary evidence surfaces, not the canonical source of project truth

## Decisions

| Decision | Why | Tradeoff | Linked ADR |
| --- | --- | --- | --- |
| Keep the knowledge base modular with one model per directory and one primary `SKILL.md` per model | This keeps the corpus inspectable, independently loadable, and portable across agent systems | Consistency must be maintained by discipline and audit rather than a compiled runtime | `ADR-0002` |
| Use `Xuan Master`, `Archon`, and `Prism` as the canonical internal layer names | The architecture becomes easier to discuss, extend, and map to capabilities | Directory names and conceptual layers are no longer identical and must be mapped explicitly | `ADR-0003` |
| Separate core, Archon, Prism, optimization, and harness responsibilities | Clear layer boundaries preserve reuse and make drift easier to inspect | Product truth is distributed across several docs and small scripts | `ADR-0002`, `ADR-0003` |
| Treat helper scripts as supporting infrastructure rather than the product core | The repo remains easy to understand by reading docs first | Script and doc drift is possible, especially where legacy paths remain | `ADR-0002` |
| Use Aries Harness artifacts as the canonical governed overlay for request/spec/story/architecture truth | Future work can start from stable design artifacts instead of chat memory | Maintainers must keep the harness docs refreshed as work evolves | `ADR-0001`, `ADR-0002` |

## Delivery Impact

- Affected stories: `STORY-001A`, `STORY-001B`, `STORY-001C`, `STORY-001D`
- Verification impact: current verification is mostly structural file inspection; if helper scripts are changed later, lightweight local script checks should be added
- Rollout or migration impact: low for this pass, but naming alignment and script hardening become important before broader publication
- Observability impact: the harness artifact pack now gives the repo a stable design-observability surface even before generated history is added

## Risks And Open Questions

- Risk: public identity and internal layer names can be conflated if their mapping is not kept explicit
- Risk: `optimization` scripts still reference Hermes-era paths, which makes local operability unclear
- Open question: how much specialist-domain structure should `Prism` gain beyond its new entrypoint and placeholder domain surface?
- Refresh trigger: any change to layer boundaries, helper-script responsibility, project naming model, or model-count contract
- Audit log entry: `AUDIT-001`
