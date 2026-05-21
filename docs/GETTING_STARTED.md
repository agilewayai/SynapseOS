# Getting Started With SynapseOS

This guide shows how to load SynapseOS manually and how to use the local `synapse-cli` initialization baseline. It is written for AI coding agents, maintainers, and integrators who want to use the skill stack from a local checkout.

## 1. Clone Or Open The Repository

```sh
git clone git@github.com:agilewayai/SynapseOS.git
cd SynapseOS
```

If you are already inside this workspace, the current local path is:

```text
/home/ubuntu/work/harenss/Skills/Cogna
```

## 2. Know The Entry Points

| Need | Load |
| --- | --- |
| Universal project context | `AGENTS.md` |
| Core reasoning kernel | `xuan-master/SKILL.md` |
| Full model catalog and scene routing | `xuan-master/00-entry/SKILL.md` |
| Problem calibration and orchestration | `archon/SKILL.md` |
| Domain-specialist routing | `prism/SKILL.md` |
| Initialization and host install | `init/SKILL.md` and `./synapse-cli` |
| OpenClaw-specific install | `docs/OPENCLAW_INSTALL.md` |
| Hermes-specific install | `docs/HERMES_INSTALL.md` |
| Corpus maintenance and recovery | `optimization/SKILL.md` |
| Project recovery and active plans | `.aries_harness/STATE.md` and `.aries_harness/TASK_STACK.md` |

## 3. Load The Core In Ten Minutes

Read these files in order:

```text
xuan-master/SKILL.md
xuan-master/00-entry/SKILL.md
xuan-master/001-layered-architecture/SKILL.md
xuan-master/007-iterative-thinking/SKILL.md
xuan-master/019-meta-cognition/SKILL.md
```

This gives you the base architecture model, the iteration model, and the meta-cognition model that anchors the rest of the system.

## 4. Use The Layered Workflow

For a simple reasoning task:

```text
AGENTS.md -> xuan-master/00-entry/SKILL.md -> selected model SKILL.md files
```

For an ambiguous or complex task:

```text
AGENTS.md -> archon/SKILL.md -> archon/interview/SKILL.md -> archon/enabled/SKILL.md -> selected xuan-master models
```

For domain-specialized work:

```text
AGENTS.md -> prism/SKILL.md -> relevant domain notes or domain package -> selected xuan-master and archon surfaces
```

## 5. Run The Initialization CLI

Check local readiness:

```sh
./synapse-cli doctor --json
```

Create repo-local initialization metadata:

```sh
./synapse-cli init --json
```

List supported agent host adapters:

```sh
./synapse-cli list-agents --json
```

Plan a generic installation without writing files:

```sh
./synapse-cli install --agent generic --target /path/to/host --dry-run --json
```

Apply and verify the generic installation after reviewing the plan:

```sh
./synapse-cli install --agent generic --target /path/to/host --yes --json
./synapse-cli verify --agent generic --target /path/to/host --json
```

The first implementation is local-only and standard-library based. Automatic system package installation is intentionally not implemented; `doctor` reports remediation hints and external writes require explicit `--yes`.

## 6. Integrate With An Agent Host

Use manual context loading or the `synapse-cli` baseline depending on your host:

| Host | Practical setup today |
| --- | --- |
| Claude Code | Add the repository to your project and point project instructions at `AGENTS.md` |
| Codex | Work from the repo root so `AGENTS.md` and layer files are available as local context |
| Cursor | Reference `AGENTS.md` and selected `SKILL.md` files from Cursor rules or project context |
| OpenCode | Register or load the relevant layer files through OpenCode's local context mechanism |
| OpenClaw | Paste the prompt from `docs/OPENCLAW_INSTALL.md` into OpenClaw chat, or use the local commands, then verify with `openclaw skills check --json` |
| Hermes | Install `docs/HERMES_INSTALL.md`'s direct-link installer skill, or use the local commands, then verify with `hermes skills list` |
| Other hosts | Use `./synapse-cli install --agent generic --target <path>` or read the relevant local `SKILL.md` files directly |

## 7. Track Installer Design

The implemented command surface is:

```sh
./synapse-cli doctor
./synapse-cli init
./synapse-cli list-agents
./synapse-cli install --agent <agent> --dry-run
./synapse-cli install --agent generic --target <path> --yes
./synapse-cli verify --agent <agent>
```

The design requires dry-run support, explicit approval for external writes, host-specific adapters, and a generic adapter for non-listed hosts.

Read the governing artifacts:

```text
.aries_harness/references/requests/REQ-002-synapseos-initialization-layer.md
.aries_harness/references/specs/SPEC-002-synapseos-initialization-layer.md
.aries_harness/references/stories/STORY-002-initialization-layer-pack.md
.aries_harness/references/domain/DOM-002-synapseos-initialization-domain.md
.aries_harness/decisions/architecture/ARCH-002-synapseos-initialization-layer.md
.aries_harness/decisions/adrs/ADR-0004-synapseos-initialization-layer.md
.aries_harness/references/specs/SPEC-003-openclaw-quick-install.md
.aries_harness/references/specs/SPEC-004-hermes-chat-install.md
```

## 8. Resume Project Work

When continuing development, start here:

```text
.aries_harness/STATE.md
.aries_harness/TASK_STACK.md
.aries_harness/MEMORY.md
```

These files describe the current state, next safe actions, and durable project facts. The recommended next implementation work is host-specific hardening beyond the baseline local installer.

## 9. License

SynapseOS is licensed under the Apache License, Version 2.0. See `LICENSE`.
