import numpy as np
import pytest

from bayesnestor.core.backends.BackendPgmpy import PgmpyInference
from bayesnestor.core.backends.BackendPyAgrum import PyagrumInference


@pytest.mark.parametrize(
    "variables, evidence, fixture",
    [
        (["A"], {"C": "st_C_0"}, "fixture_bn_random_small"),
        (["B"], {"C": "st_C_1"}, "fixture_bn_random_small"),
        (["C"], {"A": "st_A_0"}, "fixture_bn_random_small"),
        (["C"], {"A": "st_A_1", "B": "st_B_0"}, "fixture_bn_random_small"),
        (["D"], {}, "fixture_bn_random_small"),
        (
            ["D"],
            {"A": "st_A_1", "B": "st_B_0", "C": "st_C_1"},
            "fixture_bn_random_small",
        ),
        (
            ["E"],
            {"A": "st_A_1", "B": "st_B_0", "C": "st_C_1", "D": "st_D_0"},
            "fixture_bn_random_small",
        ),
    ],
)
def test_query_simple_marginal_success(variables, evidence, fixture, request):
    model_name = "test"
    model = request.getfixturevalue(fixture)(model_name)

    pgmpy_instance = PgmpyInference(model)
    pyagrum_instance = PyagrumInference(model)

    pgmpy_query_result = pgmpy_instance.query(
        variables=variables, evidence=evidence
    ).values
    pyagrum_query_result = pyagrum_instance.query(
        variables=variables, evidence=evidence
    ).values

    assert np.allclose(pgmpy_query_result[0], pyagrum_query_result[0], atol=1e-15)


@pytest.mark.parametrize(
    "variables, do, evidence, atol, fixture",
    [
        (["A"], {"B": "st_B_0"}, {"E": "st_E_0"}, 1e-15, "fixture_bn_random_small"),
        (["B"], {"A": "st_A_1"}, {"E": "st_E_0"}, 1e-15, "fixture_bn_random_small"),
        (["D"], {"C": "st_C_0"}, None, 1e-15, "fixture_bn_random_small"),
        (
            ["E"],
            {
                "C": "st_C_0",
                "D": "st_D_1",
            },
            {},
            2e-1,
            "fixture_bn_random_small",
        ),
        (
            ["E"],
            {
                "C": "st_C_0",
                "D": "st_D_1",
            },
            {"A": "st_A_1"},
            2e-1,
            "fixture_bn_random_small",
        ),
    ],
)
def test_intervention_simple_marginal_success(
    variables, do, evidence, atol, fixture, request
):
    model_name = "test"
    model = request.getfixturevalue(fixture)(model_name)

    pgmpy_instance = PgmpyInference(model)
    pyagrum_instance = PyagrumInference(model)

    pgmpy_query_result = pgmpy_instance.interventional_query(
        variables=variables, do=do, evidence=evidence
    ).values
    pyagrum_query_result = pyagrum_instance.interventional_query(
        variables=variables, do=do, evidence=evidence
    ).values

    assert np.allclose(pgmpy_query_result[0], pyagrum_query_result[0], atol=atol)
