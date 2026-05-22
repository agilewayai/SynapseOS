#!/usr/bin/env sh
set -eu

DEFAULT_REPO="https://github.com/agilewayai/SynapseOS.git"
DEFAULT_REF="main"
DEFAULT_INSTALL_DIR="$HOME/.synapseos/SynapseOS"
DEFAULT_BIN_DIR="$HOME/.local/bin"

repo="${SYNAPSEOS_REPO:-$DEFAULT_REPO}"
ref="${SYNAPSEOS_REF:-$DEFAULT_REF}"
install_dir="${SYNAPSEOS_INSTALL_DIR:-$DEFAULT_INSTALL_DIR}"
bin_dir="${SYNAPSEOS_BIN_DIR:-$DEFAULT_BIN_DIR}"
agent="${SYNAPSEOS_AGENT:-}"
target="${SYNAPSEOS_TARGET:-}"
strategy="${SYNAPSEOS_STRATEGY:-copy}"
yes="${SYNAPSEOS_YES:-0}"
dry_run="${SYNAPSEOS_DRY_RUN:-0}"
skip_doctor="${SYNAPSEOS_SKIP_DOCTOR:-0}"

usage() {
    cat <<'EOF'
SynapseOS one-line installer

Usage:
  curl -fsSL https://raw.githubusercontent.com/agilewayai/SynapseOS/main/install/synapseos.sh | bash
  curl -fsSL https://raw.githubusercontent.com/agilewayai/SynapseOS/main/install/synapseos.sh | bash -s -- --agent codex --yes
  curl -fsSL https://raw.githubusercontent.com/agilewayai/SynapseOS/main/install/synapseos.sh | bash -s -- --agent generic --target /path/to/host --yes

Options:
  --agent <id>          Also install the skills stack into this agent host.
  --target <path>      Host base directory for adapters that need an explicit target.
  --strategy <mode>    synapse-cli install strategy: copy or symlink. Default: copy.
  --yes                Apply the agent install after showing the dry-run plan.
  --dry-run            Only show the agent install plan.
  --repo <url-or-path> Repository to clone. Default: official GitHub repository.
  --ref <ref>          Git ref to install. Default: main.
  --install-dir <path> Managed checkout path. Default: ~/.synapseos/SynapseOS.
  --bin-dir <path>     Directory for the synapse-cli launcher. Default: ~/.local/bin.
  --skip-doctor        Skip the post-install doctor check.
  -h, --help           Show this help.

Environment variables mirror the option names:
  SYNAPSEOS_AGENT, SYNAPSEOS_TARGET, SYNAPSEOS_YES, SYNAPSEOS_REPO,
  SYNAPSEOS_REF, SYNAPSEOS_INSTALL_DIR, SYNAPSEOS_BIN_DIR.
EOF
}

log() {
    printf '%s\n' "synapseos-install: $*"
}

die() {
    printf '%s\n' "synapseos-install: error: $*" >&2
    exit 1
}

need_arg() {
    [ "$#" -ge 2 ] || die "missing value for $1"
}

expand_path() {
    case "$1" in
        "~")
            printf '%s\n' "$HOME"
            ;;
        "~/"*)
            printf '%s/%s\n' "$HOME" "${1#~/}"
            ;;
        *)
            printf '%s\n' "$1"
            ;;
    esac
}

while [ "$#" -gt 0 ]; do
    case "$1" in
        --agent)
            need_arg "$@"
            agent="$2"
            shift 2
            ;;
        --target)
            need_arg "$@"
            target="$2"
            shift 2
            ;;
        --strategy)
            need_arg "$@"
            strategy="$2"
            shift 2
            ;;
        --yes)
            yes="1"
            shift
            ;;
        --dry-run)
            dry_run="1"
            shift
            ;;
        --repo)
            need_arg "$@"
            repo="$2"
            shift 2
            ;;
        --ref)
            need_arg "$@"
            ref="$2"
            shift 2
            ;;
        --install-dir)
            need_arg "$@"
            install_dir="$2"
            shift 2
            ;;
        --bin-dir)
            need_arg "$@"
            bin_dir="$2"
            shift 2
            ;;
        --skip-doctor)
            skip_doctor="1"
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            die "unknown option: $1"
            ;;
    esac
done

install_dir="$(expand_path "$install_dir")"
bin_dir="$(expand_path "$bin_dir")"

command -v git >/dev/null 2>&1 || die "git is required"
command -v python3 >/dev/null 2>&1 || die "python3 is required"

case "$strategy" in
    copy|symlink)
        ;;
    *)
        die "--strategy must be copy or symlink"
        ;;
esac

install_parent="$(dirname "$install_dir")"
mkdir -p "$install_parent"

if [ -d "$install_dir/.git" ]; then
    log "Updating managed checkout at $install_dir"
    if [ -n "$(git -C "$install_dir" status --porcelain)" ]; then
        die "$install_dir has local changes; refusing to overwrite them"
    fi
    git -C "$install_dir" fetch --depth 1 origin "$ref"
    git -C "$install_dir" checkout --detach FETCH_HEAD >/dev/null
elif [ -e "$install_dir" ]; then
    die "$install_dir exists but is not a git checkout; choose another --install-dir"
else
    log "Installing managed checkout at $install_dir"
    git clone --depth 1 "$repo" "$install_dir"
    if [ -n "$ref" ]; then
        git -C "$install_dir" fetch --depth 1 origin "$ref" >/dev/null 2>&1 || true
        git -C "$install_dir" checkout --detach FETCH_HEAD >/dev/null 2>&1 || git -C "$install_dir" checkout "$ref" >/dev/null
    fi
fi

[ -x "$install_dir/synapse-cli" ] || die "synapse-cli was not found in $install_dir"

mkdir -p "$bin_dir"
launcher="$bin_dir/synapse-cli"
cat > "$launcher" <<EOF
#!/usr/bin/env sh
exec python3 "$install_dir/synapse-cli" "\$@"
EOF
chmod +x "$launcher"

log "Installed launcher at $launcher"

case ":$PATH:" in
    *":$bin_dir:"*)
        ;;
    *)
        log "Add $bin_dir to PATH to run synapse-cli directly"
        ;;
esac

if [ "$skip_doctor" != "1" ]; then
    log "Running synapse-cli doctor"
    "$launcher" doctor --json || log "doctor reported issues; inspect the JSON above"
fi

run_install_plan() {
    if [ -n "$target" ]; then
        "$launcher" install --agent "$agent" --target "$target" --strategy "$strategy" --dry-run --json
    else
        "$launcher" install --agent "$agent" --strategy "$strategy" --dry-run --json
    fi
}

run_install_apply() {
    if [ -n "$target" ]; then
        "$launcher" install --agent "$agent" --target "$target" --strategy "$strategy" --yes --json
    else
        "$launcher" install --agent "$agent" --strategy "$strategy" --yes --json
    fi
}

run_verify() {
    if [ -n "$target" ]; then
        "$launcher" verify --agent "$agent" --target "$target" --json
    else
        "$launcher" verify --agent "$agent" --json
    fi
}

if [ -n "$agent" ]; then
    log "Planning skills install for agent: $agent"
    run_install_plan

    if [ "$dry_run" = "1" ] || [ "$yes" != "1" ]; then
        log "Dry-run complete. Re-run with --yes to apply the skills install."
        exit 0
    fi

    log "Applying skills install for agent: $agent"
    run_install_apply
    log "Verifying skills install for agent: $agent"
    run_verify
else
    log "synapse-cli is ready"
    log "Install skills with: curl -fsSL https://raw.githubusercontent.com/agilewayai/SynapseOS/main/install/synapseos.sh | bash -s -- --agent codex --yes"
fi
