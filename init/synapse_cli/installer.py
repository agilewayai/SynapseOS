from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import json
import re
import shutil

from .adapters import HostAdapter


PAYLOAD_PATHS = (
    "AGENTS.md",
    "README.md",
    "LICENSE",
    "docs",
    "synapse-cli",
    "xuan-master",
    "archon",
    "prism",
    "optimization",
    "init",
)

OPENCLAW_NATIVE_SKILL_PATHS = (
    "xuan-master",
    "archon",
    "prism",
    "init",
    "optimization",
)

OPENCLAW_NATIVE_SKILL_NAMES = {
    "xuan-master": "xuan_master",
    "archon": "archon",
    "prism": "prism",
    "init": "synapse_init",
    "optimization": "optimization",
}

OPENCLAW_CANONICAL_SKILL_NAMES = {
    "xuan-master": "xuan-master",
    "archon": "archon",
    "prism": "prism",
    "init": "synapse-init",
    "optimization": "optimization",
}

REQUIRED_INSTALLED_FILES = (
    "AGENTS.md",
    "README.md",
    "LICENSE",
    "synapse-cli",
    "xuan-master/SKILL.md",
    "xuan-master/00-entry/SKILL.md",
    "archon/SKILL.md",
    "archon/enabled/SKILL.md",
    "archon/interview/SKILL.md",
    "prism/SKILL.md",
    "init/SKILL.md",
    "synapseos-install-manifest.json",
)

SYNAPSEOS_PAYLOAD_MARKERS = (
    "synapse-cli",
    "xuan-master/SKILL.md",
    "archon/SKILL.md",
    "prism/SKILL.md",
    "init/SKILL.md",
)

VERSION_PATTERN = re.compile(r"\bVersion:\s*([0-9]+(?:\.[0-9]+){0,3})\b")


@dataclass(frozen=True)
class InstallOperation:
    action: str
    source: str | None
    destination: str
    status: str


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _payload_version_from_agents(agents_file: Path) -> str | None:
    try:
        text = agents_file.read_text(encoding="utf-8")
    except OSError:
        return None

    match = VERSION_PATTERN.search(text)
    if not match:
        return None
    return match.group(1)


def _frontmatter_field(skill_file: Path, field_name: str) -> str | None:
    try:
        lines = skill_file.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None

    if not lines or lines[0].strip() != "---":
        return None

    prefix = f"{field_name}:"
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            return None
        if stripped.startswith(prefix):
            return stripped.split(":", 1)[1].strip().strip("\"'")

    return None


def _source_payload_version(repo_root: Path) -> str | None:
    return (
        _payload_version_from_agents(repo_root / "AGENTS.md")
        or _frontmatter_field(repo_root / "xuan-master" / "00-entry" / "SKILL.md", "version")
    )


def _installed_payload_version(install_root: Path, manifest_payload_version: str | None) -> str | None:
    return (
        manifest_payload_version
        or _payload_version_from_agents(install_root / "AGENTS.md")
        or _frontmatter_field(install_root / "xuan-master" / "00-entry" / "SKILL.md", "version")
    )


def _version_tuple(version: str) -> tuple[int, ...] | None:
    parts = version.split(".")
    if not parts or not all(part.isdigit() for part in parts):
        return None
    return tuple(int(part) for part in parts)


def _version_status(installed_version: str | None, source_version: str | None, payload_exists: bool) -> str:
    if not payload_exists:
        return "none"
    if not installed_version or not source_version:
        return "unknown"
    if installed_version == source_version:
        return "current"

    installed_tuple = _version_tuple(installed_version)
    source_tuple = _version_tuple(source_version)
    if installed_tuple is None or source_tuple is None:
        return "different"

    max_len = max(len(installed_tuple), len(source_tuple))
    padded_installed = installed_tuple + (0,) * (max_len - len(installed_tuple))
    padded_source = source_tuple + (0,) * (max_len - len(source_tuple))
    if padded_installed < padded_source:
        return "older"
    if padded_installed > padded_source:
        return "newer"
    return "different"


def _openclaw_native_skill_root(adapter: HostAdapter, target: str | None, install_root: Path) -> Path | None:
    if adapter.adapter_id != "openclaw":
        return None

    base, _target_source = adapter.resolve_base(target)
    if base is None:
        return None
    if base.name == "synapseos":
        return install_root.parent
    return base


def _frontmatter_name(skill_file: Path) -> str | None:
    return _frontmatter_field(skill_file, "name")


def _openclaw_native_entry(native_skill_root: Path, relative: str) -> dict:
    entry_root = native_skill_root / relative
    skill_file = entry_root / "SKILL.md"
    expected_name = OPENCLAW_NATIVE_SKILL_NAMES[relative]
    canonical_name = OPENCLAW_CANONICAL_SKILL_NAMES[relative]
    actual_name = _frontmatter_name(skill_file)

    if not entry_root.exists():
        status = "missing"
    elif not entry_root.is_dir():
        status = "conflict"
    elif not skill_file.exists():
        status = "conflict"
    elif actual_name == expected_name:
        status = "current"
    elif actual_name == canonical_name:
        status = "legacy_name"
    else:
        status = "conflict"

    return {
        "path": str(entry_root),
        "skill_file": str(skill_file),
        "expected_name": expected_name,
        "canonical_name": canonical_name,
        "actual_name": actual_name,
        "status": status,
    }


def _is_synapseos_native_skill(path: Path, relative: str) -> bool:
    if not path.is_dir():
        return False

    return _openclaw_native_entry(path.parent, relative)["status"] in {"current", "legacy_name"}


def _payload_state(install_root: Path, source_payload_version: str | None) -> dict:
    present_markers = [
        relative
        for relative in SYNAPSEOS_PAYLOAD_MARKERS
        if (install_root / relative).exists()
    ]
    manifest_path = install_root / "synapseos-install-manifest.json"
    manifest_adapter = None
    manifest_has_native_entries = False
    manifest_payload_version = None

    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest_adapter = manifest.get("adapter")
            manifest_has_native_entries = bool(manifest.get("native_skill_paths"))
            manifest_payload_version = manifest.get("payload_version")
        except json.JSONDecodeError:
            manifest_adapter = "invalid-json"

    installed_payload_version = _installed_payload_version(install_root, manifest_payload_version)

    return {
        "exists": install_root.exists(),
        "recognized": bool(present_markers or manifest_path.exists()),
        "present_markers": present_markers,
        "manifest_path": str(manifest_path),
        "manifest_exists": manifest_path.exists(),
        "manifest_adapter": manifest_adapter,
        "manifest_has_native_entries": manifest_has_native_entries,
        "manifest_payload_version": manifest_payload_version,
        "installed_payload_version": installed_payload_version,
        "source_payload_version": source_payload_version,
        "version_status": _version_status(installed_payload_version, source_payload_version, install_root.exists()),
    }


def _grouped_previous_installation(install_root: Path, source_payload_version: str | None) -> dict:
    payload = _payload_state(install_root, source_payload_version)

    if payload["exists"] and not payload["recognized"]:
        status = "existing_unrecognized_payload"
        update_required = False
    elif not payload["exists"]:
        status = "fresh"
        update_required = False
    else:
        status = "existing_grouped_payload"
        update_required = True

    return {
        "status": status,
        "install_mode": "update" if payload["exists"] else "install",
        "update_required": update_required,
        "payload": payload,
    }


def _openclaw_previous_installation(
    install_root: Path,
    native_skill_root: Path | None,
    source_payload_version: str | None,
) -> dict | None:
    if native_skill_root is None:
        return None

    previous = _grouped_previous_installation(install_root, source_payload_version)
    payload = previous["payload"]
    native_entries = {
        relative: _openclaw_native_entry(native_skill_root, relative)
        for relative in OPENCLAW_NATIVE_SKILL_PATHS
    }
    native_statuses = [entry["status"] for entry in native_entries.values()]
    has_any_native_entry = any(status != "missing" for status in native_statuses)
    has_all_current_native_entries = all(status == "current" for status in native_statuses)
    has_current_manifest = payload["manifest_adapter"] == "openclaw" and payload["manifest_has_native_entries"]
    has_conflict = any(status == "conflict" for status in native_statuses)

    if previous["status"] == "existing_unrecognized_payload":
        status = "existing_unrecognized_payload"
        update_required = False
    elif has_conflict:
        status = "conflict"
        update_required = False
    elif not payload["exists"] and not has_any_native_entry:
        status = "fresh"
        update_required = False
    elif payload["exists"] and not has_any_native_entry:
        status = "legacy_grouped_only"
        update_required = True
    elif not payload["exists"] and has_any_native_entry:
        status = "native_entries_without_payload"
        update_required = True
    elif has_all_current_native_entries and has_current_manifest and payload["version_status"] == "current":
        status = "current"
        update_required = False
    else:
        status = "update_required"
        update_required = True

    return {
        "status": status,
        "install_mode": "update" if payload["exists"] or has_any_native_entry else "install",
        "update_required": update_required,
        "payload": payload,
        "native_entries": native_entries,
    }


def _previous_installation(
    adapter: HostAdapter,
    install_root: Path,
    native_skill_root: Path | None,
    source_payload_version: str | None,
) -> dict | None:
    if adapter.adapter_id == "openclaw":
        return _openclaw_previous_installation(install_root, native_skill_root, source_payload_version)
    return _grouped_previous_installation(install_root, source_payload_version)


def _openclaw_skill_text(source_skill: Path, relative: str) -> str:
    expected_name = OPENCLAW_NATIVE_SKILL_NAMES[relative]
    lines = source_skill.read_text(encoding="utf-8").splitlines()
    patched: list[str] = []
    replaced_name = False
    in_frontmatter = bool(lines and lines[0].strip() == "---")

    for index, line in enumerate(lines):
        stripped = line.strip()
        if index > 0 and in_frontmatter and stripped == "---":
            if not replaced_name:
                patched.append(f"name: {expected_name}")
            patched.append(line)
            in_frontmatter = False
            continue
        if in_frontmatter and stripped.startswith("name:"):
            patched.append(f"name: {expected_name}")
            replaced_name = True
            continue
        patched.append(line)

    return "\n".join(patched) + "\n"


def _copy_openclaw_native_skill(source: Path, destination: Path) -> None:
    relative = source.name
    if destination.is_symlink():
        destination.unlink()
    _copy_path(source, destination)
    (destination / "SKILL.md").write_text(_openclaw_skill_text(source / "SKILL.md", relative), encoding="utf-8")


def build_plan(repo_root: Path, adapter: HostAdapter, target: str | None, strategy: str) -> dict:
    install_root, target_source = adapter.install_root(target)
    if install_root is None:
        return {
            "status": "error",
            "message": f"{adapter.adapter_id} requires --target for install planning",
            "adapter": adapter.adapter_id,
            "operations": [],
        }

    operations: list[InstallOperation] = [
        InstallOperation("ensure_dir", None, str(install_root), "planned")
    ]

    native_skill_root = _openclaw_native_skill_root(adapter, target, install_root)
    source_payload_version = _source_payload_version(repo_root)
    previous_installation = _previous_installation(adapter, install_root, native_skill_root, source_payload_version)
    if native_skill_root is not None:
        operations.append(InstallOperation("ensure_dir", None, str(native_skill_root), "planned"))

    if previous_installation and previous_installation["status"] == "existing_unrecognized_payload":
        operations.append(
            InstallOperation(
                "conflict_existing_payload",
                None,
                str(install_root),
                "error",
            )
        )

    for relative in PAYLOAD_PATHS:
        source = repo_root / relative
        destination = install_root / relative
        if source.exists():
            operations.append(InstallOperation(strategy, str(source), str(destination), "planned"))
        else:
            operations.append(InstallOperation("missing_source", str(source), str(destination), "error"))

    if native_skill_root is not None:
        for relative in OPENCLAW_NATIVE_SKILL_PATHS:
            source = repo_root / relative
            destination = native_skill_root / relative
            if not source.exists():
                operations.append(InstallOperation("missing_source", str(source), str(destination), "error"))
            elif destination.exists() and not _is_synapseos_native_skill(destination, relative):
                operations.append(
                    InstallOperation(
                        "conflict_existing_path",
                        str(source),
                        str(destination),
                        "error",
                    )
                )
            else:
                operations.append(
                    InstallOperation(
                        "copy_openclaw_skill",
                        str(source),
                        str(destination),
                        "planned",
                    )
                )

    operations.append(
        InstallOperation(
            "write_manifest",
            None,
            str(install_root / "synapseos-install-manifest.json"),
            "planned",
        )
    )

    has_error = any(operation.status == "error" for operation in operations)
    return {
        "status": "error" if has_error else "planned",
        "adapter": adapter.adapter_id,
        "display_name": adapter.display_name,
        "strategy": strategy,
        "payload_version": source_payload_version,
        "target_source": target_source,
        "install_root": str(install_root),
        "install_mode": previous_installation["install_mode"] if previous_installation else ("update" if install_root.exists() else "install"),
        "previous_installation": previous_installation,
        "native_skill_root": str(native_skill_root) if native_skill_root else None,
        "native_skill_paths": list(OPENCLAW_NATIVE_SKILL_PATHS) if native_skill_root else [],
        "native_skill_names": {
            relative: OPENCLAW_NATIVE_SKILL_NAMES[relative]
            for relative in OPENCLAW_NATIVE_SKILL_PATHS
        } if native_skill_root else {},
        "operations": [asdict(operation) for operation in operations],
    }


def _copy_path(source: Path, destination: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, destination, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def _symlink_path(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_symlink():
        if destination.resolve() == source.resolve():
            return
        destination.unlink()
    elif destination.exists():
        raise FileExistsError(f"refusing to replace non-symlink path: {destination}")
    destination.symlink_to(source, target_is_directory=source.is_dir())


def apply_plan(repo_root: Path, plan: dict) -> dict:
    if plan.get("status") == "error":
        return {"status": "error", "message": plan.get("message", "install plan contains errors"), "plan": plan}

    install_root = Path(plan["install_root"])
    install_root.mkdir(parents=True, exist_ok=True)

    applied: list[dict] = []
    for operation in plan["operations"]:
        action = operation["action"]
        if action == "ensure_dir":
            Path(operation["destination"]).mkdir(parents=True, exist_ok=True)
            applied.append({**operation, "status": "applied"})
        elif action in {"copy", "symlink"}:
            source = Path(operation["source"])
            destination = Path(operation["destination"])
            if action == "copy":
                _copy_path(source, destination)
            else:
                _symlink_path(source, destination)
            applied.append({**operation, "status": "applied"})
        elif action == "copy_openclaw_skill":
            source = Path(operation["source"])
            destination = Path(operation["destination"])
            _copy_openclaw_native_skill(source, destination)
            applied.append({**operation, "status": "applied"})

    manifest = {
        "schema_version": 1,
        "installed_at": utc_now(),
        "source_repo": str(repo_root),
        "adapter": plan["adapter"],
        "display_name": plan["display_name"],
        "strategy": plan["strategy"],
        "payload_version": plan.get("payload_version"),
        "install_root": str(install_root),
        "install_mode": plan.get("install_mode", "install"),
        "payload_paths": list(PAYLOAD_PATHS),
        "previous_installation": plan.get("previous_installation"),
        "native_skill_root": plan.get("native_skill_root"),
        "native_skill_paths": plan.get("native_skill_paths", []),
        "native_skill_names": {
            relative: OPENCLAW_NATIVE_SKILL_NAMES[relative]
            for relative in plan.get("native_skill_paths", [])
        },
        "operations": applied,
    }
    manifest_path = install_root / "synapseos-install-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    applied.append({"action": "write_manifest", "source": None, "destination": str(manifest_path), "status": "applied"})

    return {
        "status": "installed",
        "adapter": plan["adapter"],
        "install_mode": plan.get("install_mode", "install"),
        "install_root": str(install_root),
        "manifest": str(manifest_path),
        "previous_installation": plan.get("previous_installation"),
        "operations": applied,
    }


def verify_install(adapter: HostAdapter, target: str | None) -> dict:
    install_root, _target_source = adapter.install_root(target)
    if install_root is None:
        return {
            "status": "fail",
            "adapter": adapter.adapter_id,
            "message": f"{adapter.adapter_id} requires --target for verification",
            "checks": [],
        }

    checks = []
    for relative in REQUIRED_INSTALLED_FILES:
        path = install_root / relative
        checks.append({
            "id": relative,
            "path": str(path),
            "status": "pass" if path.exists() else "fail",
        })

    manifest_path = install_root / "synapseos-install-manifest.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            checks.append({
                "id": "manifest-json",
                "path": str(manifest_path),
                "status": "pass" if manifest.get("adapter") == adapter.adapter_id else "fail",
            })
        except json.JSONDecodeError:
            checks.append({"id": "manifest-json", "path": str(manifest_path), "status": "fail"})

    native_skill_root = _openclaw_native_skill_root(adapter, target, install_root)
    source_payload_version = _source_payload_version(Path(__file__).resolve().parents[2])
    previous_installation = _previous_installation(adapter, install_root, native_skill_root, source_payload_version)
    if native_skill_root is not None:
        for relative in OPENCLAW_NATIVE_SKILL_PATHS:
            path = native_skill_root / relative / "SKILL.md"
            expected_name = OPENCLAW_NATIVE_SKILL_NAMES[relative]
            status = "fail"
            if path.exists() and _frontmatter_name(path) == expected_name:
                status = "pass"
            checks.append({
                "id": f"openclaw-native/{relative}/SKILL.md",
                "path": str(path),
                "status": status,
                "expected_name": expected_name,
            })

    status = "pass" if all(check["status"] == "pass" for check in checks) else "fail"
    return {
        "status": status,
        "adapter": adapter.adapter_id,
        "install_root": str(install_root),
        "payload_version": source_payload_version,
        "native_skill_root": str(native_skill_root) if native_skill_root else None,
        "previous_installation": previous_installation,
        "checks": checks,
    }
