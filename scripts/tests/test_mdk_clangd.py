import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

import mdk_clangd  # noqa: E402


def make_target(cpu: str) -> ET.Element:
    return ET.fromstring(
        "<Target><TargetOption><TargetCommonOption>"
        f"<Cpu>{cpu}</Cpu>"
        "</TargetCommonOption></TargetOption></Target>"
    )


class WorkspaceRootTests(unittest.TestCase):
    def test_repository_root_comes_from_script_location(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            script = repo_root / "scripts" / "mdk_clangd.py"

            actual = mdk_clangd.repository_root(script)

            self.assertEqual(actual, repo_root.resolve())


class CpuArgumentTests(unittest.TestCase):
    def test_cortex_m0_has_no_fpu_arguments(self) -> None:
        target = make_target('CPUTYPE("Cortex-M0") CLOCK(48000000) ELITTLE')

        args, warnings = mdk_clangd.collect_cpu_args(target)

        self.assertEqual(args, ["-mcpu=cortex-m0", "-mthumb"])
        self.assertEqual(warnings, [])

    def test_cortex_m4_fpu2_uses_single_precision_hard_float(self) -> None:
        target = make_target(
            'CPUTYPE("Cortex-M4") FPU2 CLOCK(12000000) ELITTLE'
        )

        args, warnings = mdk_clangd.collect_cpu_args(target)

        self.assertEqual(
            args,
            [
                "-mcpu=cortex-m4",
                "-mthumb",
                "-mfpu=fpv4-sp-d16",
                "-mfloat-abi=hard",
            ],
        )
        self.assertEqual(warnings, [])

    def test_unknown_cpu_warns_without_inventing_cpu_or_fpu_flags(self) -> None:
        target = make_target('CPUTYPE("Custom-Core") FPU2 ELITTLE')

        args, warnings = mdk_clangd.collect_cpu_args(target)

        self.assertEqual(args, ["-mthumb"])
        self.assertEqual(len(warnings), 2)


class ClangdConfigTests(unittest.TestCase):
    def test_nested_config_provides_compiler_and_extra_flags(self) -> None:
        config = {
            "clangd": {
                "binary": "clang-cl",
                "extra_flags": ["-std=c99", "-DHOST_INDEX=1"],
            }
        }

        compiler, extra_flags = mdk_clangd.clangd_settings(config, None)

        self.assertEqual(compiler, "clang-cl")
        self.assertEqual(extra_flags, ["-std=c99", "-DHOST_INDEX=1"])

    def test_cli_compiler_overrides_config_binary(self) -> None:
        config = {"clangd": {"binary": "clang"}}

        compiler, extra_flags = mdk_clangd.clangd_settings(config, "custom-clang")

        self.assertEqual(compiler, "custom-clang")
        self.assertEqual(extra_flags, [])


if __name__ == "__main__":
    unittest.main()
