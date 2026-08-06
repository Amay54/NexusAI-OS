"""
Prediction Engine Metric Classifier for NexusAI OS.
Classifies all metric values into OBSERVED, ESTIMATED, MODEL_PREDICTION, USER_ASSUMPTION, or UNKNOWN to avoid presenting estimates as facts.
"""
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class MetricCategory(str, Enum):
    OBSERVED = "OBSERVED"
    ESTIMATED = "ESTIMATED"
    MODEL_PREDICTION = "MODEL_PREDICTION"
    USER_ASSUMPTION = "USER_ASSUMPTION"
    UNKNOWN = "UNKNOWN"


class ClassifiedMetric(BaseModel):
    name: str
    value: Any
    category: MetricCategory
    explanation: str


class PredictionMetricClassifier:
    """Classifies metrics according to empirical certainty."""

    def classify(self, name: str, value: Any, category: MetricCategory, explanation: str) -> ClassifiedMetric:
        return ClassifiedMetric(
            name=name,
            value=value,
            category=category,
            explanation=explanation
        )


metric_classifier = PredictionMetricClassifier()
