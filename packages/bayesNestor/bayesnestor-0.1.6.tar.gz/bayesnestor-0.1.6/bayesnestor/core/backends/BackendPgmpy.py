"""
This implementation wraps the library "pgmpy".
See https://github.com/pgmpy/pgmpy
"""

from typing import Any, List, Optional, Tuple, Union

import numpy as np
from pgmpy.inference import CausalInference as pgmpyCausalInference
from pgmpy.inference import VariableElimination as pgmpyVariableElimination
from pgmpy.models import BayesianNetwork as pgmpyBayesianModel
from pgmpy.sampling import BayesianModelSampling

from bayesnestor.core.backends.IBackend import IBackend
from bayesnestor.core.BayesianNetwork import BayesianNetwork
from bayesnestor.core.ConditionalProbabilityTable import CPT
from bayesnestor.core.CPTFactory import CPTFactory
from bayesnestor.core.DiscreteFactor import DiscreteFactor


class PgmpyInference(IBackend):
    """This implementation wraps the library "pgmpy".
        See https://github.com/pgmpy/pgmpy

    Attributes:
        model (BayesianNetwork): Instance of a core.BayesianNetwork-instance on which queries should be run.
    """

    model = None
    __inference_engine_inst = None  # pgmpy VariableElemination
    __causal_engine_inst = None  # pgmpy CausalInference
    __internal_model = None  # pgmpy BayesianModel

    def __init__(self, model: BayesianNetwork) -> None:
        """Ctor of the Inference class for backend pgmpy.

        Args:
            model (BayesianNetwork): Instance of a core.BayesianNetwork-instance on which queries should be run.
        """
        self.model = model
        self.__build_internal_model()
        self.__inference_engine_inst = pgmpyVariableElimination(self.__internal_model)
        self.__causal_engine_inst = pgmpyCausalInference(self.__internal_model)

    def __build_internal_model(self) -> None:
        """Setup method to instantiate a model that is compatible with the internally used, encapsulated inference algorithm."""
        self.__internal_model = pgmpyBayesianModel(self.model.node_connections)
        for node in self.model.get_independent_nodes():
            self.__internal_model.add_node(node)

        for cpt in self.model.model_elements.values():
            self.__internal_model.add_cpds(CPTFactory.to_pgmpy_cpt(cpt))

        print()

    def query(
        self,
        variables: Union[str, List[str]],
        evidence: Optional[List[Tuple[str, str]]] = None,
    ) -> Union[CPT, DiscreteFactor]:
        """This method can be used to run associational inference on the current BN instance.
            Depending on the queried variables either a CPT (only one var.) or a DiscreteFactor (multiple vars.) instance is returned.

        Args:
            variables (list<str>): Queried variables
            evidence (list<tuple<str, str>>, optional): Observations in the form of a list of tuples with node name and observed node state.

        Returns:
             CPT or DiscreteFactor: Return type is depending on number of queried variables.
        Raises:
             TypeError: Raised if queried variables are not a string or list of strings.
             ValueError: Raised if evidence variables and query variables intersect.
        """
        if not isinstance(variables, (list, str)):
            raise TypeError(
                f"Queried variable(s) need to be a string or list of strings but are {type(variables)}."
            )

        variables = variables if isinstance(variables, list) else [variables]

        evidence = dict(evidence) if isinstance(evidence, list) else evidence
        common_vars = set(evidence if evidence is not None else []).intersection(
            set(variables)
        )

        if common_vars:
            raise ValueError(
                f"Query contains evidence: {common_vars} that is part of the scoped variables:{variables}."
            )

        query_result = self.__inference_engine_inst.query(
            variables=variables,
            evidence=evidence,
            joint=True,
            show_progress=False,
            elimination_order="MinFill",
        )

        return self.__build_internal_repr(query_result)

    def interventional_query(
        self,
        variables: Union[str, List[str]],
        do: Optional[List[Tuple[str, str]]] = None,
        evidence: Optional[List[Tuple[str, str]]] = None,
    ) -> Union[CPT, DiscreteFactor]:
        """This method can be used to run interventional inference on the current BN instance.
            Depending on the queried variables either a CPT (only one var.) or a DiscreteFactor (multiple vars.) instance is returned.

        Args:
            variables (list<str>): Queried variables
            do (list<tuple<str, str>, optional): List of do-nodes and their active states.
            evidence (list<tuple<str, str>>, optional): Observations in the form of a list of tuples with node name and observed node state.

        Returns:
            CPT or DiscreteFactor: Return type is depending on number of queried variables.

        Raises:
            TypeError: Raised if queried variables are not a string or list of strings.
            ValueError: Raised if evidence variables and query variables intersect.
        """
        evidence = dict(evidence) if isinstance(evidence, list) else evidence
        do = dict(do) if isinstance(do, list) else do

        if not isinstance(variables, (list, str)):
            raise TypeError(
                f"Queried variable(s) need to be a string or list of strings but are {type(variables)}."
            )

        variables = variables if isinstance(variables, list) else [variables]
        common_vars = set(evidence if evidence is not None else []).intersection(
            set(variables)
        )

        if common_vars:
            raise ValueError(
                f"Query contains evidence: {common_vars} that is part of the scoped variables:{variables}."
            )

        common_vars = set(do if do is not None else []).intersection(set(variables))

        if common_vars:
            raise ValueError(
                f"Query contains do-variables: {common_vars} that are part of the scoped variables:{variables}."
            )

        query_result = self.__causal_engine_inst.query(
            variables=variables,
            do=do,
            evidence=evidence,
            adjustment_set=None,
            inference_algo="ve",
            show_progress=False,
        )

        return self.__build_internal_repr(query_result)

    def reconstruct_dataset(self, size: int = None) -> "Pandas-Dataframe":
        """Reconstructs a potential data-set based on the parameterization of the model.

        Args:
            size (int, optional): Number of records in the dataset.

        Returns:
            Pandas-Dataframe: Returns a Pandas-Dataframe representing the reconstructed dataset that is consistent with the model.
        """
        sample_size = (
            size
            if size
            else int(np.multiply(np.log(len(self.model.model_elements.keys())), 5000))
            + 1
        )
        sampler = BayesianModelSampling(self.__internal_model)
        return sampler.likelihood_weighted_sample(
            size=int(sample_size), show_progress=True
        )

    def __build_internal_repr(self, res_factor: Any) -> Union[CPT, DiscreteFactor]:
        """Method to convert the internal (pgmpy) representation of a factor/cpt
            into a CPT or DiscretFactor.
            This method is needed to encapsulate backend representation of results
            from the internal representations of Bayesian Networks.

        Args:
            res_factor (pgmpy.factor.DiscreteFactor or pgmpy.factor.TabularCPD): Result of a query.
            is_cpt (bool, optional): Flag indicating if the result should be interpreted as
                    a CPT or DiscreteFactor.

        Returns:
            core.CPT or core.DiscreteFactor: Internal representation
                    of query results.
        """

        if len(res_factor.cardinality) == 1:
            return CPTFactory.from_pgmpy_factor(res_factor)

        else:
            new_name = "_".join(res_factor.variables)
            int_obj = DiscreteFactor(
                name=new_name,
                scope=res_factor.variables,
                cardinalities=res_factor.cardinality,
                values=res_factor.values,
                state_names=res_factor.state_names,
            )
            int_obj._DiscreteFactor__str_repr = str(res_factor)
            return int_obj
