from unittest.mock import patch

import pytest

from bayesnestor.algorithms.NestorAlgorithmManager import NestorAlgorithmManager
from bayesnestor.core.ModelManager import ModelManager
from bayesnestor.utils.ParameterContainer import ENestorVariant


@pytest.mark.parametrize(
    "variant, expected_version",
    [
        (
            ENestorVariant.UN_WEIGHTED,
            ENestorVariant.UN_WEIGHTED,
        ),
        (
            ENestorVariant.WEIGHTED,
            ENestorVariant.WEIGHTED,
        ),
    ],
)
def test_configure_valid_success(
    fixture_patched_nestor_instance, variant, expected_version
):
    with patch.object(ModelManager, "create_model") as mock_create_model, patch.object(
        ModelManager, "get_handles"
    ) as mock_get_handles:

        mock_create_model.return_value = "mocked_id"
        mock_get_handles.return_value = {"mocked_handle": "mocked_meta"}

        fixture_patched_nestor_instance.configure(variant)

        assert fixture_patched_nestor_instance._configured_version == expected_version
        assert fixture_patched_nestor_instance._created_ids == "mocked_id"
        assert fixture_patched_nestor_instance._model_handles == {
            "mocked_handle": "mocked_meta"
        }
        mock_create_model.assert_called_once()
        mock_get_handles.assert_called_once()


def test_configure_invalid_raises_except(fixture_patched_nestor_instance):
    with pytest.raises(NotImplementedError):
        fixture_patched_nestor_instance.configure("invalid_variant")


def test_generate(fixture_patched_nestor_instance):
    fixture_patched_nestor_instance.configure(ENestorVariant.UN_WEIGHTED)
    evidence = {"key": "value"}
    expected_output = [("element1", 0.9), ("element2", 0.8)]

    with patch.object(
        NestorAlgorithmManager, "generate_learning_path"
    ) as mock_generate:
        mock_generate.return_value = expected_output

        result = fixture_patched_nestor_instance.generate(evidence)

        assert result == expected_output
        mock_generate.assert_called_once_with(
            fixture_patched_nestor_instance._model_handles, evidence
        )


def test_explain(fixture_patched_nestor_instance):
    target_node = "some_node"
    expected_output = "explanation"

    with patch.object(NestorAlgorithmManager, "explain") as mock_explain:
        mock_explain.return_value = expected_output

        result = fixture_patched_nestor_instance.explain(target_node)

        assert result == expected_output
        mock_explain.assert_called_once_with(
            fixture_patched_nestor_instance._model_handles, target_node
        )


def test_update(fixture_patched_nestor_instance):
    with pytest.raises(NotImplementedError):
        fixture_patched_nestor_instance.update()
