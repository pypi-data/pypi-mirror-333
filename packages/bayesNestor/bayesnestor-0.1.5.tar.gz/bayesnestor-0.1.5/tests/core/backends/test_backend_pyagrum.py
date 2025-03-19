import numpy as np
import pytest

from bayesnestor.core.backends.BackendPyAgrum import PyagrumInference



@pytest.mark.parametrize(
    "fixture",
    ["fixture_bn_confounder_param", "fixture_bn_independent_nodes_only_param"],
)
def test_instantiate_success(fixture, request):
    model_name = "test"
    model, _ = request.getfixturevalue(fixture)(model_name)

    instance = PyagrumInference(model)

    assert instance.model == model
    assert instance._PyagrumInference__inference_engine_inst is not None
    assert instance._PyagrumInference__internal_model is not None


@pytest.mark.parametrize(
    "variables, evidence, fixture, expected",
    [
        (["NODE_A"], None, "fixture_bn_confounder_param", [[0.1], [0.9]]),
        (
            ["NODE_B"],
            None,
            "fixture_bn_independent_nodes_only_param",
            [[0.987], [0.013]],
        ),
        (["NODE_C"], None, "fixture_bn_collider_param", [[0.71], [0.29]]),
        (
            ["NODE_A"],
            {"NODE_B": "STATE_NODE_B_Yes"},
            "fixture_bn_independent_nodes_only_param",
            [[0.123], [0.877]],
        ),
        (
            ["NODE_A", "NODE_B"],
            {"NODE_C": "STATE_NODE_C_Yes"},
            "fixture_bn_independent_nodes_only_param",
            [
                ({"NODE_A": "STATE_NODE_A_Yes", "NODE_B": "STATE_NODE_B_Yes"}, 0.1214),
                ({"NODE_A": "STATE_NODE_A_Yes", "NODE_B": "STATE_NODE_B_No"}, 0.0016),
                ({"NODE_A": "STATE_NODE_A_No", "NODE_B": "STATE_NODE_B_Yes"}, 0.8656),
                ({"NODE_A": "STATE_NODE_A_No", "NODE_B": "STATE_NODE_B_No"}, 0.0114),
            ],
        ),
    ],
)
def test_query_success(variables, evidence, fixture, expected, request):
    model_name = "test"
    model, _ = request.getfixturevalue(fixture)(model_name)

    instance = PyagrumInference(model)
    query_result = instance.query(variables=variables, evidence=evidence)

    if len(variables) == 1:
        assert np.allclose(query_result.get_probabilities(), expected, atol=1e-3)

    else:
        for state_combo, expected_val in expected:
            assert np.isclose(
                query_result.get_value(state_combo), expected_val, atol=1e-4
            )


@pytest.mark.parametrize(
    "variables, do, evidence, fixture, expected",
    [
        (
            ["NODE_A"],
            {"NODE_C": "STATE_NODE_C_Yes"},
            None,
            "fixture_bn_collider_param",
            [[0.123], [0.877]],
        ),  # Do-Calc Rule 1 -> P(A)
        (
            ["NODE_B"],
            {"NODE_C": "STATE_NODE_C_No"},
            None,
            "fixture_bn_collider_param",
            [[0.987], [0.013]],
        ),  # Do-Calc Rule 1 -> P(B)
        (
            ["NODE_C"],
            {"NODE_A": "STATE_NODE_A_Yes"},
            None,
            "fixture_bn_collider_param",
            [[0.127329], [0.872671]],
        ),  # Rule 2 -> P(C|A=Yes)
        (
            ["NODE_B"],
            {"NODE_A": "STATE_NODE_A_No"},
            None,
            "fixture_bn_collider_param",
            [[0.987], [0.013]],
        ),  # Rule 2 -> P(B)
        (
            ["NODE_C"],
            {"NODE_B": "STATE_NODE_B_Yes"},
            {"NODE_A": "STATE_NODE_A_No"},
            "fixture_bn_collider_param",
            [[0.789], [0.211]],
        ),  # Rule 2 -> P(C|A=No, B=Yes)
        (
            ["NODE_B"],
            {"NODE_A": "STATE_NODE_A_No"},
            None,
            "fixture_bn_confounder_param",
            [[0.3354896], [0.6645104]],
        ),  # Rule 2 -> P(B|A=No)
        (
            ["NODE_C"],
            {"NODE_B": "STATE_NODE_B_Yes"},
            {"NODE_A": "STATE_NODE_A_No"},
            "fixture_bn_independent_nodes_only_param",
            [[0.456], [0.544]],
        ),
    ],
)  # Rule 1 -> P(C)
def test_interventional_query_simple_marginal_success(
    variables, do, evidence, fixture, expected, request
):
    model_name = "test"
    model, _ = request.getfixturevalue(fixture)(model_name)

    instance = PyagrumInference(model)
    query_result = instance.interventional_query(
        variables=variables, do=do, evidence=evidence
    )

    assert np.allclose(query_result.get_probabilities(), expected, atol=1e-1)


@pytest.mark.parametrize(
    "variables, do, evidence, fixture, expected",
    [
        (
            ["NODE_A"],
            {"NODE_D": "STATE_NODE_D_Yes"},
            {"NODE_B": "STATE_NODE_B_Yes"},
            "fixture_bn_causal_queries_param",
            [[0.123], [0.877]],
        ),  # Rule 1 -> P(A|B) - d.sep via D -> P(A)
        (
            ["NODE_B"],
            {"NODE_D": "STATE_NODE_D_No"},
            {"NODE_C": "STATE_NODE_C_No"},
            "fixture_bn_causal_queries_param",
            [[0.987], [0.013]],
        ),  # Rule 1 -> P(B|C) - d.sep via D -> P(B)
        (
            ["NODE_D"],
            {"NODE_C": "STATE_NODE_C_Yes"},
            None,
            "fixture_bn_causal_queries_param",
            [[0.131658], [0.868342]],
        ),  # Rule 2 -> P(D|C=Yes)
        (
            ["NODE_D"],
            {"NODE_C": "STATE_NODE_C_No"},
            None,
            "fixture_bn_causal_queries_param",
            [[0.462903], [0.537097]],
        ),  # Rule 2 -> P(D|C=No)
        (
            ["NODE_D"],
            {"NODE_C": "STATE_NODE_C_No"},
            {"NODE_B": "STATE_NODE_B_No"},
            "fixture_bn_causal_queries_param",
            [[0.987], [0.013]],
        ),  # Rule 2 -> P(D|B=No,C=No)
        (
            ["NODE_C"],
            {"NODE_B": "STATE_NODE_B_Yes"},
            {"NODE_A": "STATE_NODE_A_No"},
            "fixture_bn_causal_queries_param",
            [[0.654], [0.346]],
        ),
    ],
)  # Rule 2 -> P(C|B=Yes, A=No) ])
def test_interventional_query_complex_marginal_success(
    variables, do, evidence, fixture, expected, request
):
    model_name = "test"
    model = request.getfixturevalue(fixture)(model_name)

    instance = PyagrumInference(model)
    query_result = instance.interventional_query(
        variables=variables, do=do, evidence=evidence
    )

    assert np.allclose(query_result.get_probabilities(), expected, atol=1e-3)


@pytest.mark.parametrize(
    "variables, do, evidence, expected",
    [
        (
            ["NODE_B", "NODE_D"],
            {"NODE_C": "STATE_NODE_C_No"},
            None,
            {
                "B_Yes#D_Yes": 0.4500719887,
                "B_Yes#D_No": 0.5369279899,
                "B_No#D_Yes": 0.01283102136,
                "B_No#D_No": 1.689999968e-4,
            },
        ),  # Rule 2 -> P(B,D|C=No)
        (
            ["NODE_A", "NODE_B"],
            {"NODE_D": "STATE_NODE_D_No"},
            None,
            {
                "A_Yes#B_Yes": 0.1175625252,
                "A_Yes#B_No": 0.1305492425e-3,
                "A_No#B_Yes": 0.8693846908,
                "A_No#B_No": 0.01144729152,
            },
        ),
    ],
)  # Rule 3 -> P(A,B)
def test_interventional_query_complex_factor_success(
    variables, do, evidence, fixture_bn_causal_queries_param, expected
):
    model_name = "test"
    delimiter = "#"
    model = fixture_bn_causal_queries_param(model_name)

    instance = PyagrumInference(model)
    query_result = instance.interventional_query(
        variables=variables, do=do, evidence=evidence
    )

    for scope, expected_val in expected.items():
        parts = scope.split(delimiter)
        node_states = {
            "NODE_" + state_ending[0]: "STATE_NODE_" + state_ending
            for state_ending in parts
        }

        assert np.isclose(query_result.get_value(node_states), expected_val, atol=1e-2)


def test_interventinal_inference_overlapping_query_node_and_evidence_raises_exception(
    fixture_bn_confounder_param,
):
    expected_exc_substring = "Query contains evidence"
    model_name = "test"
    queried_node = "NODE_C"
    overlapping_evidence = {
        "NODE_B": "STATE_NODE_B_Yes",
        queried_node: f"STATE_{queried_node}_Yes",
    }

    model, _ = fixture_bn_confounder_param(model_name)
    instance = PyagrumInference(model)

    with pytest.raises(ValueError) as e:
        assert instance.interventional_query(
            variables=queried_node, evidence=overlapping_evidence
        )

    assert expected_exc_substring in str(e.value)


def test_interventinal_inference_overlapping_query_node_and_do_raises_exception(
    fixture_bn_confounder_param,
):
    expected_exc_substring = "Query contains do-variables"
    model_name = "test"
    queried_node = "NODE_C"
    overlapping_do = {
        "NODE_B": "STATE_NODE_B_Yes",
        queried_node: f"STATE_{queried_node}_Yes",
    }

    model, _ = fixture_bn_confounder_param(model_name)
    instance = PyagrumInference(model)

    with pytest.raises(ValueError) as e:
        assert instance.interventional_query(variables=queried_node, do=overlapping_do)

    assert expected_exc_substring in str(e.value)


@pytest.mark.parametrize("bad_query", [None, 5, {0: "NODE_A"}])
def test_interventional_inference_invalid_type_for_variables_raises_exception(
    bad_query, fixture_bn_confounder_param
):
    expected_exc_substring = (
        "Queried variable(s) need to be a string or list of strings but are"
    )
    model_name = "test"
    model, _ = fixture_bn_confounder_param(model_name)
    instance = PyagrumInference(model)

    with pytest.raises(TypeError) as e:
        assert instance.interventional_query(bad_query)

    assert expected_exc_substring in str(e.value)


@pytest.mark.parametrize("bad_query", [None, 5, {0: "NODE_A"}])
def test_inference_invalid_type_for_variables_raises_exception(
    bad_query, fixture_bn_confounder_param
):
    expected_exc_substring = (
        "Queried variable(s) need to be a string or list of strings but are"
    )
    model_name = "test"
    model, _ = fixture_bn_confounder_param(model_name)
    instance = PyagrumInference(model)

    with pytest.raises(TypeError) as e:
        assert instance.query(bad_query)

    assert expected_exc_substring in str(e.value)


def test_inference_overlapping_query_node_and_evidence_raises_exception(
    fixture_bn_confounder_param,
):
    expected_exc_substring = "Query contains evidence"
    model_name = "test"
    queried_node = "NODE_C"
    overlapping_evidence = {
        "NODE_B": "STATE_NODE_B_Yes",
        queried_node: f"STATE_{queried_node}_Yes",
    }

    model, _ = fixture_bn_confounder_param(model_name)
    instance = PyagrumInference(model)

    with pytest.raises(ValueError) as e:
        assert instance.query(variables=queried_node, evidence=overlapping_evidence)

    assert expected_exc_substring in str(e.value)
