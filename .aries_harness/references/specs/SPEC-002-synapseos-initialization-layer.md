# Spec Package

## Document Control

- Spec ID: `SPEC-002`
- Artifact type: `spec`
- Objective mode: `functional_capability`
- Title: `SynapseOS initialization layer and synapse-cli installation contract`
- Status: `active`
- Owner: `Arthur`
- Parent request: `REQ-002`
- Child refs: `STORY-002`, `ARCH-002`, `ADR-0004`, `DOM-002`, `TRACE-001`
- Last reviewed: `2026-05-21`
- Source of truth: `this file`

## Belongs Here

- Objective: define what must be true for a dedicated SynapseOS initialization layer that can check prerequisites, initialize local state, install SynapseOS into agent hosts, and verify the result through a `synapse-cli` interface
- In scope:
  - a dedicated initialization layer for installation and first-run setup
  - prerequisite runtime detection and optional install planning
  - host adapters for `claude-code`, `codex`, `cursor`, `opencode`, `openclaw`, `hermes`, and `generic`
  - a `synapse-cli` command contract for diagnosis, initialization, installation, listing, verification, and dry-run planning
  - manifest and evidence outputs that make installer actions auditable
  - repo-local verification rules for the first implementation slice
- Out of scope:
  - implementing the CLI during this spec pass
  - publishing external packages
  - guaranteeing every third-party host's future path conventions before implementation verification
  - changing the content model of existing skills
  - cloud deployment, remote sync, or production operations
- Primary actors:
  - human maintainer installing SynapseOS locally
  - AI coding agent setting up its own host integration under operator control
  - downstream integrator installing SynapseOS into a non-standard agent host
  - future release operator packaging the installer
- Key flows:
  - operator runs `synapse-cli doctor` to inspect shell, Git, filesystem permissions, required runtimes, and detectable agent hosts
  - operator runs `synapse-cli init` to create or refresh local SynapseOS initialization state
  - operator runs `synapse-cli list-agents` to see supported and detected host adapters
  - operator runs `synapse-cli install --agent <agent>` to plan and apply installation for one named host
  - operator runs `synapse-cli install --agent generic --target <path>` to install into an explicit non-standard host directory
  - operator runs `synapse-cli install --agent <agent> --dry-run` to preview file writes, symlinks, copies, and host config changes
  - operator runs `synapse-cli verify --agent <agent>` to confirm the target host can see expected SynapseOS entrypoints
- Acceptance conditions:
  - `synapse-cli` exposes at least `doctor`, `init`, `list-agents`, `install`, and `verify`
  - every command supports a machine-readable output mode before release, such as `--json`
  - installer execution is idempotent: re-running the same install does not duplicate content or corrupt existing host config
  - `install` supports `--dry-run` and reports planned external writes before applying them
  - prerequisite installation is never implicit; actions that install system packages or third-party tools require explicit operator approval or a documented `--yes` mode
  - each named host adapter owns host-specific detection, target resolution, install planning, and verification logic
  - the generic adapter supports explicit `--target <path>` installation without host-specific assumptions
  - verification confirms at least the expected layer entrypoints are present: `synapse-cli`, `xuan-master`, `archon`, `prism`, and initialization docs or metadata
  - installation produces a manifest or equivalent evidence record that can be inspected after the run
  - failures produce actionable diagnostics instead of partial silent success
- NFRs:
  - portable across common developer shells and repo-local execution
  - safe by default for filesystem writes outside the repository
  - clear enough for AI agents to use without relying on hidden chat context
  - deterministic dry-run output for review
  - minimal coupling between host adapters
  - no network dependency for the basic local install path unless a future slice explicitly adds one
- Regression guardrails:
  - do not move canonical product truth out of Markdown skill files
  - do not hardcode host paths without an adapter-level detection and override strategy
  - do not silently mutate user configuration files
  - do not make a named host adapter required for generic installation
  - do not couple installer implementation to only one agent ecosystem
- Touched surfaces expected in implementation:
  - initialization layer surface: `init/`
  - `synapse-cli` entrypoint
  - host adapter modules under `init/synapse_cli/`
  - `.aries_harness/` implementation evidence
  - user-facing install docs
- Operational concerns:
  - host path conventions may change and must be verified during implementation
  - some targets may prefer symlink installs while others need file copies
  - permissions can vary across machines and agent sandboxes
  - install verification may need host-specific smoke checks where available

## CLI Contract

| Command | Required purpose | Required safety behavior |
| --- | --- | --- |
| `synapse-cli doctor` | Detect prerequisites, runtime readiness, permissions, and known agent hosts | Read-only by default |
| `synapse-cli init` | Create or refresh SynapseOS local initialization metadata | Idempotent and repo-local unless flags say otherwise |
| `synapse-cli list-agents` | List supported adapters and detected host availability | Read-only |
| `synapse-cli install --agent <agent>` | Install SynapseOS into one host adapter target | Supports `--dry-run`; external writes are explicit |
| `synapse-cli install --agent generic --target <path>` | Install into an explicit non-standard host directory | Requires explicit target path |
| `synapse-cli verify --agent <agent>` | Confirm installed files and entrypoints are visible to the host target | Read-only except optional evidence output |

## Slice Candidates

| Slice ID | User value | Acceptance anchor | Priority | Notes |
| --- | --- | --- | --- | --- |
| `STORY-002A` | Maintainers get an auditable initialization-layer design package | `REQ-002`, `SPEC-002`, `STORY-002`, `ARCH-002`, and `ADR-0004` exist and cross-link | `now` | This pass |
| `STORY-002B` | Operators get a runnable `synapse-cli` skeleton | CLI exposes command parser, help, `doctor`, `list-agents`, and `--json` basics | `next` | First coding slice |
| `STORY-002C` | Operators can see prerequisite readiness before install | `doctor` reports required, optional, missing, and installable prerequisites | `next` | Must remain read-only by default |
| `STORY-002D` | Agent users can install into named hosts | Host adapters exist for `claude-code`, `codex`, `cursor`, `opencode`, `openclaw`, and `hermes` | `later` | Implement incrementally by adapter |
| `STORY-002E` | Integrators can install into other agent hosts | Generic adapter supports explicit target path and manifest output | `later` | Keeps non-standard hosts first-class |
| `STORY-002F` | Maintainers can trust install results | `verify` checks installed entrypoints and reports drift | `later` | Add smoke checks where host tooling permits |

## Keep Out

- Exact host adapter implementation details
- Long release plan
- Packaging registry instructions
- User support matrix beyond the named target hosts

## Design Implications

- Domain implications: likely domain concepts are `installation_layer`, `runtime_prerequisite`, `agent_host_adapter`, `install_plan`, `install_manifest`, `verification_report`, and `generic_host_target`
- Architecture implications: SynapseOS needs an initialization layer that sits outside the cognition/execution/specialist stack and prepares those layers for host consumption
- Expected ADRs: `ADR-0004`

## Linked Artifacts

- Request brief: `.aries_harness/references/requests/REQ-002-synapseos-initialization-layer.md`
- Story-slice pack: `.aries_harness/references/stories/STORY-002-initialization-layer-pack.md`
- Domain package: `.aries_harness/references/domain/DOM-002-synapseos-initialization-domain.md`
- Architecture design pack: `.aries_harness/decisions/architecture/ARCH-002-synapseos-initialization-layer.md`
- Traceability matrix: `.aries_harness/references/VALUE-TRACEABILITY-MATRIX.md`

## Open Questions And Risks

- Resolved: the physical initialization layer is `init/`, with `synapse-cli` as the repo-local executable entrypoint
- Resolved: host installs support selectable `copy` and `symlink` strategies, with `copy` as the safe default
- Risk: exact install paths and host conventions can drift across agent versions
- Risk: prerequisite installation can become too invasive unless approval and dry-run rules stay strict
- Refresh trigger: any change to supported hosts, CLI commands, prerequisite policy, or installer write behavior
- Audit log entry: `AUDIT-001`
