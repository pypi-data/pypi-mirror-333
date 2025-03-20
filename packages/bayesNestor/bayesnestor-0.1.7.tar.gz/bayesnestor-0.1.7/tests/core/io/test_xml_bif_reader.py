from unittest.mock import Mock, patch

import numpy as np
import pytest
from lxml import etree

from bayesnestor.core.BayesianNetwork import BayesianNetwork
from bayesnestor.core.io.XmlBifReader import XMLBIFReader


@pytest.fixture
def xml_bif_reader():
    """Fixture to initialize XMLBIFReader with an actual file."""
    path = r"examples\data\example_xmlbif.xml"

    with patch("pynestor.utils.Utils.check_file_type", return_value=True):
        mock_schema = Mock()
        with patch("lxml.etree.XMLSchema", return_value=mock_schema):
            mock_tree = etree.parse(path)
            mock_network = mock_tree.find("NETWORK")
            mock_schema.validate = Mock(return_value=True)
            return XMLBIFReader(path)


def test_get_variables(xml_bif_reader):
    """Test extraction of variables."""
    variables = xml_bif_reader._get_variables()
    expected_variables = [
        "light_on",
        "bowel_problem",
        "dog_out",
        "hear_bark",
        "family_out",
    ]
    assert variables == expected_variables


def test_get_edges(xml_bif_reader):
    """Test extraction of edges."""
    xml_bif_reader.variable_parents = {
        "light_on": ["family_out"],
        "dog_out": ["bowel_problem", "family_out"],
        "hear_bark": ["dog_out"],
    }
    edges = xml_bif_reader._get_edges()
    expected_edges = [
        ("family_out", "light_on"),
        ("bowel_problem", "dog_out"),
        ("family_out", "dog_out"),
        ("dog_out", "hear_bark"),
    ]
    assert edges == expected_edges


def test_get_states(xml_bif_reader):
    """Test extraction of states."""
    states = xml_bif_reader._get_states()
    expected_states = {
        "light_on": ["true", "false"],
        "bowel_problem": ["true", "false"],
        "dog_out": ["true", "false"],
        "hear_bark": ["true", "false"],
        "family_out": ["true", "false"],
    }
    assert states == expected_states


def test_get_parents(xml_bif_reader):
    """Test extraction of parents."""
    parents = xml_bif_reader._get_parents()
    expected_parents = {
        "light_on": ["family_out"],
        "bowel_problem": [],
        "dog_out": ["bowel_problem", "family_out"],
        "hear_bark": ["dog_out"],
        "family_out": [],
    }
    assert parents == expected_parents


def test_get_values(xml_bif_reader):
    """Test extraction of CPD values."""
    xml_bif_reader.variable_states = {
        "light_on": ["true", "false"],
        "bowel_problem": ["true", "false"],
        "dog_out": ["true", "false"],
        "hear_bark": ["true", "false"],
        "family_out": ["true", "false"],
    }
    values = xml_bif_reader._get_values()
    expected_values = {
        "light_on": [[0.6, 0.05], [0.4, 0.95]],
        "bowel_problem": [[0.01], [0.99]],
        "dog_out": [[0.99, 0.97, 0.9, 0.3], [0.01, 0.03, 0.1, 0.7]],
        "hear_bark": [[0.7, 0.01], [0.3, 0.99]],
        "family_out": [[0.15], [0.85]],
    }

    for key, exp_vals in expected_values.items():
        assert np.array_equal(exp_vals, values[key])


# def test_get_property(xml_bif_reader):
#     """Test extraction of variable properties."""
#     properties = xml_bif_reader._get_property()
#     expected_properties = {
#         "kid": ["position = (100, 165)"],
#         "light_on": ["position = (73, 165)"],
#         "bowel_problem": ["position = (190, 69)"],
#         "dog_out": ["position = (155, 165)"],
#         "hear_bark": ["position = (154, 241)"],
#         "family_out": ["position = (112, 69)"],
#     }
#     assert properties == expected_properties


def test_get_model(xml_bif_reader):
    """Test construction of BayesianNetwork model."""
    model = xml_bif_reader.get_model()
    assert isinstance(model, BayesianNetwork)
    assert model.name == "Dog_Problem"
    assert model.node_connections == [
        ("family_out", "light_on"),
        ("bowel_problem", "dog_out"),
        ("family_out", "dog_out"),
        ("dog_out", "hear_bark"),
    ]


def test_invalid_file_extension():
    with pytest.raises(ValueError):
        XMLBIFReader("invalid_file.abc")
