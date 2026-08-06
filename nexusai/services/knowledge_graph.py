"""
Generic Knowledge Graph Engine for NexusAI OS.
Abstracts graph backend implementations (InMemory, Neo4j, NetworkX) behind a clean generic interface.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class GraphNode(BaseModel):
    id: str
    label: str  # Project, Task, File, Agent, Deployment, API, Database
    properties: Dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    source_id: str
    target_id: str
    relation: str  # HAS_TASK, TOUCHES_FILE, DEPLOYED_TO, EXPOSES_API, DEPENDS_ON


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
    """High-performance in-memory graph provider."""

    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[GraphEdge] = []

    async def add_node(self, node_id: str, label: str, properties: Optional[Dict[str, Any]] = None) -> GraphNode:
        node = GraphNode(id=node_id, label=label, properties=properties or {})
        self.nodes[node_id] = node
        return node

    async def add_edge(self, source_id: str, target_id: str, relation: str) -> GraphEdge:
        edge = GraphEdge(source_id=source_id, target_id=target_id, relation=relation)
        self.edges.append(edge)
        return edge

    async def query_relationships(self, subject_id: str, relation: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        for edge in self.edges:
            if edge.source_id == subject_id and (relation is None or edge.relation == relation):
                target_node = self.nodes.get(edge.target_id)
                if target_node:
                    results.append({
                        "relation": edge.relation,
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

    async def add_node(self, node_id: str, label: str, properties: Optional[Dict[str, Any]] = None) -> GraphNode:
        return await self.provider.add_node(node_id, label, properties)

    async def add_edge(self, source_id: str, target_id: str, relation: str) -> GraphEdge:
        return await self.provider.add_edge(source_id, target_id, relation)

    async def query_relationships(self, subject_id: str, relation: Optional[str] = None) -> List[Dict[str, Any]]:
        return await self.provider.query_relationships(subject_id, relation)

    async def get_full_graph_topology(self) -> Dict[str, Any]:
        return await self.provider.get_full_graph_topology()


knowledge_graph = KnowledgeGraphService()
