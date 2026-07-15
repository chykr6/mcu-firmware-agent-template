import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

import mdk_common  # noqa: E402


class ToolchainConfigTests(unittest.TestCase):
    def test_load_toolchain_reads_nested_mdk_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "toolchain.local.json"
            config_path.write_text(
                json.dumps({"mdk": {"uv4_dir": "D:/devtool/Keil5/UV4"}}),
                encoding="utf-8",
            )

            config = mdk_common.load_toolchain(config_path)

            self.assertEqual(config["mdk"]["uv4_dir"], "D:/devtool/Keil5/UV4")

    def test_find_uv4_uses_uvision_com_from_local_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            uv4_dir = Path(tmp) / "UV4"
            uv4_dir.mkdir()
            expected = uv4_dir / "uVision.com"
            expected.touch()

            with patch.object(
                mdk_common,
                "load_toolchain",
                return_value={"mdk": {"uv4_dir": str(uv4_dir)}},
            ):
                actual = mdk_common.find_uv4()

            self.assertEqual(actual, expected.resolve())


if __name__ == "__main__":
    unittest.main()
