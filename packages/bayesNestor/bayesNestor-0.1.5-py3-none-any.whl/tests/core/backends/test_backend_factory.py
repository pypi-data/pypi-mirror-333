import uuid
from unittest.mock import Mock, patch

import pytest

from bayesnestor.core.backends.BackendFactory import BackendFactory
from bayesnestor.utils.ParameterContainer import (
    ENestorVariant,
    ERequestType,
    ModelMetadata,
)

# Mocking necessary imports
MockPgmpyInference = Mock()
MockPyagrumInference = Mock()


@pytest.fixture
def mock_uuid():
    with patch(
        "uuid.uuid4", return_value=uuid.UUID("12345678-1234-5678-1234-567812345678")
    ):
        yield


@pytest.fixture
def backend_factory():
    return BackendFactory()


def test_create_with_str(mock_uuid, backend_factory):
    result = backend_factory.create(r"examples\data\example_xmlbif.xml")

    assert len(result) == 2

    for instance, metadata in result.items():
        assert isinstance(metadata, ModelMetadata)
        assert metadata.id == "12345678-1234-5678-1234-567812345678"
        assert metadata.created_via == ERequestType.EXCHANGE_FORMAT


def test_create_with_bayesian_network(
    fixture_bn_confounder_param, mock_uuid, backend_factory, mocker
):
    model, _ = fixture_bn_confounder_param("Test")
    result = backend_factory.create(model)

    assert len(result) == 2

    for instance, metadata in result.items():
        assert isinstance(metadata, ModelMetadata)
        assert metadata.name == "Test"
        assert metadata.id == "12345678-1234-5678-1234-567812345678"
        assert metadata.created_via == ERequestType.NETWORK
        assert metadata.network_defintion == model


def test_create_with_unsupported_type(backend_factory):
    with pytest.raises(TypeError):
        backend_factory.create(123)


def test_create_with_nestor_variant(backend_factory):
    mock_variant = Mock(spec=ENestorVariant)
    with pytest.raises(NotImplementedError):
        backend_factory.create(mock_variant)
