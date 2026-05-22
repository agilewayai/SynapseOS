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
    def run_installer(self, *args: str, home: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["HOME"] = str(home)
        env["PATH"] = os.environ.get("PATH", "")

        result = subprocess.run(
            ["sh", str(INSTALLER), "--repo", str(REPO_ROOT), "--skip-doctor", *args],
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
