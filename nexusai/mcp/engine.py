"""
Adaptive MCP Discovery Engine for NexusAI OS.
Automatically discovers MCP servers and plugins, parses metadata, generates embeddings, and indexes tools into ToolRegistry.
"""
import logging
from typing import Any, Dict, List
from nexusai.memory.embeddings import embedding_service
from nexusai.mcp.registry import ToolMetadata, RiskLevel, tool_registry

logger = logging.getLogger("nexusai.mcp_engine")

# Core built-in MCP Tool Catalog definition
BUILTIN_MCP_TOOLS = [
    {
        "tool_id": "mcp_filesystem_read",
        "tool_name": "Filesystem Reader",
        "provider": "mcp-filesystem",
        "description": "Reads contents of local workspace files safely.",
        "parameters": {"path": "string", "start_line": "integer", "end_line": "integer"},
        "permissions": ["READ_FS"],
        "risk_level": RiskLevel.LOW,
        "supported_agents": ["Developer Agent", "QA Agent", "Documentation Agent"]
    },
    {
        "tool_id": "mcp_filesystem_write",
        "tool_name": "Filesystem Writer",
        "provider": "mcp-filesystem",
        "description": "Creates or updates code and text files in local workspace.",
        "parameters": {"path": "string", "content": "string"},
        "permissions": ["WRITE_FS"],
        "risk_level": RiskLevel.MEDIUM,
        "supported_agents": ["Developer Agent", "Documentation Agent"]
    },
    {
        "tool_id": "mcp_terminal_exec",
        "tool_name": "Terminal Command Runner",
        "provider": "mcp-terminal",
        "description": "Executes shell commands in isolated sandbox terminal environment.",
        "parameters": {"command": "string", "timeout": "float"},
        "permissions": ["EXECUTE_COMMAND"],
        "risk_level": RiskLevel.HIGH,
        "supported_agents": ["DevOps Agent", "Developer Agent"]
    },
    {
        "tool_id": "mcp_docker_container",
        "tool_name": "Docker Container Manager",
        "provider": "mcp-docker",
        "description": "Manages ephemeral Docker containers, builds, and logs.",
        "parameters": {"action": "string", "image": "string"},
        "permissions": ["DOCKER_CONTROL"],
        "risk_level": RiskLevel.HIGH,
        "supported_agents": ["DevOps Agent"]
    },
    {
        "tool_id": "mcp_postgres_query",
        "tool_name": "PostgreSQL Query Execution",
        "provider": "mcp-postgres",
        "description": "Executes SQL migrations, schema updates, and database queries.",
        "parameters": {"sql": "string"},
        "permissions": ["DB_WRITE"],
        "risk_level": RiskLevel.HIGH,
        "supported_agents": ["Database Agent"]
    },
    {
        "tool_id": "mcp_github_commit",
        "tool_name": "GitHub PR & Commit Creator",
        "provider": "mcp-github",
        "description": "Pushes code changes, creates branches, and opens pull requests.",
        "parameters": {"repo": "string", "branch": "string", "message": "string"},
        "permissions": ["GIT_PUSH"],
        "risk_level": RiskLevel.MEDIUM,
        "supported_agents": ["Developer Agent", "DevOps Agent"]
    }
]


class AdaptiveDiscoveryEngine:
    """Automatic tool discovery and vector embedding indexing service."""

    def __init__(self):
        self.registry = tool_registry
        self.embed_svc = embedding_service

    async def discover_and_index_all_tools(self) -> List[ToolMetadata]:
        """Discovers all MCP tools, generates vector embeddings, and registers into KB."""
        logger.info("Starting Adaptive MCP Tool Discovery & Vector Indexing...")
        discovered = []

        for tool_def in BUILTIN_MCP_TOOLS:
            embedding = await self.embed_svc.embed_text(
                f"{tool_def['tool_name']} {tool_def['description']} {tool_def['provider']}"
            )

            meta = ToolMetadata(
                tool_id=tool_def["tool_id"],
                tool_name=tool_def["tool_name"],
                provider=tool_def["provider"],
                description=tool_def["description"],
                parameters=tool_def["parameters"],
                permissions=tool_def["permissions"],
                risk_level=tool_def["risk_level"],
                supported_agents=tool_def["supported_agents"],
                embedding=embedding
            )

            self.registry.register_tool(meta)
            discovered.append(meta)

        logger.info(f"Discovered and indexed {len(discovered)} MCP tools into Knowledge Base.")
        return discovered


discovery_engine = AdaptiveDiscoveryEngine()
