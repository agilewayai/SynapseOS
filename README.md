# SynapseOS

SynapseOS is an agent-agnostic cognitive skills stack for AI coding agents and LLM hosts. It packages 27 reusable reasoning models plus execution, routing, and initialization layers that can be loaded by Codex, Claude Code, Cursor, OpenCode, Gemini, Antigravity, OpenClaw, Hermes, or any host that can read local Markdown context.

The main user contract is simple: load the relevant `SKILL.md` files as context, or install the stack into your agent host with `synapse-cli`.

## Quick Start

Start with the core reasoning layer:

```text
xuan-master/SKILL.md
```

For model selection and scenario routing, load the catalog:

```text
xuan-master/00-entry/SKILL.md
```

Use the other top-level layers when the task needs them:

| Need | Load |
| --- | --- |
| Core reasoning models and scene selection | `xuan-master/SKILL.md` |
| Calibration, orchestration, actions, document generation, synthesis | `archon/SKILL.md` |
| Specialist routing into deeper domain work | `prism/SKILL.md` |
| Setup, host installation, and verification | `init/SKILL.md` or `./synapse-cli` |

Example prompt after loading SynapseOS:

```text
Load SynapseOS. Explain when I should use Xuan Master, Archon, Prism, and Init, then recommend the first skill for my current task.
```

## Install

From a local checkout, inspect your environment first:

```sh
./synapse-cli doctor --json
./synapse-cli list-agents --json
```

Then run a dry-run for your target host:

```sh
./synapse-cli install --agent <agent> --dry-run --json
```

If the plan is correct, apply and verify:

```sh
./synapse-cli install --agent <agent> --yes --json
./synapse-cli verify --agent <agent> --json
```

Supported adapter ids:

```text
claude-code, codex, cursor, opencode, gemini, antigravity, antigravity-cli, openclaw, hermes, generic
```

Use `generic` for a custom or unknown host target:

```sh
./synapse-cli install --agent generic --target /path/to/host --dry-run --json
./synapse-cli install --agent generic --target /path/to/host --yes --json
./synapse-cli verify --agent generic --target /path/to/host --json
```

Repeat installs are treated as updates. Dry-run output reports `install_mode`, `payload_version`, and `previous_installation` so you can see whether the target is fresh, already installed, older than the current payload, or unsafe to overwrite. Existing unrecognized `synapseos/` directories are blocked instead of overwritten.

## Host Notes

| Host | Recommended setup |
| --- | --- |
| Claude Code | Use the `claude-code` adapter or load `AGENTS.md` / `xuan-master/SKILL.md` as project context |
| Codex | Use the `codex` adapter or work from this repo so `AGENTS.md` and layer files are available |
| Cursor | Use the `cursor` adapter or reference selected `SKILL.md` files from Cursor rules/context |
| OpenCode | Use the `opencode` adapter or load layer files through OpenCode context |
| Gemini | Use the `gemini` adapter for `~/.gemini/skills` or load layer files directly |
| Antigravity | Use `antigravity` for `~/.gemini/antigravity/skills` or `antigravity-cli` for `~/.gemini/antigravity-cli/skills` |
| OpenClaw | Use the OpenClaw guide or `./synapse-cli install --agent openclaw --dry-run --json` |
| Hermes | Use the Hermes guide or `./synapse-cli install --agent hermes --dry-run --json` |

OpenClaw and Hermes have dedicated guided install paths:

- [OpenClaw install guide](docs/OPENCLAW_INSTALL.md)
- [Hermes install guide](docs/HERMES_INSTALL.md)

## Use The Skills

For common tasks, start with these entrypoints:

| Task | Suggested layer |
| --- | --- |
| Architecture design | `xuan-master/001-layered-architecture/SKILL.md` plus `xuan-master/002-flow-model/SKILL.md` |
| Debugging or incident diagnosis | `xuan-master/003-state-machine/SKILL.md`, `xuan-master/005-reverse-thinking/SKILL.md`, `xuan-master/024-rice-diagnosis/SKILL.md` |
| Strategy or product decisions | `xuan-master/006-first-principles/SKILL.md`, `xuan-master/018-swot/SKILL.md`, `xuan-master/022-mckinsey-method/SKILL.md` |
| Code quality improvement | `xuan-master/011-feedback-loop/SKILL.md`, `xuan-master/007-iterative-thinking/SKILL.md`, `xuan-master/010-occams-razor/SKILL.md` |
| Long or ambiguous work | `archon/SKILL.md` first, then route into Xuan Master or Prism |

For the full walkthrough, see [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md).

## License

SynapseOS is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE).
