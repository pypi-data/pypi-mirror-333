import time
from dataclasses import dataclass
from enum import Enum

current_timestamp = time.time()


@dataclass
class ReportEntry:
    """Struct-like class to store reporting results for one metric."""

    metric: Enum
    report_origin: Enum
    data: object  # preferably a dict(str, any)
    timestamp: float
    scope: Enum
    scoped_name: str
    misc: object


class EReportScope(Enum):
    NODE_LEVEL = "node"
    EDGE_LEVEL = "edge"
    CLUSTER_LEVEL = "cluster"
    NETWORK_LEVEL = "network"


class EReportOrigin(Enum):
    """Enumeration of data origins that can be visualizd."""

    DOWHY_REPORTER = "dowhy"
    BASIC_REPORTER = "basic"


class EBasicReportMetric(Enum):
    """Enumeration of available metrics that can be provided via the Basic-reporting feature."""

    ADJECENCY_MATRIX = "adjecency"
    MARKOV_BLANKET = "blankets"
    CONNECTIVITY = "connectivity"


class EDoWhyReportMetric(Enum):
    """Enumeration of available metrics that can be provided via the doWhy-reporting feature."""

    INTRINSIC_CAUSAL_INFLUENCE = "iic"
    PARENTAL_FEATURE_RELEVANCE = "relevance"
    DIRECT_EFFECT = "direct"
    AVERAGE_CAUSAL_EFFECT = "ace"
    NATURAL_DIRECT_EFFECT = "nde"
    NATURAL_INDIRECT_EFFECT = "nie"
