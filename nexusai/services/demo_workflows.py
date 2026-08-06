"""
Built-In Demo Workflows Engine for NexusAI OS (v0.4.0).
Provides pre-configured production demonstration workflows ready for immediate dashboard execution.
"""
from typing import Any, Dict, List
from pydantic import BaseModel, Field

from nexusai.services.project_synthesizer import project_synthesizer, ProductionProjectArtifact


class DemoWorkflowSpec(BaseModel):
    demo_id: str
    title: str
    description: str
    category: str
    estimated_duration_sec: float
    goal_prompt: str


class DemoWorkflowsRegistry:
    """Registry and manager for built-in demonstration workflows."""

    def __init__(self):
        self.demos: List[DemoWorkflowSpec] = [
            DemoWorkflowSpec(
                demo_id="demo_inventory_system",
                title="FastAPI Inventory Management System",
                description="Production CRUD inventory system with Pydantic validation, Docker compose stack, and Pytest coverage.",
                category="Enterprise SaaS",
                estimated_duration_sec=35.0,
                goal_prompt="Build a FastAPI Inventory Management System with items CRUD, PostgreSQL schema, Docker compose, and unit tests."
            ),
            DemoWorkflowSpec(
                demo_id="demo_blog_platform",
                title="Blog Platform REST API",
                description="Blogging microservice API supporting post publishing, tags, author authorization, and OpenAPI specs.",
                category="Content Management",
                estimated_duration_sec=30.0,
                goal_prompt="Build a Blog Platform API with posts CRUD, author authorization, tag searching, and unit tests."
            ),
            DemoWorkflowSpec(
                demo_id="demo_crm_backend",
                title="Customer Relationship Management (CRM) Backend",
                description="Enterprise CRM backend with lead tracking, deal pipelines, contact management, and database migrations.",
                category="Enterprise SaaS",
                estimated_duration_sec=40.0,
                goal_prompt="Build a CRM Backend API with customer leads, contact histories, pipeline stages, and unit tests."
            ),
            DemoWorkflowSpec(
                demo_id="demo_auth_service",
                title="OAuth2 JWT Authentication Microservice",
                description="Secure authentication microservice featuring password bcrypt hashing, OAuth2 token issuance, and rate limiting.",
                category="Security",
                estimated_duration_sec=25.0,
                goal_prompt="Build an OAuth2 JWT Authentication microservice with user registration, login, token refresh, and bcrypt hashing."
            ),
            DemoWorkflowSpec(
                demo_id="demo_rest_microservice",
                title="Generic REST API Microservice",
                description="Clean architecture REST API template with health monitoring, CORS middleware, and Docker deployment.",
                category="Microservices",
                estimated_duration_sec=20.0,
                goal_prompt="Build a production REST API microservice with health checks, Pydantic schemas, and Docker configuration."
            )
        ]

    def list_demo_workflows(self) -> List[DemoWorkflowSpec]:
        return self.demos

    async def execute_demo_workflow(self, demo_id: str) -> ProductionProjectArtifact:
        """Executes selected demonstration workflow end-to-end."""
        demo = next((d for d in self.demos if d.demo_id == demo_id), None)
        if not demo:
            demo = self.demos[0]

        artifact = await project_synthesizer.synthesize_full_project(
            project_name=demo.title,
            goal_prompt=demo.goal_prompt,
            workflow_id=abs(hash(demo_id)) % 1000 + 500
        )
        return artifact


demo_workflows_registry = DemoWorkflowsRegistry()
