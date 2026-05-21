# Runbook

## Artifact Header

- artifact id: `aries-runbook-synapseos`
- artifact type: `runbook`
- status: `active`
- owner: `Arthur`
- canonical path: `.aries_harness/RUNBOOK.md`
- source of truth: `this file`
- upstream links: `MISSION.md`, `STATE.md`, `ADR.md`
- downstream links: `JOURNAL.md`, `checkpoints/README.md`, `runs/README.md`
- verification state: `initialized`
- last reviewed: `2026-05-21`
- next review or refresh trigger: `when the operating loop or repo workflow changes`
- run id: `pending`
- task id or slice id: `bootstrap`
- checkpoint id: `n/a`
- approval request id: `n/a`
- trace id: `pending`
- eval report id: `pending`
- audit log id: `pending`

## Execution Card

### Before Starting

- Target: maintain and improve the `SynapseOS` skills stack built from `Xuan Master`, `Archon`, and `Prism`
- Scope: repo-local docs, structure, scripts, and harness state
- Constraints: keep the repo inspectable, concise, and agent-agnostic
- Done condition: another operator can resume safely from `.aries_harness/`

### Before Acting

- Load `MISSION.md`, `TASK_STACK.md`, `STATE.md`, and `MEMORY.md`
- Identify the smallest safe change path
- Decide how the change will be verified

### During Execution

- Follow `Inspect -> Plan -> Edit -> Verify -> Summarize`
- Keep `STATE.md` current during longer tasks
- Leave a checkpoint note if a task spans sessions

### Before Closing

- Record what changed in `JOURNAL.md` when the change is substantial
- Update `EVAL.md` with what was verified
- Note any residual risk in `RISKS.md`

## Practical Rules

- Do not treat generated history as canonical state
- Keep `MEMORY.md` small and move durable details into `memory/cards/`
- Prefer updating existing source docs over scattering state into ad hoc notes
