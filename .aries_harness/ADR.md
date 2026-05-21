# Decisions

## Artifact Header

- artifact id: `aries-adr-synapseos`
- artifact type: `decision_log`
- status: `active`
- owner: `Arthur`
- canonical path: `.aries_harness/ADR.md`
- source of truth: `this file`
- upstream links: `MISSION.md`
- downstream links: `STATE.md`, `RUNBOOK.md`, `memory/INDEX.md`
- verification state: `initialized`
- last reviewed: `2026-05-21`
- next review or refresh trigger: `when a durable workflow or structural decision is made`
- run id: `pending`
- task id or slice id: `bootstrap`
- checkpoint id: `n/a`
- approval request id: `n/a`
- trace id: `pending`
- eval report id: `pending`
- audit log id: `pending`

## ADR-0001: Adopt Aries Harness As The Repo Recovery Surface

- Date: `2026-05-21`
- Status: `accepted`

### Context

The repository now has Git history and needs a stable, inspectable recovery surface for future agent work.

### Decision

Create a project-local `.aries_harness/` directory with the canonical Aries root docs, managed subdirectories, and an explicit hot/cold memory split.

### Consequences

- Future substantial work should update the harness root docs as part of completion
- Detailed durable memory can expand in `memory/cards/` without bloating `MEMORY.md`
- Generated history can be added later without replacing the canonical source artifacts

## ADR-0002: Preserve The Layered Docs-First Knowledge Architecture

- Date: `2026-05-21`
- Status: `accepted`
- Detailed record: `.aries_harness/decisions/adrs/ADR-0002-layered-docs-first-architecture.md`

### Context

The repository’s primary product is a structured knowledge corpus with small helper scripts, not a monolithic application runtime.

### Decision

Keep the catalog, kernel, interview, enabled, optimization, and Aries governance responsibilities separated, and keep `SKILL.md` files as the primary product contract.

### Consequences

- Documentation remains the first-stop source for understanding the system
- Helper scripts must stay aligned with the documented architecture
- Naming and operability cleanup become follow-on slices rather than implicit drift

## ADR-0003: Adopt Canonical Layer Names For The Skills Stack

- Date: `2026-05-21`
- Status: `accepted`
- Detailed record: `.aries_harness/decisions/adrs/ADR-0003-canonical-layer-names.md`

### Context

The repository now has a clearer internal architecture naming model than the earlier generic labels of core, enabled, and specialist behavior.

### Decision

Use `Xuan Master` for the meta-cognition core, `Archon` for the enabler layer, and `Prism` for the specialist layer.

### Consequences

- Entry docs and design artifacts should use these names consistently
- Physical directory names may lag the conceptual architecture and must be mapped explicitly
- Future work should decide how deeply `Prism` domain assets materialize in the repo beyond its new top-level entrypoint

## ADR-0004: Add A SynapseOS Initialization Layer And synapse-cli Contract

- Date: `2026-05-21`
- Status: `accepted`
- Detailed record: `.aries_harness/decisions/adrs/ADR-0004-synapseos-initialization-layer.md`

### Context

SynapseOS needs a first-class installation and host onboarding surface for multi-agent use.

### Decision

Add a dedicated initialization layer with `synapse-cli` as the command interface for prerequisite diagnosis, local initialization, host installation, and verification.

### Consequences

- Installation becomes inspectable and repeatable across supported agent hosts
- Host-specific installation behavior should live behind adapters
- Future implementation must keep prerequisite installation and external writes approval-gated
