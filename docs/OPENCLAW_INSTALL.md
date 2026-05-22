# OpenClaw Installation Guide For SynapseOS

This guide installs SynapseOS as an OpenClaw skill stack and then verifies both the SynapseOS payload and OpenClaw's native skill view.

## What Gets Installed

SynapseOS is a grouped multi-skill stack:

- `xuan-master`: 27-model cognition core
- `archon`: calibration, orchestration, actions, and generation layer
- `prism`: specialist routing layer
- `init`: setup, installation, and verification layer

The default OpenClaw skill root is:

```text
~/.openclaw/skills/
```

SynapseOS keeps a managed payload copy here:

```text
~/.openclaw/skills/synapseos/
```

For OpenClaw-native discovery, the installer also writes direct skill entries at the skill root:

```text
~/.openclaw/skills/xuan-master/SKILL.md      name: xuan_master
~/.openclaw/skills/archon/SKILL.md           name: archon
~/.openclaw/skills/prism/SKILL.md            name: prism
~/.openclaw/skills/init/SKILL.md             name: synapse_init
~/.openclaw/skills/optimization/SKILL.md     name: optimization
```

This keeps the full SynapseOS payload grouped for updates while giving `openclaw skills list` direct child skill directories to enumerate.

## Prerequisites

Install and verify OpenClaw first:

```sh
openclaw --version
openclaw doctor
```

You also need:

- Git available on `PATH`
- Python 3.8 or newer for `synapse-cli`
- Write access to the OpenClaw skill target

Check SynapseOS readiness from the SynapseOS checkout:

```sh
./synapse-cli doctor --json
```

## Chatbox Install Mode

Use this when you want OpenClaw to finish the install from its channel chatbox.

Paste this into OpenClaw:

```text
Install the SynapseOS skills family for OpenClaw from this installation prompt:
https://raw.githubusercontent.com/agilewayai/SynapseOS/main/install/openclaw-chat-install.md

Follow the prompt exactly. Show me the target directory and dry-run plan first, then complete the install and verification if the plan is safe.
```

OpenClaw should then:

- clone or update SynapseOS from GitHub
- run `./synapse-cli doctor --json`
- show `./synapse-cli install --agent openclaw --dry-run --json`
- apply `./synapse-cli install --agent openclaw --yes --json` when the plan is safe
- run `./synapse-cli verify --agent openclaw --json`
- run `openclaw skills check --json` and `openclaw skills list --json`
- confirm `openclaw skills list --json` includes `xuan_master`, `archon`, `prism`, `synapse_init`, and `optimization`
- explain how to start using `Xuan Master`, `Archon`, `Prism`, and `Init`

The prompt source lives in this repository at `install/openclaw-chat-install.md`.

## Recommended Safe Install

From a local SynapseOS checkout:

```sh
./synapse-cli install --agent openclaw --dry-run --json
```

Review the planned destination and install state. A fresh install reports `install_mode: install`. A previous install reports `install_mode: update`. The plan also reports `payload_version` and `previous_installation.payload.version_status` so an older installed payload is visible before applying the refresh.

If the dry-run reports `previous_installation.status: legacy_grouped_only`, the installer found the old OpenClaw layout where only `~/.openclaw/skills/synapseos` exists. This is an expected safe update path when the payload markers are present and no direct skill conflicts are reported.

If the plan is correct:

```sh
./synapse-cli install --agent openclaw --yes --json
```

Verify the SynapseOS payload and manifest:

```sh
./synapse-cli verify --agent openclaw --json
```

Verify OpenClaw's native skill view:

```sh
openclaw skills check --json
openclaw skills list --json
```

If OpenClaw reports `xuan_master`, `archon`, `prism`, `synapse_init`, and `optimization`, start a new OpenClaw session or reload the host if your setup requires it.

OpenClaw's current skill metadata docs define `name` as a required identifier, so the direct OpenClaw entries use OpenClaw-safe names such as `xuan_master` and `synapse_init`. Treat `openclaw skills check --json` as the authority on whether the installed SynapseOS skill metadata is accepted by your OpenClaw version.

## Custom Target

Use `--target` when your OpenClaw skills directory is not `~/.openclaw/skills`:

```sh
./synapse-cli install --agent openclaw --target /path/to/openclaw/skills --dry-run --json
./synapse-cli install --agent openclaw --target /path/to/openclaw/skills --yes --json
./synapse-cli verify --agent openclaw --target /path/to/openclaw/skills --json
```

The final install root is:

```text
/path/to/openclaw/skills/synapseos
```

The native OpenClaw skill entries are written beside it:

```text
/path/to/openclaw/skills/xuan-master
/path/to/openclaw/skills/archon
/path/to/openclaw/skills/prism
/path/to/openclaw/skills/init
/path/to/openclaw/skills/optimization
```

## Shell One-Link Target UX

The optional future shell quick-install command is:

```sh
curl -fsSL https://raw.githubusercontent.com/agilewayai/SynapseOS/main/install/openclaw.sh | bash
```

That shell script is specified but not implemented in the current baseline. Use the chatbox install mode or safe local install path above. Before the shell script is promoted, it must:

- support `--dry-run`
- show the resolved OpenClaw target before writing
- refuse to overwrite a non-SynapseOS folder unless `--force` is explicit
- support `--target <path>`
- install the managed SynapseOS payload plus direct OpenClaw skill entries
- run `synapse-cli verify --agent openclaw`
- run `openclaw skills check --json` when OpenClaw is available
- print the first-use learning prompt below

Use the safe local install path above or the chatbox install mode until the shell one-link script exists and has been reviewed.

## Quick Learning Prompt

After installation, ask OpenClaw:

```text
Use xuan_master. Explain when I should use Xuan Master, Archon, Prism, and Init, then recommend the first SynapseOS skill for my current task.
```

For architecture or reasoning tasks, start with:

```text
Use xuan_master to choose the right cognitive model pipeline for this problem.
```

For ambiguous requests or tasks that need orchestration:

```text
Use archon to clarify the request, plan the workflow, and route to the right SynapseOS layer.
```

For domain-specialized work:

```text
Use prism to map this work into the right specialist domain path.
```

## Update

From a SynapseOS checkout:

```sh
git pull
./synapse-cli install --agent openclaw --dry-run --json
./synapse-cli install --agent openclaw --yes --json
./synapse-cli verify --agent openclaw --json
openclaw skills check --json
openclaw skills list --json
```

For an old grouped-only install, the dry-run should show:

```text
install_mode: update
previous_installation.status: legacy_grouped_only
previous_installation.update_required: true
```

The approved update keeps the managed payload at `~/.openclaw/skills/synapseos` and adds the direct native entries beside it.

## Troubleshooting

### `openclaw: command not found`

Install OpenClaw and verify it with:

```sh
openclaw --version
openclaw doctor
```

### `synapse-cli verify` fails

Check the `checks` array in the JSON output. Missing files usually mean the install target is not the same target used for verification.

### `openclaw skills check` fails but `synapse-cli verify` passes

SynapseOS files are present, but OpenClaw does not accept or load them. Check:

- the OpenClaw skills root you installed into
- OpenClaw skill allowlist or configuration rules
- whether OpenClaw needs a restart or new session
- whether any `SKILL.md` frontmatter errors are reported

If the grouped payload exists under `~/.openclaw/skills/synapseos` but `openclaw skills list --json` does not show the SynapseOS layer skills, check that these direct entries exist:

```text
~/.openclaw/skills/xuan-master/SKILL.md
~/.openclaw/skills/archon/SKILL.md
~/.openclaw/skills/prism/SKILL.md
~/.openclaw/skills/init/SKILL.md
~/.openclaw/skills/optimization/SKILL.md
```

If a direct entry already exists and is not a SynapseOS skill, the installer blocks instead of overwriting it. Move or rename the conflicting directory, then rerun the dry-run before applying the install.

### Old OpenClaw Layout Detected

Older SynapseOS OpenClaw installs may have only this grouped payload:

```text
~/.openclaw/skills/synapseos
```

Rerun the current installer. The dry-run should report `previous_installation.status: legacy_grouped_only` and `install_mode: update`, then the approved install writes the missing direct OpenClaw entries.

If the dry-run reports `conflict_existing_payload`, the existing `synapseos` directory does not look like a SynapseOS payload. Inspect or move it before rerunning the installer.

### Target Already Exists

The safe path is to review before overwriting:

```sh
./synapse-cli install --agent openclaw --dry-run --json
```

If you maintain your own modified local copy, prefer a symlink strategy or a custom target:

```sh
./synapse-cli install --agent openclaw --strategy symlink --target /path/to/openclaw/skills --dry-run --json
```

## Reference Artifacts

- Spec: `.aries_harness/references/specs/SPEC-003-openclaw-quick-install.md`
- Story pack: `.aries_harness/references/stories/STORY-003-openclaw-quick-install.md`
- Architecture: `.aries_harness/decisions/architecture/ARCH-003-openclaw-quick-install.md`
- ADR: `.aries_harness/decisions/adrs/ADR-0005-openclaw-quick-install.md`

## OpenClaw References

- OpenClaw install: `https://docs.openclaw.ai/install`
- OpenClaw skills: `https://docs.openclaw.ai/tools/skills`
- OpenClaw skills CLI: `https://docs.openclaw.ai/cli/skills`
- OpenClaw skills config: `https://docs.openclaw.ai/tools/skills-config`
