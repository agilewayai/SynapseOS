# Index

## Root Docs

- `README.md`: harness purpose and navigation
- `MISSION.md`: current mission and boundaries
- `TASK_STACK.md`: prioritized work stack
- `STATE.md`: current execution state
- `JOURNAL.md`: chronological working notes
- `EVAL.md`: verification and acceptance surface
- `RISKS.md`: active risk register
- `MEMORY.md`: hot memory snapshot
- `ADR.md`: decision register
- `RUNBOOK.md`: operating checklist

## Managed Directories

- `history/`: generated status and development history projections
- `memory/`: cold recall index and durable memory cards
- `checkpoints/`: resumable checkpoint notes
- `decisions/`: expanded decision records when root `ADR.md` is no longer enough
- `runs/`: per-run evidence and traces
- `references/`: supporting notes that are not canonical state
- `archive/`: retired or superseded harness artifacts

## Living Design Artifacts

- `references/requests/`: canonical request briefs
- `references/specs/`: canonical spec packages
- `references/stories/`: story-slice packs
- `references/domain/`: domain packages when extracted
- `references/reviews/`: review and audit memos
- `references/ARTIFACT-REGISTER.md`: active artifact inventory
- `references/VALUE-TRACEABILITY-MATRIX.md`: request-to-delivery links
- `references/ARTIFACT-REFRESH-POLICY.md`: same-pass refresh rules
- `references/ARTIFACT-AUDIT-LOG.md`: meaningful artifact changes
- `decisions/architecture/`: architecture design packs
- `decisions/adrs/`: detailed ADR records

## Refresh Rules

- Update `MISSION.md` when the repo purpose or scope changes
- Update `TASK_STACK.md` when slices start, finish, or get reprioritized
- Update `STATE.md` at the start and end of substantial work
- Keep `MEMORY.md` concise; promote detailed facts into `memory/cards/`
- Refresh this index if new managed artifacts become permanent
