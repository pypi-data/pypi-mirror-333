from unittest.mock import Mock
import pytest

from bayesnestor.algorithms.NestorAlgorithmManager import NestorAlgorithmManager
from bayesnestor.utils.ParameterContainer import EBackend, ModelMetadata

# Fixture to reset the singleton before and after each test.
@pytest.fixture(autouse=True)
def reset_singleton():
    NestorAlgorithmManager._instance = None
    yield
    NestorAlgorithmManager._instance = None

@pytest.fixture
def singleton_instance():
    return NestorAlgorithmManager()

@pytest.mark.parametrize(
    "new_prio, expected_backend",
    [
        (EBackend.PGMPY, EBackend.PGMPY),
        (EBackend.PYAGRUM, EBackend.PYAGRUM),
    ],
)
def test_change_prioritized_backend(singleton_instance, new_prio, expected_backend):
    NestorAlgorithmManager.change_prioritized_backend(new_prio)
    assert (
        singleton_instance._NestorAlgorithmManager__prioritized_backend
        == expected_backend
    )

def test_change_prioritized_backend_invalid_type(singleton_instance):
    with pytest.raises(TypeError):
        singleton_instance.change_prioritized_backend("invalid_backend")

def test_explain(singleton_instance, mocker):
    # For the PGMPY branch: prepare a dummy instance that returns mock data.
    mock_model_instance_pgmpy = mocker.Mock()
    mock_model_instance_pgmpy.reconstruct_dataset.return_value = "mock_data"

    # For the PYAGRUM branch: prepare a dummy instance whose causal_shap returns an explanation.
    mock_model_instance_pyagrum = mocker.Mock()
    mock_model_instance_pyagrum.causal_shap.return_value = "explanation"

    mock_metadata_pgmpy = ModelMetadata(
        name="mock_model_pgmpy",
        id="mock_id_pgmpy",
        created_via=None,
        network_defintion=None,
        backend_used=EBackend.PGMPY,
        misc={},
    )
    mock_metadata_pyagrum = ModelMetadata(
        name="mock_model_pyagrum",
        id="mock_id_pyagrum",
        created_via=None,
        network_defintion=None,
        backend_used=EBackend.PYAGRUM,
        misc={},
    )

    model_handles_pgmpy = {"mock_id_pgmpy": (mock_model_instance_pgmpy, mock_metadata_pgmpy)}
    model_handles_pyagrum = {"mock_id_pyagrum": (mock_model_instance_pyagrum, mock_metadata_pyagrum)}

    # First call: no data provided, so explain() should call reconstruct_dataset.
    result_pgmpy = singleton_instance.explain(model_handles_pgmpy)
    # Since there is no PYAGRUM handle, the function returns None.
    assert result_pgmpy is None
    mock_model_instance_pgmpy.reconstruct_dataset.assert_called_once()

    # Second call: pass in data so that the PGMPY branch is skipped and PYAGRUM's causal_shap is used.
    result_pyagrum = singleton_instance.explain(model_handles_pyagrum, target_node="node", data="mock_data")
    assert result_pyagrum == "explanation"
    mock_model_instance_pyagrum.causal_shap.assert_called_once_with("node", "mock_data")

def test_generate_learning_path(singleton_instance, mocker):
    # Create a dummy query result that always returns 0.9.
    dummy_query_result = mocker.Mock()
    dummy_query_result.get_value.return_value = 0.9

    # Create a mock model instance that returns the dummy query result when query is called.
    mock_model_instance = mocker.Mock()
    mock_model_instance.query.return_value = dummy_query_result

    mock_metadata = ModelMetadata(
        name="mock_model",
        id="mock_id",
        created_via=None,
        network_defintion=None,
        backend_used=EBackend.PGMPY,
        misc={},
    )

    model_handles = {"mock_id": (mock_model_instance, mock_metadata)}
    evidence = {"evidence_key": "evidence_value"}

    # Patch the class attribute __all_le_target_states so that only one learning element is processed.
    mocker.patch.object(
        NestorAlgorithmManager,
        "_NestorAlgorithmManager__all_le_target_states",
        {"CT": "Yes"}
    )

    # Ensure the prioritized backend is PGMPY.
    singleton_instance.change_prioritized_backend(EBackend.PGMPY)

    # Patch the sort function so we control the final output.
    mocker.patch.object(
        singleton_instance,
        "_NestorAlgorithmManager__sort_learn_path",
        return_value=[("CT", 0.9)]
    )

    result = singleton_instance.generate_learning_path(model_handles, evidence)
    assert result == [("CT", 0.9)]

def test_sort_learn_path(singleton_instance):
    learn_path = [("element1", 0.75), ("element2", 0.95), ("element3", 0.65)]
    sorted_learn_path = singleton_instance._NestorAlgorithmManager__sort_learn_path(
        learn_path
    )
    assert sorted_learn_path == [
        ("element2", 0.95),
        ("element1", 0.75),
        ("element3", 0.65),
    ]
