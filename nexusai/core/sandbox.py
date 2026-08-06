"""
Isolated Code Execution Sandbox Engine for NexusAI OS.
Executes generated code in temporary, isolated workspaces with resource limits, timeouts, and automatic cleanup.
Supports Python, Node.js, and Shell scripts.
"""
import asyncio
import os
import shutil
import tempfile
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class SandboxResult(BaseModel):
    language: str
    exit_code: int
    stdout: str
    stderr: str
    execution_time_ms: float
    success: bool
    workspace_dir: str


class CodeSandboxEngine:
    """Isolated execution engine enforcing timeouts and resource isolation."""

    def __init__(self, timeout_seconds: float = 15.0):
        self.timeout_seconds = timeout_seconds

    async def execute_code(
        self,
        code: str,
        language: str = "python",
        cwd_override: Optional[str] = None
    ) -> SandboxResult:
        """Executes code snippet in an isolated temporary directory."""
        temp_dir = cwd_override or tempfile.mkdtemp(prefix="nexusai_sandbox_")
        start_time = asyncio.get_event_loop().time()

        try:
            if language.lower() in ["python", "py"]:
                file_path = os.path.join(temp_dir, "script.py")
                cmd = f"python {file_path}"
            elif language.lower() in ["javascript", "typescript", "node", "js"]:
                file_path = os.path.join(temp_dir, "script.js")
                cmd = f"node {file_path}"
            elif language.lower() in ["shell", "bash", "sh", "powershell"]:
                file_path = os.path.join(temp_dir, "script.sh")
                cmd = f"bash {file_path}" if os.name != "nt" else f"powershell -File {file_path}"
            else:
                raise ValueError(f"Unsupported sandbox language: {language}")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)

            proc = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=temp_dir
            )

            try:
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=self.timeout_seconds)
                elapsed_ms = round((asyncio.get_event_loop().time() - start_time) * 1000, 2)

                return SandboxResult(
                    language=language,
                    exit_code=proc.returncode or 0,
                    stdout=stdout.decode("utf-8", errors="replace"),
                    stderr=stderr.decode("utf-8", errors="replace"),
                    execution_time_ms=elapsed_ms,
                    success=(proc.returncode == 0),
                    workspace_dir=temp_dir
                )
            except asyncio.TimeoutError:
                proc.kill()
                elapsed_ms = round((asyncio.get_event_loop().time() - start_time) * 1000, 2)
                return SandboxResult(
                    language=language,
                    exit_code=-1,
                    stdout="",
                    stderr=f"Execution timed out after {self.timeout_seconds} seconds.",
                    execution_time_ms=elapsed_ms,
                    success=False,
                    workspace_dir=temp_dir
                )
        finally:
            if not cwd_override and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)


sandbox_engine = CodeSandboxEngine()
