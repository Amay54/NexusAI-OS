"""
Benchmark Test Suite & Performance Instrumentation for NexusAI OS (v0.2.1).
Measures latency for Memory Retrieval, Graph Traversal, Vector Search, Context Compression, and Concurrent Requests,
generating a markdown report in docs/benchmarks/benchmark_report.md.
"""
import asyncio
import os
import time
import pytest

from nexusai.memory.manager import MemoryManager
from nexusai.memory.base import MemoryItem, ImportanceLevel
from nexusai.memory.retrieval import ContextRetrievalEngine
from nexusai.memory.context_budget import ContextBudgetManager
from nexusai.services.knowledge_graph import KnowledgeGraphService, InMemoryGraphProvider


@pytest.mark.asyncio
async def test_performance_benchmarks():
    """Executes benchmarks across Memory, Graph, Compression, and Concurrency."""
    results = {}

    # 1. Benchmark Vector Search Latency
    mem_mgr = MemoryManager()
    for i in range(100):
        await mem_mgr.store_experience(f"bench-exp-{i}", f"Lesson {i}: Always benchmark async database and memory operations.")

    start_v = time.time()
    search_res = await mem_mgr.long_term.search("async database memory operations", top_k=10)
    v_latency_ms = round((time.time() - start_v) * 1000, 2)
    results["vector_search_latency_ms"] = v_latency_ms
    assert len(search_res) > 0

    # 2. Benchmark Graph Traversal Latency
    kg = KnowledgeGraphService(provider=InMemoryGraphProvider())
    await kg.add_node("proj-bench", "Project")
    for i in range(50):
        t_id = f"task-bench-{i}"
        await kg.add_node(t_id, "Task")
        await kg.add_edge("proj-bench", t_id, "HAS_TASK")

    start_g = time.time()
    graph_rels = await kg.query_relationships("proj-bench")
    g_latency_ms = round((time.time() - start_g) * 1000, 2)
    results["graph_query_latency_ms"] = g_latency_ms
    assert len(graph_rels) == 50

    # 3. Benchmark Context Compression Latency
    budget_mgr = ContextBudgetManager(max_char_budget=1000)
    items = [
        MemoryItem(memory_id=f"m-{i}", content=f"Memory content sample {i} with long description text for compression testing.", importance_level=ImportanceLevel.HIGH)
        for i in range(30)
    ]

    start_c = time.time()
    compressed = budget_mgr.optimize_context(items, query="sample compression")
    c_latency_ms = round((time.time() - start_c) * 1000, 2)
    results["compression_latency_ms"] = c_latency_ms
    assert compressed["packed_count"] <= 30

    # 4. Benchmark Concurrent Memory Retrieval Requests
    ret_engine = ContextRetrievalEngine()

    async def single_retrieval(req_id: int):
        return await ret_engine.build_compressed_context(f"Agent-{req_id}", "Benchmark query for memory retrieval")

    start_conc = time.time()
    concurrent_results = await asyncio.gather(*[single_retrieval(i) for i in range(20)])
    conc_latency_ms = round((time.time() - start_conc) * 1000, 2)
    results["concurrent_20_requests_latency_ms"] = conc_latency_ms
    assert len(concurrent_results) == 20

    # Write Markdown Benchmark Report
    report_md = (
        "# NexusAI OS Performance Benchmark Report (v0.2.1)\n\n"
        f"- **Vector Search Latency (100 docs)**: `{v_latency_ms} ms`\n"
        f"- **Knowledge Graph Query Latency (50 edges)**: `{g_latency_ms} ms`\n"
        f"- **Context Budget Compression Latency (30 items)**: `{c_latency_ms} ms`\n"
        f"- **Concurrent Retrieval Latency (20 requests)**: `{conc_latency_ms} ms` (`{round(conc_latency_ms / 20, 2)} ms/req`)\n"
    )

    report_path = os.path.join("docs", "benchmarks", "benchmark_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)

    assert os.path.exists(report_path)
