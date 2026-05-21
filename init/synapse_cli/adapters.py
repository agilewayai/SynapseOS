from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import shutil


@dataclass(frozen=True)
class DetectionResult:
    adapter_id: str
    display_name: str
    command_found: bool
    command_path: str | None
    target_base: str | None
    target_source: str | None
    target_exists: bool
    detected: bool
    notes: list[str]


@dataclass(frozen=True)
class HostAdapter:
    adapter_id: str
    display_name: str
    commands: tuple[str, ...]
    default_base_parts: tuple[str, ...] | None
    env_var: str
    requires_explicit_target: bool = False

    def default_base(self) -> Path | None:
        if self.default_base_parts is None:
            return None
        return Path.home().joinpath(*self.default_base_parts).expanduser()

    def resolve_base(self, target_override: str | None = None) -> tuple[Path | None, str | None]:
        if target_override:
            return Path(target_override).expanduser(), "argument"

        env_value = os.environ.get(self.env_var)
        if env_value:
            return Path(env_value).expanduser(), self.env_var

        if self.requires_explicit_target:
            return None, None

        return self.default_base(), "default"

    def install_root(self, target_override: str | None = None) -> tuple[Path | None, str | None]:
        base, source = self.resolve_base(target_override)
        if base is None:
            return None, source
        return (base if base.name == "synapseos" else base / "synapseos"), source

    def detect(self, target_override: str | None = None) -> DetectionResult:
        command_path = next((shutil.which(command) for command in self.commands if shutil.which(command)), None)
        target_base, target_source = self.resolve_base(target_override)
        target_exists = bool(target_base and target_base.exists())
        notes: list[str] = []

        if self.requires_explicit_target and target_override is None:
            notes.append("requires --target for installation and verification")
        if target_base and not target_exists:
            notes.append("target base does not exist yet")
        if not command_path and self.commands:
            notes.append("host command was not found on PATH")

        return DetectionResult(
            adapter_id=self.adapter_id,
            display_name=self.display_name,
            command_found=command_path is not None,
            command_path=command_path,
            target_base=str(target_base) if target_base else None,
            target_source=target_source,
            target_exists=target_exists,
            detected=bool(command_path or target_exists or target_override),
            notes=notes,
        )


ADAPTERS: dict[str, HostAdapter] = {
    "claude-code": HostAdapter(
        adapter_id="claude-code",
        display_name="Claude Code",
        commands=("claude",),
        default_base_parts=(".claude", "skills"),
        env_var="SYNAPSE_CLAUDE_CODE_TARGET",
    ),
    "codex": HostAdapter(
        adapter_id="codex",
        display_name="Codex",
        commands=("codex",),
        default_base_parts=(".codex", "skills"),
        env_var="SYNAPSE_CODEX_TARGET",
    ),
    "cursor": HostAdapter(
        adapter_id="cursor",
        display_name="Cursor",
        commands=("cursor",),
        default_base_parts=(".cursor", "rules"),
        env_var="SYNAPSE_CURSOR_TARGET",
    ),
    "opencode": HostAdapter(
        adapter_id="opencode",
        display_name="OpenCode",
        commands=("opencode",),
        default_base_parts=(".opencode", "skills"),
        env_var="SYNAPSE_OPENCODE_TARGET",
    ),
    "openclaw": HostAdapter(
        adapter_id="openclaw",
        display_name="OpenClaw",
        commands=("openclaw",),
        default_base_parts=(".openclaw", "skills"),
        env_var="SYNAPSE_OPENCLAW_TARGET",
    ),
    "hermes": HostAdapter(
        adapter_id="hermes",
        display_name="Hermes",
        commands=("hermes",),
        default_base_parts=(".hermes", "skills"),
        env_var="SYNAPSE_HERMES_TARGET",
    ),
    "generic": HostAdapter(
        adapter_id="generic",
        display_name="Generic Agent Host",
        commands=(),
        default_base_parts=None,
        env_var="SYNAPSE_GENERIC_TARGET",
        requires_explicit_target=True,
    ),
}


def get_adapter(adapter_id: str) -> HostAdapter:
    try:
        return ADAPTERS[adapter_id]
    except KeyError as exc:
        known = ", ".join(sorted(ADAPTERS))
        raise ValueError(f"unknown agent adapter '{adapter_id}'. Known adapters: {known}") from exc
