"""
Backend Dynamic Workflow Execution & Artifact REST API Routers for NexusAI OS (v0.8.0).
Provides endpoints to create workflows, list dynamic files, fetch raw file contents on-demand,
get execution summaries, and download ZIP archives.

STRICT POLICY: Every endpoint returns a proper 404 if the workflow_id is not found.
NO silent ghost workflow creation. NO hardcoded fallback prompts. EVER.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Path, Response
from pydantic import BaseModel

from nexusai.services.workflow_store import workflow_store

workflow_exec_router = APIRouter(prefix="/workflow", tags=["100% Dynamic Workflow Execution & Artifacts"])


class CreateWorkflowRequest(BaseModel):
    goal_prompt: str
    project_name: Optional[str] = None


@workflow_exec_router.post("/create")
async def create_workflow(payload: CreateWorkflowRequest):
    """Starts autonomous workflow execution for a goal prompt and returns unique workflow_id."""
    print(f"\n[STAGE 1] Incoming Prompt: '{payload.goal_prompt}'")
    if not payload.goal_prompt or not payload.goal_prompt.strip():
        raise HTTPException(status_code=400, detail="goal_prompt must not be empty.")
    wf_id = await workflow_store.create_and_execute_workflow(payload.goal_prompt, payload.project_name)
    print(f"[STAGE 1] Workflow created: {wf_id}")
    return {"status": "STARTED", "workflow_id": wf_id, "goal_prompt": payload.goal_prompt, "message": "Workflow created successfully"}


@workflow_exec_router.get("/{workflow_id}")
async def get_workflow_status(workflow_id: str = Path(...)):
    """Returns workflow execution status and agent states."""
    summary = workflow_store.get_summary(workflow_id)
    if not summary:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found. Submit a goal prompt via POST /create first.")
    return summary.model_dump()


@workflow_exec_router.get("/{workflow_id}/files")
async def get_workflow_files(workflow_id: str = Path(...)):
    """Returns dynamic file tree list for a workflow."""
    files = workflow_store.get_files_list(workflow_id)
    if not files:
        raise HTTPException(status_code=404, detail=f"No files found for workflow '{workflow_id}'. The workflow may not exist or synthesis may have failed.")
    return {"workflow_id": workflow_id, "count": len(files), "files": files}


@workflow_exec_router.get("/{workflow_id}/file/{file_path:path}")
async def get_file_content(workflow_id: str = Path(...), file_path: str = Path(...)):
    """Returns exact raw content of the requested file path on-demand."""
    artifact = workflow_store.get_artifact(workflow_id)
    if not artifact:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found.")
    content = workflow_store.get_file_content(workflow_id, file_path)
    return {"workflow_id": workflow_id, "file_path": file_path, "content": content}


@workflow_exec_router.get("/{workflow_id}/summary")
async def get_workflow_summary(workflow_id: str = Path(...)):
    """Returns comprehensive execution summary metrics."""
    summary = workflow_store.get_summary(workflow_id)
    if not summary:
        raise HTTPException(status_code=404, detail=f"Summary not found for workflow '{workflow_id}'. The workflow may not exist or synthesis may have failed.")
    return summary.model_dump()


@workflow_exec_router.get("/{workflow_id}/artifacts")
async def get_workflow_artifacts(workflow_id: str = Path(...)):
    """Returns all documentation & deployment artifacts for a workflow."""
    art = workflow_store.get_artifact(workflow_id)
    if not art:
        raise HTTPException(status_code=404, detail=f"Artifacts not found for workflow '{workflow_id}'.")
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
    if not workflow_store.get_artifact(workflow_id):
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found for download.")
    zip_bytes = workflow_store.get_zip_bytes(workflow_id)
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={workflow_id}.zip"}
    )
