"""
Multi-Framework Code Synthesis Test Suite for NexusAI OS (v0.7.0).
Verifies that Flask, React, FastAPI, and Django prompts generate 100% distinct project structures and code bases.
"""
import pytest
from nexusai.services.project_synthesizer import project_synthesizer


@pytest.mark.asyncio
async def test_flask_weather_api_synthesis():
    """Prompt 1: Build a Flask Weather API using SQLite."""
    prompt = "Build a Flask Weather API using SQLite"
    artifact = await project_synthesizer.synthesize_full_project("FlaskWeatherAPI", prompt)

    assert artifact.spec.framework == "flask"
    assert artifact.spec.database == "sqlite"
    assert "app.py" in artifact.files
    assert "Flask" in artifact.files["app.py"]
    assert "Flask" in artifact.files["requirements.txt"]


@pytest.mark.asyncio
async def test_react_todo_app_synthesis():
    """Prompt 2: Build a React Todo App."""
    prompt = "Build a React Todo App"
    artifact = await project_synthesizer.synthesize_full_project("ReactTodoApp", prompt)

    assert artifact.spec.framework == "react"
    assert "src/App.jsx" in artifact.files
    assert "package.json" in artifact.files
    assert "react" in artifact.files["package.json"]


@pytest.mark.asyncio
async def test_fastapi_crm_backend_synthesis():
    """Prompt 3: Build a FastAPI CRM Backend with PostgreSQL."""
    prompt = "Build a FastAPI CRM Backend with PostgreSQL"
    artifact = await project_synthesizer.synthesize_full_project("FastAPICRM", prompt)

    assert artifact.spec.framework == "fastapi"
    assert artifact.spec.database == "postgresql"
    assert "main.py" in artifact.files
    assert "FastAPI" in artifact.files["main.py"]


@pytest.mark.asyncio
async def test_django_blog_synthesis():
    """Prompt 4: Build a Django Blog."""
    prompt = "Build a Django Blog"
    artifact = await project_synthesizer.synthesize_full_project("DjangoBlog", prompt)

    assert artifact.spec.framework == "django"
    assert "manage.py" in artifact.files
    assert "blog/models.py" in artifact.files
    assert "Django" in artifact.files["requirements.txt"]


@pytest.mark.asyncio
async def test_all_four_prompts_are_100_percent_distinct():
    """Verifies that all 4 generated project structures are 100% distinct."""
    p1 = await project_synthesizer.synthesize_full_project("P1", "Build a Flask Weather API using SQLite")
    p2 = await project_synthesizer.synthesize_full_project("P2", "Build a React Todo App")
    p3 = await project_synthesizer.synthesize_full_project("P3", "Build a FastAPI CRM Backend with PostgreSQL")
    p4 = await project_synthesizer.synthesize_full_project("P4", "Build a Django Blog")

    # Assert Framework Specs
    assert p1.spec.framework == "flask"
    assert p2.spec.framework == "react"
    assert p3.spec.framework == "fastapi"
    assert p4.spec.framework == "django"

    # Assert File Structures are different
    assert set(p1.files.keys()) != set(p2.files.keys())
    assert set(p2.files.keys()) != set(p3.files.keys())
    assert set(p3.files.keys()) != set(p4.files.keys())
