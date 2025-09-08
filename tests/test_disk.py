from __future__ import annotations

import json
import subprocess
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "awesome-disk"


def test_json_output() -> None:
    result = subprocess.check_output(["uv", "run", str(SCRIPT), "--once"])
    info = json.loads(result)
    assert {"total", "used", "free", "percent"} <= info.keys()


def test_format_output() -> None:
    result = subprocess.check_output(
        ["uv", "run", str(SCRIPT), "--once", "--format", "{percent}"]
    )
    assert result.decode().strip().isdigit()
