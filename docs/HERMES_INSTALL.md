# Hermes Installation Guide For SynapseOS

This guide installs SynapseOS as a Hermes Agent skills family and then verifies both the SynapseOS payload and Hermes' native skill view.

## What Gets Installed

SynapseOS is a grouped skills family:

- `xuan-master`: 27-model cognition core
- `archon`: calibration, orchestration, actions, and generation layer
- `prism`: specialist routing layer
- `init`: setup, installation, and verification layer

The default Hermes target is:

```text
~/.hermes/skills/synapseos/
```

Inside that group, Hermes receives layer folders such as:

```text
~/.hermes/skills/synapseos/xuan-master/SKILL.md
~/.hermes/skills/synapseos/archon/SKILL.md
~/.hermes/skills/synapseos/prism/SKILL.md
~/.hermes/skills/synapseos/init/SKILL.md
```

## Hermes Skill Requirements

Hermes skills are `SKILL.md` files with YAML frontmatter and Markdown instructions. The Hermes CLI can install a skill from a direct HTTP(S) URL to a `SKILL.md` file:

```sh
hermes skills install https://example.com/path/to/SKILL.md --name custom-name --yes
```

This guide uses that native path to bootstrap a small `synapseos-installer` Hermes skill. That installer skill then clones SynapseOS, runs `synapse-cli`, installs the full skill family, and verifies the result.

## Prerequisites

Install and verify Hermes first:

```sh
hermes --version
hermes skills list
```

You also need:

- Git available on `PATH`
- Python 3.8 or newer for `synapse-cli`
- Write access to the Hermes skills target

## Chatbox Install Mode

Use this when you want Hermes to finish the install from its channel chatbox.

Paste this into Hermes:

```text
Install this Hermes skill and use it to install the SynapseOS skills family:
https://raw.githubusercontent.com/agilewayai/SynapseOS/main/install/hermes-chat-install/SKILL.md

After installing it as synapseos-installer, run it. Show me the target directory and dry-run plan first, then complete the install and verification if the plan is safe.
```

If Hermes asks for an explicit command, use:

```text
/skills install https://raw.githubusercontent.com/agilewayai/SynapseOS/main/install/hermes-chat-install/SKILL.md --name synapseos-installer
```

Then run:

```text
/synapseos-installer install the SynapseOS skills family. Show the dry-run plan first, then install and verify if safe.
```

Hermes should then:

- install the `synapseos-installer` skill from the raw `SKILL.md` URL
- clone or update SynapseOS from GitHub
- run `./synapse-cli doctor --json`
- show `./synapse-cli install --agent hermes --dry-run --json`
- apply `./synapse-cli install --agent hermes --yes --json` when the plan is safe
- run `./synapse-cli verify --agent hermes --json`
- run `hermes skills list` and `hermes skills check`
- explain how to start using `Xuan Master`, `Archon`, `Prism`, and `Init`

The installer skill source lives in this repository at `install/hermes-chat-install/SKILL.md`.

## Recommended Safe Local Install

From a local SynapseOS checkout:

```sh
./synapse-cli install --agent hermes --dry-run --json
```

Review the planned destination and install state. A fresh install reports `install_mode: install`. A previous SynapseOS install reports `install_mode: update`. The plan also reports `payload_version` and `previous_installation.payload.version_status` so an older installed payload is visible before applying the refresh.

If the dry-run reports `previous_installation.status: existing_grouped_payload`, the installer found an existing grouped SynapseOS payload under the Hermes target. This is the normal safe update path when the payload markers are present.

If the plan is correct:

```sh
./synapse-cli install --agent hermes --yes --json
```

Verify the SynapseOS payload and manifest:

```sh
./synapse-cli verify --agent hermes --json
```

Verify Hermes' native skill view:

```sh
hermes skills list
hermes skills check
```

If Hermes does not show newly installed skills in the current session, start a new Hermes session so the skill list is reloaded.

## Custom Target

Use `--target` when your Hermes skills directory is not `~/.hermes/skills`:

```sh
./synapse-cli install --agent hermes --target /path/to/hermes/skills --dry-run --json
./synapse-cli install --agent hermes --target /path/to/hermes/skills --yes --json
./synapse-cli verify --agent hermes --target /path/to/hermes/skills --json
```

The final install root is:

```text
/path/to/hermes/skills/synapseos
```

## Quick Learning Prompt

After installation, ask Hermes:

```text
Use SynapseOS. Explain when I should use Xuan Master, Archon, Prism, and Init, then recommend the first skill for my current task.
```

For architecture or reasoning tasks:

```text
Use xuan-master to choose the right cognitive model pipeline for this problem.
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
./synapse-cli install --agent hermes --dry-run --json
./synapse-cli install --agent hermes --yes --json
./synapse-cli verify --agent hermes --json
hermes skills list
hermes skills check
```

For an existing grouped install, the dry-run should show:

```text
install_mode: update
previous_installation.status: existing_grouped_payload
previous_installation.update_required: true
```

The approved update refreshes the managed payload at `~/.hermes/skills/synapseos`.

## Troubleshooting

### `hermes: command not found`

Install Hermes Agent first, then verify:

```sh
hermes --version
hermes skills list
```

### `synapse-cli verify` fails

Check the `checks` array in the JSON output. Missing files usually mean the install target is not the same target used for verification.

### Hermes does not show newly installed skills

Start a new Hermes session or refresh the current session. If Hermes still does not list the skills, check:

- the Hermes skills root you installed into
- whether Hermes expects skills under category directories
- whether any `SKILL.md` frontmatter errors are reported
- whether your local Hermes configuration disables local skills

### Existing Hermes Install Detected

The current installer handles an existing grouped SynapseOS install as an update:

```text
~/.hermes/skills/synapseos
```

Rerun the current installer. The dry-run should report `previous_installation.status: existing_grouped_payload` and `install_mode: update`, then the approved install refreshes the payload in place.

If the dry-run reports `conflict_existing_payload`, the existing `synapseos` directory does not look like a SynapseOS payload. Inspect or move it before rerunning the installer.

### Target Already Exists

Review before overwriting:

```sh
./synapse-cli install --agent hermes --dry-run --json
```

If you maintain your own modified local copy, prefer a symlink strategy or a custom target:

```sh
./synapse-cli install --agent hermes --strategy symlink --target /path/to/hermes/skills --dry-run --json
```

## Reference Artifacts

- Spec: `.aries_harness/references/specs/SPEC-004-hermes-chat-install.md`
- Story pack: `.aries_harness/references/stories/STORY-004-hermes-chat-install.md`
- Architecture: `.aries_harness/decisions/architecture/ARCH-004-hermes-chat-install.md`
- ADR: `.aries_harness/decisions/adrs/ADR-0006-hermes-chat-install.md`

## Hermes References

- Hermes working with skills: `https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/work-with-skills.md`
- Hermes skills feature reference: `https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md`
