# Memory

## Artifact Header

- artifact id: `aries-memory-synapseos`
- artifact type: `memory_snapshot`
- status: `active`
- owner: `Arthur`
- canonical path: `.aries_harness/MEMORY.md`
- source of truth: `this file`
- upstream links: `MISSION.md`, `STATE.md`, `ADR.md`
- downstream links: `memory/INDEX.md`
- verification state: `initialized`
- last reviewed: `2026-05-21`
- next review or refresh trigger: `when a fact becomes important enough to reload in future sessions`
- run id: `pending`
- task id or slice id: `bootstrap`
- checkpoint id: `n/a`
- approval request id: `n/a`
- trace id: `pending`
- eval report id: `pending`
- audit log id: `pending`

## Hot Facts To Load First

- Repository root: `/home/ubuntu/work/harenss/Skills/Cogna`
- Remote: `git@github.com:agilewayai/SynapseOS.git`
- Current branch: `main`
- Primary content: `xuan-master/00-entry/` plus the `xuan-master/001-*` through `xuan-master/027-*` model directories, alongside `archon/interview/`, `archon/enabled/`, and `optimization/`
- Public docs: `README.md` and `docs/GETTING_STARTED.md`
- License: `Apache-2.0` in `LICENSE`
- Aries Harness root: `.aries_harness/`
- Canonical layer naming:
  - `Xuan Master`: core meta-cognition and 27-model kernel
  - `Archon`: enabler layer implemented primarily by `archon/interview/` and `archon/enabled/`, with `archon/SKILL.md` as the layer entrypoint
  - `Prism`: specialist layer for deeper domain routing, now materialized by `prism/SKILL.md` with future domain assets under `prism/domains/`
- Canonical request/spec/architecture baseline:
  - `REQ-001` at `.aries_harness/references/requests/REQ-001-repository-baseline.md`
  - `SPEC-001` at `.aries_harness/references/specs/SPEC-001-repository-baseline.md`
  - `ARCH-001` at `.aries_harness/decisions/architecture/ARCH-001-repository-layered-architecture.md`
  - `REVIEW-001` at `.aries_harness/references/reviews/REVIEW-001-skill-layer-structure.md`
- Initialization-layer specification baseline:
  - `REQ-002` at `.aries_harness/references/requests/REQ-002-synapseos-initialization-layer.md`
  - `SPEC-002` at `.aries_harness/references/specs/SPEC-002-synapseos-initialization-layer.md`
  - `ARCH-002` at `.aries_harness/decisions/architecture/ARCH-002-synapseos-initialization-layer.md`
  - `ADR-0004` at `.aries_harness/decisions/adrs/ADR-0004-synapseos-initialization-layer.md`

## Operating Notes

- Use `.aries_harness/` as the first-stop recovery surface
- Keep root harness docs concise and push detailed durable knowledge into `memory/cards/`
- Treat `history/` as generated later, not as a manual scratchpad

## Recent Decisions

- Adopt a minimal Aries Harness skeleton before further repository work
- Keep the harness repo-local and documentation-first
- Preserve the repository as a layered docs-first knowledge architecture
- Use `Xuan Master`, `Archon`, and `Prism` as the canonical internal layer names
- Materialize canonical layers as dedicated loadable entrypoints when the repo is meant for agent reuse
- Physically nest the `Xuan Master` catalog and 27-model kernel under `xuan-master/` to align the file layout with the layered architecture
- Physically nest the `Archon` interview and enabled components under `archon/` to align the file layout with the layered architecture
- Add a dedicated initialization layer and `synapse-cli` contract for prerequisite diagnosis, local setup, agent host installation, and verification
- Use Apache-2.0 as the project license
