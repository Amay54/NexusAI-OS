"""
Backend Dynamic Workflow Execution & Artifact REST API Routers for NexusAI OS (v0.6.0).
Provides endpoints to create workflows, list dynamic files, fetch raw file contents on-demand, get execution summaries, and download ZIP archives.
"""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Path, Query, Response
from pydantic import BaseModel, Field

from nexusai.services.workflow_store import workflow_store

workflow_exec_router = APIRouter(prefix="/workflow", tags=["100% Dynamic Workflow Execution & Artifacts"])


class CreateWorkflowRequest(BaseModel):
    goal_prompt: str
    project_name: Optional[str] = None


@workflow_exec_router.post("/create")
async def create_workflow(payload: CreateWorkflowRequest):
    """Starts autonomous workflow execution for a goal prompt and returns unique workflow_id."""
    wf_id = await workflow_store.create_and_execute_workflow(payload.goal_prompt, payload.project_name)
    return {"status": "STARTED", "workflow_id": wf_id, "message": "Workflow created successfully"}


@workflow_exec_router.get("/{workflow_id}")
async def get_workflow_status(workflow_id: str = Path(...)):
    """Returns workflow execution status and agent states."""
    summary = workflow_store.get_summary(workflow_id)
    if not summary:
        raise HTTPException(status_code=404, detail=f"Workflow #{workflow_id} not found")
    return summary.model_dump()


@workflow_exec_router.get("/{workflow_id}/files")
async def get_workflow_files(workflow_id: str = Path(...)):
    """Returns dynamic file tree list for a workflow."""
    files = workflow_store.get_files_list(workflow_id)
    if not files:
        # Fallback to default if not found
        await workflow_store.create_and_execute_workflow("Build default FastAPI project", "DefaultProject")
        files = workflow_store.get_files_list(workflow_id)
    return {"workflow_id": workflow_id, "count": len(files), "files": files}


@workflow_exec_router.get("/{workflow_id}/file/{file_path:path}")
async def get_file_content(workflow_id: str = Path(...), file_path: str = Path(...)):
    """Returns exact raw content of the requested file path on-demand."""
    content = workflow_store.get_file_content(workflow_id, file_path)
    return {"workflow_id": workflow_id, "file_path": file_path, "content": content}


@workflow_exec_router.get("/{workflow_id}/summary")
async def get_workflow_summary(workflow_id: str = Path(...)):
    """Returns comprehensive execution summary metrics."""
    summary = workflow_store.get_summary(workflow_id)
    if not summary:
        # Auto-create if default lookup
        await workflow_store.create_and_execute_workflow("Build FastAPI Inventory System", "InventorySystem")
        summary = workflow_store.get_summary(workflow_id)
    return summary.model_dump()


@workflow_exec_router.get("/{workflow_id}/artifacts")
async def get_workflow_artifacts(workflow_id: str = Path(...)):
    """Returns all documentation & deployment artifacts for a workflow."""
    art = workflow_store.get_artifact(workflow_id)
    if not art:
        raise HTTPException(status_code=404, detail="Artifacts not found")
    return {
        "readme_md": art.readme_md,
        "dockerfile": art.dockerfile,
        "docker_compose_yml": art.docker_compose_yml,
        "adr_md": art.adr_md,
        "quality_score": art.quality_score
    }


@workflow_exec_router.get("/{workflow_id}/download")
async def download_workflow_zip(workflow_id: str = Path(...)):
    """Downloads ZIP archive of the specific workflow project files."""
    zip_bytes = workflow_store.get_zip_bytes(workflow_id)
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={workflow_id}.zip"}
    )
