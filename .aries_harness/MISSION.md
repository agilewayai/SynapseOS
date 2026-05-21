# Mission

## Artifact Header

- artifact id: `aries-mission-synapseos`
- artifact type: `mission`
- status: `active`
- owner: `Arthur`
- canonical path: `.aries_harness/MISSION.md`
- source of truth: `this file`
- upstream links: `AGENTS.md`, `xuan-master/00-entry/SKILL.md`
- downstream links: `TASK_STACK.md`, `STATE.md`, `EVAL.md`, `RUNBOOK.md`
- verification state: `initialized`
- last reviewed: `2026-05-21`
- next review or refresh trigger: `when project positioning, scope, or operating model changes`
- run id: `pending`
- task id or slice id: `bootstrap`
- checkpoint id: `n/a`
- approval request id: `n/a`
- trace id: `pending`
- eval report id: `pending`
- audit log id: `pending`

## Outcome

Maintain a reusable, agent-agnostic skills stack inside the `SynapseOS` repository with:

- `Xuan Master` as the meta-cognition core
- `Archon` as the enabler layer for orchestration and actions
- `Prism` as the specialist layer for deeper domain routing and mapping

## Scope

- Keep the 27-model knowledge base under `xuan-master/` coherent, navigable, and publishable
- Maintain execution-layer assets such as `enabled/`, `interview/`, and `optimization/`
- Improve repository structure, documentation quality, automation, and release readiness
- Preserve compatibility across coding-agent environments

## Constraints

- The repository is documentation-heavy and should stay easy to inspect without special tooling
- Changes should preserve agent-agnostic usage unless a compatibility break is explicitly chosen
- Harness docs must stay concise enough for rapid recovery by another operator

## Non-Goals

- Building an unrelated end-user application inside this repository
- Treating generated history as the source of truth
- Expanding the harness into deployment or rollout policy before the repo needs it

## Done Condition

Another operator should be able to open `.aries_harness/`, identify the repo objective, current priorities, current risks, and the next safe action without replaying prior chat.
