---
name: synapseos-installer
description: "Install and verify the SynapseOS skills family for Hermes Agent from a chat session. Use when a Hermes user wants one prompt to install Xuan Master, Archon, Prism, and Init into the local Hermes skills directory."
version: 0.1.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [synapseos, installer, skills, cognition, setup]
    related_skills: [hermes-agent]
---

# SynapseOS Installer For Hermes

This skill installs the SynapseOS skills family into Hermes Agent.

## What It Installs

- `xuan-master`: 27-model cognition core
- `archon`: calibration, orchestration, actions, and generation layer
- `prism`: specialist routing layer
- `init`: setup, installation, and verification layer

## Safety Policy

- Do not run opaque remote shell.
- Do not overwrite a non-SynapseOS folder without explicit user confirmation.
- Always show the resolved Hermes target and dry-run plan before applying writes.
- Prefer HTTPS clone so the install does not require SSH key setup.
- If a command needs approval, ask with the exact command and reason.
- If `hermes` is not available on `PATH`, stop and explain that Hermes Agent must be installed first.

## Install Workflow

1. Check prerequisites:

```sh
hermes --version
hermes skills list
git --version
python3 --version
```

2. Prepare or update a local SynapseOS checkout:

```sh
INSTALL_ROOT="${TMPDIR:-/tmp}/synapseos-hermes-install"
if [ -d "$INSTALL_ROOT/.git" ]; then
  git -C "$INSTALL_ROOT" pull --ff-only
else
  git clone https://github.com/agilewayai/SynapseOS.git "$INSTALL_ROOT"
fi
```

3. Inspect SynapseOS readiness:

```sh
cd "$INSTALL_ROOT"
./synapse-cli doctor --json
```

4. Show the Hermes install plan:

```sh
./synapse-cli install --agent hermes --dry-run --json
```

Confirm the plan includes:

- `install_root`: `~/.hermes/skills/synapseos`
- `install_mode`: `install` for a fresh target or `update` when a previous SynapseOS install exists
- `payload_version` and `previous_installation.payload.version_status`: use these to identify old installed payloads before refresh
- `previous_installation.status`: `fresh`, `existing_grouped_payload`, or `existing_unrecognized_payload`

If `previous_installation.status` is `existing_grouped_payload`, this is an existing SynapseOS install. Treat it as a safe update path if the payload markers are present.

5. If the dry-run target is safe, install:

```sh
./synapse-cli install --agent hermes --yes --json
```

6. Verify the SynapseOS payload:

```sh
./synapse-cli verify --agent hermes --json
```

7. Verify Hermes can see skills:

```sh
hermes skills list
hermes skills check
```

If the newly installed skills do not appear in the current session, tell the user to start a new Hermes session or reset the current session so Hermes reloads its skill list.

## Success Response

After successful verification, explain:

- where SynapseOS was installed
- whether this was a fresh install or an update of a previous install
- whether `synapse-cli verify --agent hermes` passed
- whether Hermes listed the installed skills
- how to start using the skill family

Then tell the user to try:

```text
Use SynapseOS. Explain when I should use Xuan Master, Archon, Prism, and Init, then recommend the first skill for my current task.
```

## Failure Response

If any step fails, stop and report:

- the command that failed
- the relevant error message
- whether the failure is prerequisite, checkout, SynapseOS payload verification, or Hermes skill visibility
- whether the dry-run reported `conflict_existing_payload`
- the safest next command to retry
