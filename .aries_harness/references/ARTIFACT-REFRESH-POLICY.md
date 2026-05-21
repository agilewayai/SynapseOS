# Artifact Refresh Policy

## Document Control

- Artifact ID: `POL-001`
- Artifact type: `artifact-refresh-policy`
- Status: `active`
- Owner: `Arthur`
- Last reviewed: `2026-05-21`
- Source of truth: `this file`

## Purpose

Keep request, spec, story, architecture, and ADR artifacts aligned as the repository evolves.

## Same-Pass Update Rules

- If `REQ-001` changes, refresh `SPEC-001`, impacted story rows in `STORY-001`, `TRACE-001`, `REG-001`, and `AUDIT-001` in the same pass
- If `SPEC-001` changes, refresh impacted story details, `ARCH-001` if boundaries or quality attributes moved, then update `TRACE-001`, `REG-001`, and `AUDIT-001`
- If a story status or scope changes, refresh `STORY-001`, `TRACE-001`, `REG-001`, and `AUDIT-001`
- If architecture boundaries, layer names, layer mapping, or helper-script responsibilities change, refresh `ARCH-001`, any impacted ADR, then update `SPEC-001`, `TRACE-001`, `REG-001`, and `AUDIT-001`
- If an ADR meaning changes, update `ADR.md` and any affected request/spec/story/architecture links in the same pass

## Artifact-Specific Triggers

| Artifact | Refresh when | Minimum linked updates |
| --- | --- | --- |
| `REQ-001` | project identity, internal layer naming, product framing, or scope boundary changes | `SPEC-001`, `STORY-001`, `TRACE-001`, `REG-001`, `AUDIT-001` |
| `SPEC-001` | layer contract, layer naming, model count, primary actors, or quality rules change | `STORY-001`, `ARCH-001`, `TRACE-001`, `REG-001`, `AUDIT-001` |
| `STORY-001` | current or next slice changes status or scope | `TRACE-001`, `REG-001`, `AUDIT-001` |
| `ARCH-001` | layer boundaries, canonical layer names, script roles, or governance overlay meaning changes | `ADR-0002`, `ADR-0003`, `SPEC-001`, `TRACE-001`, `REG-001`, `AUDIT-001` |
| `ADR-0003` | the internal layer names or their repo mapping changes materially | `ADR.md`, `ARCH-001`, `SPEC-001`, `TRACE-001`, `REG-001`, `AUDIT-001` |
| `ADR-0002` | the accepted architectural rule changes materially | `ADR.md`, `ARCH-001`, `TRACE-001`, `REG-001`, `AUDIT-001` |
| `REVIEW-001` | review findings close, reopen, or gain new evidence | `TASK_STACK.md`, `REG-001`, `AUDIT-001` |
| `TRACE-001` | artifact links or delivery evidence changes | `REG-001`, `AUDIT-001` |
| `REG-001` | any artifact is added, retired, or materially re-scoped | `AUDIT-001` |

## Source-Of-Truth Rules

- `history/` and `runs/` are evidence or projections, not the canonical product/design source
- `AGENTS.md`, `00-entry/SKILL.md`, and the layer directories remain the primary product corpus
- `.aries_harness/` design artifacts describe and govern that corpus; they do not replace it

## Review Cadence

- Review the artifact set after any substantial repository-structure change
- Review again before broader publication or packaging work
- If a task changes only wording and not meaning, update the relevant artifact only if traceability would otherwise become misleading
