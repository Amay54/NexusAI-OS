"""
Generic Knowledge Graph Engine for NexusAI OS.
Abstracts graph backend implementations (InMemory, Neo4j, NetworkX) behind a clean generic interface.
Supports node and relationship metadata (owner, confidence, workflow_id, tags, timestamp).
"""
from abc import ABC, abstractmethod
from datetime import datetime, timezone
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class GraphNode(BaseModel):
    id: str
    label: str  # Project, Task, File, Agent, Deployment, API, Database
    node_type: str = "ENTITY"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    owner: str = "SYSTEM"
    confidence: float = 1.0
    tags: List[str] = Field(default_factory=list)
    properties: Dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_id: str
    target_id: str
    relation: str  # HAS_TASK, TOUCHES_FILE, DEPLOYED_TO, EXPOSES_API, DEPENDS_ON
    created_by: str = "SYSTEM"
    workflow_id: Optional[int] = None
    confidence: float = 1.0
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class BaseKnowledgeGraphProvider(ABC):
    """Abstract interface for knowledge graph backends."""

    @abstractmethod
    async def add_node(self, node_id: str, label: str, properties: Optional[Dict[str, Any]] = None) -> GraphNode:
        pass

    @abstractmethod
    async def add_edge(self, source_id: str, target_id: str, relation: str) -> GraphEdge:
        pass

    @abstractmethod
    async def query_relationships(self, subject_id: str, relation: Optional[str] = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_full_graph_topology(self) -> Dict[str, Any]:
        pass


class InMemoryGraphProvider(BaseKnowledgeGraphProvider):
    """High-performance in-memory graph provider with metadata support."""

    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[GraphEdge] = []

    async def add_node(
        self,
        node_id: str,
        label: str,
        properties: Optional[Dict[str, Any]] = None,
        node_type: str = "ENTITY",
        owner: str = "SYSTEM",
        confidence: float = 1.0,
        tags: Optional[List[str]] = None
    ) -> GraphNode:
        node = GraphNode(
            id=node_id,
            label=label,
            node_type=node_type,
            owner=owner,
            confidence=confidence,
            tags=tags or [],
            properties=properties or {}
        )
        self.nodes[node_id] = node
        return node

    async def add_edge(
        self,
        source_id: str,
        target_id: str,
        relation: str,
        created_by: str = "SYSTEM",
        workflow_id: Optional[int] = None,
        confidence: float = 1.0
    ) -> GraphEdge:
        edge = GraphEdge(
            source_id=source_id,
            target_id=target_id,
            relation=relation,
            created_by=created_by,
            workflow_id=workflow_id,
            confidence=confidence
        )
        self.edges.append(edge)
        return edge

    async def query_relationships(self, subject_id: str, relation: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        for edge in self.edges:
            if edge.source_id == subject_id and (relation is None or edge.relation == relation):
                target_node = self.nodes.get(edge.target_id)
                if target_node:
                    results.append({
                        "edge_id": edge.id,
                        "relation": edge.relation,
                        "workflow_id": edge.workflow_id,
                        "confidence": edge.confidence,
                        "target_node": target_node.model_dump()
                    })
        return results

    async def get_full_graph_topology(self) -> Dict[str, Any]:
        return {
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "nodes": [n.model_dump() for n in self.nodes.values()],
            "edges": [e.model_dump() for e in self.edges]
        }


class KnowledgeGraphService:
    """Provider-agnostic Knowledge Graph Service."""

    def __init__(self, provider: Optional[BaseKnowledgeGraphProvider] = None):
        self.provider = provider or InMemoryGraphProvider()

    def set_provider(self, provider: BaseKnowledgeGraphProvider) -> None:
        self.provider = provider

    async def add_node(self, node_id: str, label: str, properties: Optional[Dict[str, Any]] = None, **kwargs) -> GraphNode:
        if isinstance(self.provider, InMemoryGraphProvider):
            return await self.provider.add_node(node_id, label, properties, **kwargs)
        return await self.provider.add_node(node_id, label, properties)

    async def add_edge(self, source_id: str, target_id: str, relation: str, **kwargs) -> GraphEdge:
        if isinstance(self.provider, InMemoryGraphProvider):
            return await self.provider.add_edge(source_id, target_id, relation, **kwargs)
        return await self.provider.add_edge(source_id, target_id, relation)

    async def query_relationships(self, subject_id: str, relation: Optional[str] = None) -> List[Dict[str, Any]]:
        return await self.provider.query_relationships(subject_id, relation)

    async def get_full_graph_topology(self) -> Dict[str, Any]:
        return await self.provider.get_full_graph_topology()


knowledge_graph = KnowledgeGraphService()
