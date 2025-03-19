from unittest.mock import Mock

import pytest

from bayesnestor.core.BayesianNetwork import BayesianNetwork
from bayesnestor.core.ModelManager import ModelManager
from bayesnestor.utils.ParameterContainer import ModelMetadata


@pytest.fixture
def model_manager():
    """Fixture to get the singleton instance of ModelManager."""
    return ModelManager.get_instance()


@pytest.fixture
def mock_backend_factory(mocker):
    """Fixture to mock BackendFactory.create method."""
    return mocker.patch("pynestor.core.backends.BackendFactory.BackendFactory.create")


@pytest.fixture
def mock_bn():
    """Fixture to create a mock BayesianNetwork."""
    mock_bn = Mock(spec=BayesianNetwork)
    mock_bn.name = "mock_bn"
    return mock_bn


@pytest.fixture
def mock_metadata():
    """Fixture to create a mock ModelMetadata."""
    return ModelMetadata(
        name="mock_bn",
        id="12345678-1234-5678-1234-567812345678",
        created_via="EXCHANGE_FORMAT",
        network_defintion=Mock(spec=BayesianNetwork),
        backend_used="PGMPY",
        misc={},
    )


def test_singleton_instance(model_manager):
    """Test that ModelManager is a Singleton."""
    instance1 = ModelManager.get_instance()
    instance2 = ModelManager.get_instance()
    assert instance1 is instance2

def test_get_handles(model_manager, mock_bn, mock_metadata):
    """Test retrieving handles using a request."""
    model_manager._objects[mock_metadata.id] = "mock_obj"
    model_manager._metadata[mock_metadata.id] = mock_metadata
    model_manager._variant_records[mock_bn] = [mock_metadata.id]

    handles = model_manager.get_handles(mock_bn)

    assert len(handles) == 1
    assert handles[mock_metadata.id] == ("mock_obj", mock_metadata)


def test_get_handles_with_invalid_request(model_manager):
    """Test retrieving handles with an invalid request."""
    with pytest.raises(ValueError):
        model_manager.get_handles("invalid_request")


def test_get_object_metadata(model_manager, mock_metadata):
    """Test retrieving metadata for a specific object."""
    model_manager._metadata[mock_metadata.id] = mock_metadata

    metadata = model_manager.get_object_metadata(mock_metadata.id)

    assert metadata == mock_metadata


def test_get_object_metadata_with_invalid_id(model_manager):
    """Test retrieving metadata with an invalid object ID."""
    with pytest.raises(KeyError):
        model_manager.get_object_metadata("invalid_id")
