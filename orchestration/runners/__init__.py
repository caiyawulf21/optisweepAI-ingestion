from __future__ import annotations

import subprocess
import sys
from pathlib import Path


class CommandError(RuntimeError):
    def __init__(self, command: list[str], returncode: int, stdout: str, stderr: str) -> None:
        self.command = command
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        super().__init__(
            f"Command failed ({returncode}): {' '.join(command)}\n{stderr or stdout}"
        )


def run_python_script(
    script: Path,
    args: list[str],
    *,
    cwd: Path | None = None,
) -> str:
    command = [sys.executable, str(script), *args]
    completed = subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        check=False,
    )
    output = (completed.stdout or "") + (completed.stderr or "")
    if completed.returncode != 0:
        raise CommandError(command, completed.returncode, completed.stdout or "", completed.stderr or "")
    return output.strip()
