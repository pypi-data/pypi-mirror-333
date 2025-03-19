import itertools

import pytest
from pgmpy.factors.discrete import TabularCPD as pgmpyCPT
from pyAgrum import Potential as pyagrumCPT

from bayesnestor.core.ConditionalProbabilityTable import CPT
from bayesnestor.core.CPTFactory import CPTFactory


class TestCPTFactory:

    @pytest.mark.parametrize(
        "fix_create_valid_cpt",
        [
            {"var_card": 2, "ev_cards": []},  # marginal prob
            {"var_card": 3, "ev_cards": [2]},  # one parent
            {"var_card": 3, "ev_cards": [2, 4, 5, 7, 3]},  # mult. parents
        ],
        indirect=True,
    )
    def test_to_pgmpy_success(self, fix_create_valid_cpt):
        internal_cpt = fix_create_valid_cpt
        con_pgmpy_cpt = CPTFactory.to_pgmpy_cpt(internal_cpt)

        assert isinstance(con_pgmpy_cpt, pgmpyCPT)

    @pytest.mark.parametrize(
        "fix_create_valid_cpt",
        [
            {"var_card": 4, "ev_cards": []},  # marginal prob
            {"var_card": 2, "ev_cards": [3]},  # one parent
            {"var_card": 5, "ev_cards": [5, 4, 3, 2]},  # mult. parents
        ],
        indirect=True,
    )
    def test_to_pyagrum_success(self, fix_create_valid_cpt):
        internal_cpt = fix_create_valid_cpt
        con_pgmpy_cpt = CPTFactory.to_pyagrum_cpt(internal_cpt)

        assert isinstance(con_pgmpy_cpt, pyagrumCPT)

    @pytest.mark.parametrize(
        "fix_create_valid_pgmpy_cpt",
        [
            {"var_card": 3, "ev_cards": []},  # marginal prob
            {"var_card": 6, "ev_cards": [2]},  # one parent
            {"var_card": 4, "ev_cards": [2, 3, 4, 5, 6]},  # mult. parents
        ],
        indirect=True,
    )
    def test_from_pgmpy_success(self, fix_create_valid_pgmpy_cpt):
        pgmpy_cpt = fix_create_valid_pgmpy_cpt
        internal_cpt = CPTFactory.from_pgmpy_cpt(pgmpy_cpt)

        assert isinstance(internal_cpt, CPT)

    @pytest.mark.parametrize(
        "fix_create_valid_pyagrum_cpt",
        [
            {"var_card": 5, "ev_cards": []},  # marginal prob
            {"var_card": 2, "ev_cards": [7]},  # one parent
            {"var_card": 3, "ev_cards": [5, 11]},  # mult. parents
        ],
        indirect=True,
    )
    def test_from_pyagrum_success(self, fix_create_valid_pyagrum_cpt):
        pyagrum_cpt = fix_create_valid_pyagrum_cpt
        internal_cpt = CPTFactory.from_pyagrum_potential(pyagrum_cpt)

        assert isinstance(internal_cpt, CPT)

    @pytest.mark.parametrize(
        "fix_create_valid_pgmpy_cpt",
        [
            {"var_card": 2, "ev_cards": []},  # marginal prob
            {"var_card": 3, "ev_cards": [7]},  # one parent
            {"var_card": 2, "ev_cards": [3, 5, 7, 11]},  # mult. parents
        ],
        indirect=True,
    )
    def test_convert_pgmpy_to_pyagrum_success(self, fix_create_valid_pgmpy_cpt):
        pgmpy_cpt = fix_create_valid_pgmpy_cpt
        pyagrum_cpt = CPTFactory.convert_pgmpy_to_pyagrum(pgmpy_cpt)

        assert isinstance(pyagrum_cpt, pyagrumCPT)

    @pytest.mark.parametrize(
        "fix_create_valid_pyagrum_cpt",
        [
            {"var_card": 7, "ev_cards": []},  # marginal prob
            {"var_card": 5, "ev_cards": [3]},  # one parent
            {"var_card": 3, "ev_cards": [2, 2, 3, 7]},  # mult. parents
        ],
        indirect=True,
    )
    def test_convert_pyagrum_to_pgmpy_success(self, fix_create_valid_pyagrum_cpt):
        pyagrum_cpt = fix_create_valid_pyagrum_cpt
        pgmpy_cpt = CPTFactory.convert_pyagrum_to_pgmpy(pyagrum_cpt)

        assert isinstance(pgmpy_cpt, pgmpyCPT)

    @pytest.mark.parametrize(
        "fix_create_valid_cpt",
        [
            {"var_card": 7, "ev_cards": []},  # marginal prob
            {"var_card": 5, "ev_cards": [3]},  # one parent
            {"var_card": 3, "ev_cards": [3, 5, 3, 7, 5]},  # mult. parents
        ],
        indirect=True,
    )
    def test_are_equal_success(self, fix_create_valid_cpt):
        internal_cpt = fix_create_valid_cpt
        pgmpy_cpt = CPTFactory.to_pgmpy_cpt(internal_cpt)
        pyagrum_cpt = CPTFactory.to_pyagrum_cpt(internal_cpt)

        variants = [internal_cpt, pgmpy_cpt, pyagrum_cpt]
        for combination in itertools.product(variants, variants):
            assert CPTFactory.are_equal(combination[0], combination[1])
