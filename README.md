# SynapseOS

SynapseOS is an agent-agnostic cognitive skills stack for AI coding agents and LLM hosts. It packages a 27-model reasoning kernel, an execution and generation layer, a specialist routing layer, and a governed harness surface so agents can load reusable reasoning frameworks instead of relying on one-off prompt memory.

The repository is documentation-first. The primary runtime contract is a set of `SKILL.md` files that can be read directly by Codex, Claude Code, Cursor, OpenCode, OpenClaw, Hermes, or any other agent host that can load local Markdown context.

## What It Includes

| Layer | Path | Purpose |
| --- | --- | --- |
| Xuan Master | `xuan-master/` | Meta-cognition core with 27 cognitive models and scene routing |
| Archon | `archon/` | Enabler layer for problem calibration, orchestration, actions, document generation, and synthesis |
| Prism | `prism/` | Specialist layer for mapping work into deeper domain-specific paths |
| Optimization | `optimization/` | Cross-cutting audit, recovery, and corpus improvement guidance |
| Aries Harness | `.aries_harness/` | Project-local governance, recovery, request/spec/story/architecture, and traceability artifacts |

The next planned product layer is the SynapseOS initialization layer, specified in `.aries_harness/references/specs/SPEC-002-synapseos-initialization-layer.md`. It defines the future `synapse-cli` interface for prerequisite diagnosis, local initialization, agent-host installation, and verification.

## Repository Layout

```text
.
├── AGENTS.md
├── README.md
├── docs/
│   └── GETTING_STARTED.md
├── xuan-master/
│   ├── SKILL.md
│   ├── 00-entry/
│   └── 001-layered-architecture/ ... 027-ai-native-mindset/
├── archon/
│   ├── SKILL.md
│   ├── interview/
│   └── enabled/
├── prism/
│   ├── SKILL.md
│   └── domains/
├── optimization/
├── .aries_harness/
└── LICENSE
```

## Quick Start

Start with the core entrypoint:

```text
xuan-master/SKILL.md
```

For most analysis tasks, load the model catalog next:

```text
xuan-master/00-entry/SKILL.md
```

For ambiguous requests or tasks that need orchestration, load Archon:

```text
archon/SKILL.md
```

For specialist routing, load Prism:

```text
prism/SKILL.md
```

For a practical walkthrough, see [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md).

## Agent Host Integration

SynapseOS is intentionally host-neutral. Until `synapse-cli` is implemented, install it by cloning the repository and pointing your agent host at the relevant local entrypoints.

| Host | Recommended entrypoint |
| --- | --- |
| Claude Code | Add this repository path and load `AGENTS.md` or `xuan-master/SKILL.md` as project context |
| Codex | Use `AGENTS.md` as the project instruction surface and load layer `SKILL.md` files as needed |
| Cursor | Reference `AGENTS.md` or selected layer files from project rules |
| OpenCode / OpenClaw / Hermes | Load the layer `SKILL.md` files through the host's local skill or context mechanism |
| Generic LLM host | Read `AGENTS.md`, then load specific layer and model files directly |

Future installation work is tracked under:

```text
.aries_harness/references/stories/STORY-002-initialization-layer-pack.md
```

## Working With The Harness

The `.aries_harness/` directory is the recovery and governance surface for the repository. It records:

| Artifact | Purpose |
| --- | --- |
| `MISSION.md` | Current repository mission and scope |
| `STATE.md` | Current project state and next safe action |
| `TASK_STACK.md` | Ready, active, later, and completed work |
| `ADR.md` | Decision index |
| `references/` | Request, spec, story, traceability, audit, and review artifacts |
| `decisions/` | Architecture packs and detailed ADR records |

Use these files when you need to resume work without replaying prior chat.

## Current Status

The repository currently provides:

- 27 cognitive model skills under `xuan-master/`
- A nested Archon enabler layer under `archon/`
- A Prism specialist layer scaffold
- Aries Harness artifacts for architecture, traceability, and future initialization work
- A planned, not-yet-implemented `synapse-cli` installation interface

## License

SynapseOS is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE).
