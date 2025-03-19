from dataclasses import dataclass
from enum import Enum


@dataclass
class ModelMetadata:
    """Struct-like class to store additional information about an instantated model."""

    name: str
    id: str
    created_via: Enum

    network_defintion: object

    backend_used: Enum
    misc: dict


class ERequestType(Enum):
    """Enumeration of 'valid' sources from where a model is instantiated from."""

    NETWORK = "network"

    NESTOR_VARIANT = "variant"

    EXCHANGE_FORMAT = "file"


class ENestorVariant(Enum):
    """Enumeration of available variants (i.e., different model versions) of the Nestor-BayesianNetworks."""

    WEIGHTED = 1

    UN_WEIGHTED = 2

    FULL_COGNITIVE = 3


class EBackend(Enum):
    """Enumeration of currently supported third-party libraries (i.e., used actively in the code)."""

    PGMPY = "pgmpy"

    PYAGRUM = "pyagrum"
