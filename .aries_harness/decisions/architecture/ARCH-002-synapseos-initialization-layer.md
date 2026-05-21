# Architecture Design Pack

## Document Control

- Architecture ID: `ARCH-002`
- Artifact type: `architecture`
- Title: `SynapseOS initialization layer and synapse-cli installer architecture`
- Status: `active`
- Owner: `Arthur`
- Related request: `REQ-002`
- Related spec: `SPEC-002`
- Child refs: `ADR-0004`
- Last reviewed: `2026-05-21`
- Source of truth: `this file`

## Design Drivers

- Primary business outcome: make SynapseOS installable and verifiable across multiple agent hosts through a consistent local CLI
- Quality attributes:
  - idempotence
  - portability
  - diagnostic clarity
  - explicit operator control
  - adapter isolation
  - inspectable install evidence
- Constraints:
  - the skill corpus remains docs-first and independently loadable
  - host-specific behavior must be isolated behind adapters
  - external writes and prerequisite installation must be visible before execution
  - generic host installation must not require a named agent ecosystem

## Current And Target Shape

- Current state summary:
  - SynapseOS has a layered skill corpus with `Xuan Master`, `Archon`, and `Prism`
  - the repository has no dedicated initialization layer or `synapse-cli` contract yet
  - installation expectations are implicit and would be hard to verify across agent hosts
- Target state summary:
  - add a dedicated `Initialization Layer` responsible for first-run setup and host installation
  - expose setup behavior through `synapse-cli`
  - separate CLI command parsing, prerequisite diagnosis, install planning, host adapters, filesystem operations, and verification reporting
  - support named host adapters for `claude-code`, `codex`, `cursor`, `opencode`, `openclaw`, and `hermes`
  - support a generic adapter for any other agent host through an explicit target path
- Why the change is needed: without a first-class initialization layer, multi-agent adoption depends on fragile manual instructions and host-specific assumptions that are difficult to audit or repeat

## Boundaries

- Component or module boundaries:
  - `Initialization layer`: future repo surface for installation docs, host registry, prerequisite policy, and CLI behavior
  - `synapse-cli`: executable interface that exposes diagnosis, init, install, list, and verify commands
  - `Prerequisite checker`: read-only runtime inspection and optional install-plan generation
  - `Install planner`: builds an explicit plan of file operations and config changes before execution
  - `Host adapters`: one adapter per named host plus `generic`
  - `Install executor`: applies approved plans with idempotent writes
  - `Verification reporter`: checks installed entrypoints and writes evidence
- Integration boundaries:
  - initialization reads the SynapseOS repo as source content
  - initialization writes only to operator-approved host targets or repo-local metadata
  - host adapters resolve target paths and verification behavior for their own host
  - existing layers remain product payloads, not installer control logic
- Data boundaries:
  - source skills stay in the repository
  - install manifests and verification reports record what was applied
  - host configuration mutations must be planned and reported before write

## Proposed CLI Surface

| Command | Responsibility | Notes |
| --- | --- | --- |
| `synapse-cli doctor` | Inspect prerequisites, host availability, permissions, and runtime readiness | Read-only default |
| `synapse-cli init` | Create or refresh initialization metadata | Repo-local default |
| `synapse-cli list-agents` | Show supported adapters and detection status | Includes generic adapter |
| `synapse-cli install --agent <agent>` | Plan and apply install for a named host | Requires `--dry-run` support |
| `synapse-cli install --agent generic --target <path>` | Install into an explicit non-standard host path | Target path is mandatory |
| `synapse-cli verify --agent <agent>` | Verify installed entrypoints and manifest consistency | Read-only unless evidence output is requested |

## Agent Host Adapter Contract

Each adapter should provide:

- stable adapter id
- detection strategy
- target path resolution with override support
- install plan generation
- dry-run rendering
- apply behavior
- verification behavior
- uninstall or rollback notes, even if full uninstall is deferred

Supported adapter ids for the first design are:

- `claude-code`
- `codex`
- `cursor`
- `opencode`
- `openclaw`
- `hermes`
- `generic`

## Decisions

| Decision | Why | Tradeoff | Linked ADR |
| --- | --- | --- | --- |
| Add a dedicated initialization layer instead of embedding install behavior in `Archon` or `optimization` | Installation is a first-run host integration concern, not a reasoning or corpus-maintenance concern | Adds another layer to document and maintain | `ADR-0004` |
| Use `synapse-cli` as the installation interface | A stable command contract is easier for agents and operators to call consistently | Requires CLI packaging and validation work later | `ADR-0004` |
| Keep host behavior in adapters | Agent hosts differ in path conventions and config expectations | Adapter count grows as host support grows | `ADR-0004` |
| Require dry-run and explicit approval for external writes | Installation can affect user configuration and should be inspectable | Slightly more ceremony for first-time users | `ADR-0004` |
| Keep a generic adapter | Non-listed hosts should not be second-class users | Generic install cannot offer deep host-specific verification | `ADR-0004` |

## Delivery Impact

- Affected stories: `STORY-002A`, `STORY-002B`, `STORY-002C`, `STORY-002D`, `STORY-002E`, `STORY-002F`
- Verification impact: future implementation needs CLI parser checks, doctor output checks, dry-run snapshot checks, adapter-specific path planning tests, and local verification checks
- Rollout impact: implementation should start local-only; external package publishing is deferred
- Observability impact: install manifests and verification reports become the main evidence surfaces

## Risks And Open Questions

- Risk: host-specific path conventions can drift, so adapters must be easy to update
- Risk: automatic prerequisite installation can become too broad unless approval rules stay strict
- Risk: symlink versus copy behavior may need per-host selection
- Open question: choose the physical repo name for the initialization layer during the first coding slice
- Open question: decide whether `synapse-cli` should be a shell entrypoint, Python module entrypoint, Node package command, or a thin wrapper around a repo-local script
- Refresh trigger: any change to supported host ids, command names, prerequisite policy, adapter contract, or install evidence shape
- Audit log entry: `AUDIT-001`
