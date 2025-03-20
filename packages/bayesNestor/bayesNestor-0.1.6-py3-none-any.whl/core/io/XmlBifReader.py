from itertools import chain
from pathlib import Path
from typing import Dict, List, Tuple, Union

import numpy as np
from lxml import etree

from bayesnestor.core.BayesianNetwork import BayesianNetwork
from bayesnestor.core.ConditionalProbabilityTable import CPT
from bayesnestor.utils.Utils import check_file_type

base_path = Path(__file__).parent
XSD_FILE = str((base_path / "../io/validation_files/schema_xmlbif.xsd").resolve())


class XMLBIFReader:
    """
    Initialisation of XMLBIFReader object.

    Parameters
    ----------
    path : str
        Path to the file containing XMLBIF data

    Reference
    ---------
    [1] https://www.cs.cmu.edu/afs/cs/user/fgcozman/www/Research/InterchangeFormat/
    """

    def __init__(self, path):
        self.network = self._load_xml(path)
        self.network_name = self.network.find("NAME").text
        self.variables = self._get_variables()
        self.variable_parents = self._get_parents()
        self.edge_list = self._get_edges()
        self.variable_states = self._get_states()
        self.variable_CPD = self._get_values()
        self.variable_property = self._get_property()

    def _load_xml(self, path: Union[Path, str]) -> None:
        """Helper function to parse and validate a specified BIFXML-file.

        Args:
            path (Union[Path, str]): Path to the XML-file

        Raises:
            ValueError: Raised if the provided path is invalid OR if the BIFXML-file cannot be validated against its schema.
        """
        if check_file_type(path, valid_extensions=[".xml"]) is False:
            raise ValueError(
                f"The provided file path ({path}) is invalid. Please check the file extension and/or the path itself."
            )

        with open(XSD_FILE, "r") as xsd_file:
            xsd_content = xsd_file.read()
            xmlschema_doc = etree.XML(xsd_content)
            xmlschema = etree.XMLSchema(xmlschema_doc)

        try:
            tree = etree.parse(path)

            # Validate the XML file against the XSD
            if xmlschema.validate(tree):
                return tree.find("NETWORK")
            else:
                raise ValueError(
                    f"XML file is invalid against the XSD. \n {xmlschema.error_log}"
                )

        except (etree.XMLSyntaxError, etree.XMLSchemaParseError) as e:
            print(f"Error parsing XML or XSD: {e}")

    def _get_variables(self) -> List[str]:
        """
        Returns list of variables of the network
        """
        return [
            variable.find("NAME").text for variable in self.network.findall("VARIABLE")
        ]

    def _get_edges(self) -> List[Tuple[str, str]]:
        """
        Returns the edges of the network
        """
        return [
            (value, key)
            for key, values in self.variable_parents.items()
            for value in values
        ]

    def _get_states(self) -> Dict[str, List[str]]:
        """
        Returns the states of variables present in the network
        """
        return {
            variable.find("NAME").text: [
                outcome.text for outcome in variable.findall("OUTCOME")
            ]
            for variable in self.network.findall("VARIABLE")
        }

    def _get_parents(self) -> Dict[str, List[str]]:
        """
        Returns the parents of the variables present in the network
        """
        return {
            definition.find("FOR").text: [
                given.text for given in definition.findall("GIVEN")
            ]
            for definition in self.network.findall("DEFINITION")
        }

    def _get_values(self) -> Dict[str, List[float]]:
        """
        Returns the CPD of the variables present in the network
        """
        variable_CPD = {
            definition.find("FOR").text: list(
                map(float, definition.find("TABLE").text.split())
            )
            for definition in self.network.findall("DEFINITION")
        }
        for variable, values in variable_CPD.items():
            arr = np.array(values).reshape(
                (len(self.variable_states[variable]), -1), order="F"
            )
            variable_CPD[variable] = list(arr)
        return variable_CPD

    def _get_property(self) -> Dict[str, List[str]]:
        """
        Returns the property of the variable
        """
        return {
            variable.find("NAME").text: [
                prop.text for prop in variable.findall("PROPERTY")
            ]
            for variable in self.network.findall("VARIABLE")
        }

    def get_model(self, state_name_type=str) -> BayesianNetwork:
        """
        Returns a Bayesian Network instance from the file.

        Parameters
        ----------
        state_name_type: int, str, or bool (default: str)
            The data type to which to convert the state names of the variables.

        Returns
        -------
        BayesianNetwork instance: The read model.

        """
        model = BayesianNetwork(name=self.network_name, node_connections=self.edge_list)

        defined_cpts = []
        for var, values in self.variable_CPD.items():
            evidence_card = [
                len(self.variable_states[evidence_var])
                for evidence_var in self.variable_parents[var]
            ]
            state_names = {
                v: list(map(state_name_type, self.variable_states[v]))
                for v in chain([var], self.variable_parents[var])
            }
            cur_cpt = CPT(
                var,
                len(self.variable_states[var]),
                values,
                evidence=[str(elem) for elem in self.variable_parents[var]],
                evidence_card=[int(elem) for elem in evidence_card],
                state_names=state_names,
            )
            defined_cpts.append(cur_cpt)

        connected_vars = set([item for sublist in self.edge_list for item in sublist])
        for cpt in (cpt for cpt in defined_cpts if cpt.name in connected_vars):
            model.add_cpts(cpt)

        return model
