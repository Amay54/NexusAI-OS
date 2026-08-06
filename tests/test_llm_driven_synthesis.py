"""
100% LLM-Driven Synthesis Test Suite for NexusAI OS (v0.8.0).
Verifies that project_synthesizer routes through IntelligentRouter, passes Quality Gates, and throws errors without static fallback templates on failure.
"""
import pytest
from nexusai.services.project_synthesizer import project_synthesizer


@pytest.mark.asyncio
async def test_llm_driven_flask_synthesis():
    """Verify Flask Weather API synthesis via IntelligentRouter."""
    prompt = "Build a Flask Weather API using SQLite"
    artifact = await project_synthesizer.synthesize_full_project("LLM_Flask", prompt)

    assert artifact.spec.framework == "flask"
    assert "app.py" in artifact.files
    assert "flask" in artifact.files["app.py"].lower()


@pytest.mark.asyncio
async def test_llm_driven_react_synthesis():
    """Verify React Todo App synthesis via IntelligentRouter."""
    prompt = "Build a React Todo App"
    artifact = await project_synthesizer.synthesize_full_project("LLM_React", prompt)

    assert artifact.spec.framework == "react"
    assert "package.json" in artifact.files
    assert "react" in artifact.files["package.json"]


@pytest.mark.asyncio
async def test_llm_driven_fastapi_synthesis():
    """Verify FastAPI CRM Backend synthesis via IntelligentRouter."""
    prompt = "Build a FastAPI CRM Backend with PostgreSQL"
    artifact = await project_synthesizer.synthesize_full_project("LLM_FastAPI", prompt)

    assert artifact.spec.framework == "fastapi"
    assert "main.py" in artifact.files
    assert "fastapi" in artifact.files["main.py"].lower()


@pytest.mark.asyncio
async def test_llm_driven_cli_synthesis():
    """Verify CLI Application synthesis (no Flask or FastAPI)."""
    prompt = "Build a Python CLI application for file encryption"
    artifact = await project_synthesizer.synthesize_full_project("LLM_CLI", prompt)

    assert artifact.spec.framework == "cli"
    assert "cli.py" in artifact.files
    all_code = "".join(artifact.files.values()).lower()
    assert "flask" not in all_code
    assert "fastapi" not in all_code


@pytest.mark.asyncio
async def test_llm_failure_raises_error_without_static_template_fallback():
    """Verifies that invalid LLM responses raise a ValueError and do NOT return a static fallback template."""
    flask_spec = project_synthesizer.parse_spec_from_prompt("FailTest", "Build a Flask App")
    bad_files = {"app.py": "print('Hello world')"}  # Completely missing Flask import

    with pytest.raises(ValueError) as exc_info:
        project_synthesizer.validate_framework_match(flask_spec, bad_files)

    assert "Quality Gate Failed" in str(exc_info.value)
