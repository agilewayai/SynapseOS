from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "install" / "synapseos.sh"


class OneLineInstallerTests(unittest.TestCase):
    def run_installer(
        self,
        *args: str,
        home: Path,
        check: bool = True,
        skip_doctor: bool = True,
        extra_env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["HOME"] = str(home)
        env["PATH"] = os.environ.get("PATH", "")
        if extra_env:
            env.update(extra_env)

        command = ["sh", str(INSTALLER), "--repo", str(REPO_ROOT)]
        if skip_doctor:
            command.append("--skip-doctor")
        command.extend(args)
        result = subprocess.run(
            command,
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            env=env,
        )
        if check and result.returncode != 0:
            raise AssertionError(
                f"installer failed: {args}\nstdout={result.stdout}\nstderr={result.stderr}"
            )
        return result

    def test_installer_creates_synapse_cli_launcher(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            install_dir = root / "managed" / "SynapseOS"
            bin_dir = root / "bin"

            self.run_installer(
                "--install-dir",
                str(install_dir),
                "--bin-dir",
                str(bin_dir),
                home=root,
            )

            launcher = bin_dir / "synapse-cli"
            self.assertTrue(launcher.exists())
            self.assertTrue((install_dir / "synapse-cli").exists())

            result = subprocess.run(
                [str(launcher), "--version"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("synapse-cli", result.stdout)

    def test_installer_doctor_summary_is_compact_when_readiness_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            install_dir = root / "managed" / "SynapseOS"
            bin_dir = root / "bin"

            result = self.run_installer(
                "--install-dir",
                str(install_dir),
                "--bin-dir",
                str(bin_dir),
                home=root,
                skip_doctor=False,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("Readiness: pass", result.stdout)
            self.assertIn("Result: CLI installed", result.stdout)
            self.assertNotIn('"checks"', result.stdout)
            self.assertNotIn('"hosts"', result.stdout)

    def test_installer_summarizes_failed_doctor_without_full_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            install_dir = root / "managed" / "SynapseOS"
            bin_dir = root / "bin"
            fake_bin = root / "fake-bin"
            fake_bin.mkdir()
            fake_python = fake_bin / "python3"
            fake_python.write_text(
                f"""#!/usr/bin/env sh
if [ "$1" = "-" ]; then
    exec "{sys.executable}" "$@"
fi
if [ "$2" = "doctor" ]; then
    cat <<'JSON'
{{"status":"fail","checks":[{{"id":"python","category":"runtime","required":true,"status":"fail","detected":"3.8.9","missing":true,"hint":"Use Python 3.9 or newer."}}],"hosts":[]}}
JSON
    exit 1
fi
exec "{sys.executable}" "$@"
""",
                encoding="utf-8",
            )
            fake_python.chmod(0o755)

            result = self.run_installer(
                "--install-dir",
                str(install_dir),
                "--bin-dir",
                str(bin_dir),
                home=root,
                skip_doctor=False,
                extra_env={"PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}"},
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("Readiness: failed", result.stdout)
            self.assertIn("install Python 3.9 or newer (detected 3.8.9)", result.stdout)
            self.assertIn("Result: CLI installed with readiness issues", result.stdout)
            self.assertNotIn('"checks"', result.stdout)
            self.assertNotIn('"hosts"', result.stdout)

    def test_installer_can_apply_generic_skills_install(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            install_dir = root / "managed" / "SynapseOS"
            bin_dir = root / "bin"
            target = root / "host"

            result = self.run_installer(
                "--install-dir",
                str(install_dir),
                "--bin-dir",
                str(bin_dir),
                "--agent",
                "generic",
                "--target",
                str(target),
                "--yes",
                home=root,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue((target / "synapseos" / "synapse-cli").exists())
            self.assertTrue((target / "synapseos" / "xuan-master" / "SKILL.md").exists())
            self.assertIn("Verifying skills install for agent: generic", result.stdout)


if __name__ == "__main__":
    unittest.main()
