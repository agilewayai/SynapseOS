from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import json
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


@dataclass(frozen=True)
class InstallOperation:
    action: str
    source: str | None
    destination: str
    status: str


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


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

    for relative in PAYLOAD_PATHS:
        source = repo_root / relative
        destination = install_root / relative
        if source.exists():
            operations.append(InstallOperation(strategy, str(source), str(destination), "planned"))
        else:
            operations.append(InstallOperation("missing_source", str(source), str(destination), "error"))

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
        "target_source": target_source,
        "install_root": str(install_root),
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

    manifest = {
        "schema_version": 1,
        "installed_at": utc_now(),
        "source_repo": str(repo_root),
        "adapter": plan["adapter"],
        "display_name": plan["display_name"],
        "strategy": plan["strategy"],
        "install_root": str(install_root),
        "payload_paths": list(PAYLOAD_PATHS),
        "operations": applied,
    }
    manifest_path = install_root / "synapseos-install-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    applied.append({"action": "write_manifest", "source": None, "destination": str(manifest_path), "status": "applied"})

    return {
        "status": "installed",
        "adapter": plan["adapter"],
        "install_root": str(install_root),
        "manifest": str(manifest_path),
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

    status = "pass" if all(check["status"] == "pass" for check in checks) else "fail"
    return {
        "status": status,
        "adapter": adapter.adapter_id,
        "install_root": str(install_root),
        "checks": checks,
    }
