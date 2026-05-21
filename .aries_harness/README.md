# Aries Harness

This directory is the project-local recovery surface for the `SynapseOS` repository at `git@github.com:agilewayai/SynapseOS.git`.

It exists to keep the current objective, operating state, risks, and durable memory inspectable without replaying chat history.

## Base Loop

- Inspect
- Plan
- Edit
- Verify
- Summarize

## Canonical Root Docs

- `MISSION.md`: project target, scope, constraints, and done condition
- `TASK_STACK.md`: active and upcoming work slices
- `STATE.md`: current phase and working status
- `JOURNAL.md`: dated operator notes
- `EVAL.md`: acceptance and verification status
- `RISKS.md`: active risks and mitigations
- `MEMORY.md`: hot working memory
- `ADR.md`: architectural and workflow decisions
- `RUNBOOK.md`: operating playbook
- `INDEX.md`: directory map and refresh rules

## Memory Split

- `MEMORY.md` is the hot snapshot
- `memory/INDEX.md` is the cold recall map
- `memory/cards/` stores detailed durable memory entries

## Directory Policy

- Keep root files high-signal
- Put overflow notes under the managed subdirectories
- Treat `history/` as a projection surface, not a source of truth
