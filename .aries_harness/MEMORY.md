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
- Primary content: 27 cognitive model skill directories plus `enabled/`, `interview/`, and `optimization/`
- Aries Harness root: `.aries_harness/`
- Canonical layer naming:
  - `Xuan Master`: core meta-cognition and 27-model kernel
  - `Archon`: enabler layer implemented primarily by `interview/` and `enabled/`, with `archon/SKILL.md` as the layer entrypoint
  - `Prism`: specialist layer for deeper domain routing, now materialized by `prism/SKILL.md` with future domain assets under `prism/domains/`
- Canonical request/spec/architecture baseline:
  - `REQ-001` at `.aries_harness/references/requests/REQ-001-repository-baseline.md`
  - `SPEC-001` at `.aries_harness/references/specs/SPEC-001-repository-baseline.md`
  - `ARCH-001` at `.aries_harness/decisions/architecture/ARCH-001-repository-layered-architecture.md`
  - `REVIEW-001` at `.aries_harness/references/reviews/REVIEW-001-skill-layer-structure.md`

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
