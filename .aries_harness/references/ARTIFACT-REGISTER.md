# Artifact Register

## Artifact header

- Artifact ID: `REG-001`
- Artifact type: `artifact-register`
- Status: `active`
- Owner: `Arthur`
- Canonical path: `.aries_harness/references/ARTIFACT-REGISTER.md`
- Source of truth: `this file`
- Upstream links: `REQ-001`, `SPEC-001`, `STORY-001`, `ARCH-001`, `ADR-0003`
- Downstream links: `TRACE-001`, `POL-001`, `AUDIT-001`, `REVIEW-001`
- Verification state: `initialized`
- Last reviewed: `2026-05-21`
- Next review / refresh trigger: `refresh in the same pass as any meaningful request/spec/story/architecture/ADR update`

## Runtime links

- Run ID: `pending`
- Task ID / Slice ID: `distill-current-project-baseline`
- Checkpoint ID: `n/a`
- Approval Request ID: `n/a`
- Trace ID: `TRACE-001`
- Eval Report ID: `pending`
- Audit Log ID: `AUDIT-001`

| Artifact ID | Type | Canonical path | Owner | Phase | Status | Verification state | Last reviewed | Source of truth | Refresh trigger | Runtime links | Upstream links | Downstream links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `REQ-001` | `request` | `.aries_harness/references/requests/REQ-001-repository-baseline.md` | `Arthur` | `intake` | `active` | `distilled from current repo` | `2026-05-21` | `that file` | `project identity, internal layer names, purpose, or scope changes` | `TRACE-001; AUDIT-001` | `MISSION.md; AGENTS.md` | `SPEC-001; STORY-001; ARCH-001; ADR-0003` |
| `SPEC-001` | `spec` | `.aries_harness/references/specs/SPEC-001-repository-baseline.md` | `Arthur` | `shaping` | `active` | `distilled from current repo` | `2026-05-21` | `that file` | `layer contract, model count, or integration guidance changes` | `TRACE-001; AUDIT-001` | `REQ-001` | `STORY-001; ARCH-001; ADR-0002; ADR-0003` |
| `STORY-001` | `story-pack` | `.aries_harness/references/stories/STORY-001-baseline-alignment-pack.md` | `Arthur` | `slice-planning` | `active` | `baseline slices defined` | `2026-05-21` | `that file` | `active or next slice changes` | `TRACE-001; AUDIT-001` | `REQ-001; SPEC-001` | `ARCH-001; ADR-0002; ADR-0003` |
| `ARCH-001` | `architecture` | `.aries_harness/decisions/architecture/ARCH-001-repository-layered-architecture.md` | `Arthur` | `design` | `active` | `distilled from current repo` | `2026-05-21` | `that file` | `layer boundaries, layer mapping, or script responsibilities change` | `TRACE-001; AUDIT-001` | `REQ-001; SPEC-001` | `ADR-0002; ADR-0003` |
| `ADR-0002` | `adr` | `.aries_harness/decisions/adrs/ADR-0002-layered-docs-first-architecture.md` | `Arthur` | `design` | `accepted` | `accepted by repository inspection` | `2026-05-21` | `that file` | `architecture decision meaning changes` | `AUDIT-001` | `ARCH-001` | `STORY-001B; STORY-001C` |
| `ADR-0003` | `adr` | `.aries_harness/decisions/adrs/ADR-0003-canonical-layer-names.md` | `Arthur` | `design` | `accepted` | `accepted by operator clarification and document refresh` | `2026-05-21` | `that file` | `canonical internal layer names or their repo mapping change` | `AUDIT-001` | `REQ-001; SPEC-001; ARCH-001` | `STORY-001B; STORY-001D` |
| `POL-001` | `artifact-refresh-policy` | `.aries_harness/references/ARTIFACT-REFRESH-POLICY.md` | `Arthur` | `governance` | `active` | `initialized` | `2026-05-21` | `that file` | `artifact handling rules change` | `AUDIT-001` | `REQ-001; SPEC-001; STORY-001; ARCH-001` | `REG-001; TRACE-001` |
| `TRACE-001` | `value-traceability-matrix` | `.aries_harness/references/VALUE-TRACEABILITY-MATRIX.md` | `Arthur` | `governance` | `active` | `initialized` | `2026-05-21` | `that file` | `artifact links or delivery evidence changes` | `AUDIT-001` | `REQ-001; SPEC-001; STORY-001; ARCH-001` | `future runs and history` |
| `AUDIT-001` | `artifact-audit-log` | `.aries_harness/references/ARTIFACT-AUDIT-LOG.md` | `Arthur` | `governance` | `active` | `initialized` | `2026-05-21` | `that file` | `meaningful artifact change occurs` | `n/a` | `REG-001` | `future review and history` |
| `REVIEW-001` | `harness-audit` | `.aries_harness/references/reviews/REVIEW-001-skill-layer-structure.md` | `Arthur` | `review` | `active` | `reviewed and partially remediated` | `2026-05-21` | `that file` | `after the next structure or operability-hardening pass` | `TRACE-001; AUDIT-001` | `REQ-001; SPEC-001; ARCH-001` | `STORY-001C` |
