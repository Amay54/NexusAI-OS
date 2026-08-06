"""
Observability Metrics Instrumentation for NexusAI OS.
Tracks operational metrics (retrieval latency, cache hit ratio, vector search latency, compression time, graph query latency).
"""
import time
from typing import Any, Dict, List


class ObservabilityMetricsTracker:
    """Central metrics collector for Prometheus/Grafana dashboards."""

    def __init__(self):
        self.metrics: Dict[str, List[float]] = {
            "retrieval_latency_ms": [],
            "vector_search_latency_ms": [],
            "compression_time_ms": [],
            "graph_query_latency_ms": [],
        }
        self.cache_hits = 0
        self.cache_misses = 0

    def record_metric(self, name: str, value_ms: float) -> None:
        if name in self.metrics:
            self.metrics[name].append(value_ms)

    def record_cache_event(self, hit: bool) -> None:
        if hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

    def get_metrics_summary(self) -> Dict[str, Any]:
        total_cache = self.cache_hits + self.cache_misses
        hit_ratio = round((self.cache_hits / max(total_cache, 1)) * 100, 2)

        summary = {
            "cache_hit_ratio_percent": hit_ratio,
            "cache_total_requests": total_cache,
            "metrics": {}
        }

        for k, v in self.metrics.items():
            avg_val = round(sum(v) / len(v), 2) if v else 0.0
            summary["metrics"][k] = {
                "count": len(v),
                "avg_ms": avg_val,
                "max_ms": max(v, default=0.0)
            }

        return summary


metrics_tracker = ObservabilityMetricsTracker()
