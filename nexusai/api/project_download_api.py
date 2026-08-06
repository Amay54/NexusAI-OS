"""
Project Download ZIP REST API Router for NexusAI OS (v0.5.1).
Packages synthesized multi-file software projects into a downloadable zip archive.
"""
import io
import zipfile
from typing import Any, Dict
from fastapi import APIRouter, HTTPException, Path, Response

from nexusai.services.project_synthesizer import project_synthesizer

download_router = APIRouter(prefix="/projects", tags=["Project Download & Export"])


@download_router.get("/download/{project_id}")
async def download_project_zip(project_id: str = Path(...)):
    """Packages synthesized codebase into a downloadable .zip archive."""
    artifact = await project_synthesizer.synthesize_full_project(
        project_name="NexusAI_Synthesized_Project",
        goal_prompt="Build production software codebase"
    )

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # 1. Add synthesized code files
        for filename, content in artifact.files.items():
            zip_file.writestr(filename, content)

        # 2. Add Docker & Docs
        zip_file.writestr("Dockerfile", artifact.dockerfile)
        zip_file.writestr("docker-compose.yml", artifact.docker_compose_yml)
        zip_file.writestr("README.md", artifact.readme_md)
        zip_file.writestr("docs/ADR-001.md", artifact.adr_md)

    zip_buffer.seek(0)
    filename = f"{artifact.project_name.lower().replace(' ', '_')}.zip"

    return Response(
        content=zip_buffer.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
