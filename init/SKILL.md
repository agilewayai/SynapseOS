---
name: synapse-init
description: "SynapseOS initialization layer. Use when checking local prerequisites, preparing initialization metadata, installing SynapseOS into agent hosts, or verifying host installation state through synapse-cli."
version: 0.1.0
author: Arthur
---

# SynapseOS Initialization Layer

This layer owns first-run setup and host installation for SynapseOS.

## Responsibilities

- Check local runtime prerequisites with `synapse-cli doctor`
- Initialize repo-local metadata with `synapse-cli init`
- List supported agent host adapters with `synapse-cli list-agents`
- Plan and apply host installation with `synapse-cli install`
- Verify installed entrypoints with `synapse-cli verify`

## Safety Rules

- `doctor`, `list-agents`, and `verify` are read-only by default.
- `install` supports `--dry-run` and requires `--yes` before applying writes.
- The `generic` adapter requires an explicit `--target`.
- External writes are represented as an install plan before execution.

## Supported Host Adapters

- `claude-code`
- `codex`
- `cursor`
- `opencode`
- `openclaw`
- `hermes`
- `generic`

## Primary CLI

```sh
./synapse-cli doctor
./synapse-cli init
./synapse-cli list-agents
./synapse-cli install --agent generic --target /path/to/host --dry-run
./synapse-cli install --agent generic --target /path/to/host --yes
./synapse-cli verify --agent generic --target /path/to/host
```
