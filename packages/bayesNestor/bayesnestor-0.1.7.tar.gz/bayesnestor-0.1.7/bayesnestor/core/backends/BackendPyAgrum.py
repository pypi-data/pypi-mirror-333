"""
This implementation wraps the library "PyAgrum".
See  https://agrum.gitlab.io/  and   https://gitlab.com/agrumery/aGrUM
"""

from typing import Any, List, Optional, Tuple, Union

import numpy as np
import pyAgrum.causal as pyagrumCausal
import pyAgrum.lib.explain as expl
from pyAgrum import BayesNet as pyagrumBayesNet
from pyAgrum import LabelizedVariable as pyagrumLabelizedVariable
from pyAgrum import LazyPropagation as pyagrumLazyPropagation

from bayesnestor.core.backends.IBackend import IBackend
from bayesnestor.core.BayesianNetwork import BayesianNetwork
from bayesnestor.core.ConditionalProbabilityTable import CPT
from bayesnestor.core.CPTFactory import CPTFactory
from bayesnestor.core.DiscreteFactor import DiscreteFactor


class PyagrumInference(IBackend):
    """This implementation wraps the library "PyAgrum".
        See  https://agrum.gitlab.io/  and   https://gitlab.com/agrumery/aGrUM

    Attributes:
        model (BayesianNetwork): Instance of a core.BayesianNetwork-instance on which queries should be run.
    """

    model = None
    __inference_engine_inst = None  # pyagrum LazyPropagation
    __internal_model = None  # pyagrum BayesModel

    def __init__(self, model: BayesianNetwork) -> None:
        """Ctor of the Inference class for backend pyagrum.

        Args:
            model (BayesianNetwork): Instance of a core.BayesianNetwork-instance on which queries should be run.
        """
        self.model = model
        self.__build_internal_model()
        self.__inference_engine_inst = pyagrumLazyPropagation(self.__internal_model)

    def __build_internal_model(self) -> None:
        """Setup method to instantiate a model that is compatible with the internally used, encapsulated inference algorithm."""
        self.__internal_model = pyagrumBayesNet(self.model.name)

        # add nodes
        for node_name, node in self.model.model_elements.items():
            states = (
                node.state_names[node_name]
                if node.state_names is not None and node_name in node.state_names.keys()
                else node.variable_card
            )
            self.__internal_model.add(
                pyagrumLabelizedVariable(node_name, node_name, states)
            )

        # add connections
        for link in list(set(self.model.node_connections)):
            self.__internal_model.addArc(*link)

        # populate the pyagrum nodes with values
        for node_name, node in self.model.model_elements.items():
            if node.evidence_card is not None and len(node.evidence_card) >= 1:
                # address a potential re-ordering of evidence nodes and their effect on the cpts value-mapping
                target_evidence_order = self.__internal_model.cpt(node.name).names
                expected_potential = CPTFactory.to_pyagrum_cpt(node)

                if target_evidence_order != expected_potential.names:
                    self.__internal_model.cpt(node_name)[:] = (
                        expected_potential.reorganize(target_evidence_order).toarray()
                    )
                else:
                    self.__internal_model.cpt(node_name)[
                        :
                    ] = expected_potential.toarray()
            else:
                self.__internal_model.cpt(node_name).fillWith(
                    np.ravel(node.values).tolist()
                )

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

        # query_result is a pyagrum.Potential
        evidence = dict(evidence) if evidence is not None else {}
        self.__inference_engine_inst.setEvidence(evidence)

        if len(variables) <= 1:
            self.__inference_engine_inst.makeInference()
            query_result = self.__inference_engine_inst.posterior(str(variables[0]))

            return self.__build_internal_repr(query_result, is_cpt=True)

        else:
            query_vars = frozenset(variables)
            self.__inference_engine_inst.addJointTarget(query_vars)
            self.__inference_engine_inst.makeInference()
            query_result = self.__inference_engine_inst.jointPosterior(query_vars)

            return self.__build_internal_repr(query_result, is_cpt=False)

    def interventional_query(
        self,
        variables: Union[str, List[str]],
        do: Optional[List[Tuple[str, str]]] = None,
        evidence: Optional[List[Tuple[str, str]]] = None,
    ) -> Union[CPT, DiscreteFactor]:
        """This method can be used to run interventional inference on the current BN instance.
            Depending on the queried variables either a CPT (only one var.) or a DiscreteFactor (multiple vars.) instance is returned.
            Internally pyAgrum uses do-calculus or *door-criterias to build the estimation formula.
            Due to this the estimand, estimate and logic used to create the estimand are available as return values.

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

        params_on = set(variables)
        params_do = dict(do) if do is not None else {}
        params_knowing = dict(evidence) if evidence is not None else {}
        params_values = {**params_do, **params_knowing}

        formula, query_result, explanation = pyagrumCausal.causalImpact(
            cm=pyagrumCausal.CausalModel(self.__internal_model),
            on=params_on,
            doing=params_do.keys(),
            knowing=params_knowing.keys(),
            values=params_values,
        )
        print(f"Formula: {formula}")
        print(f"Explanation: {explanation}")
        print(f"Query Result: {query_result}")
        # latex_forumula = formula.toLatex()

        if len(variables) <= 1:
            return self.__build_internal_repr(query_result, is_cpt=True)

        return self.__build_internal_repr(query_result, is_cpt=False)

    def causal_shap(self, target_node, data):
        shap_obj = expl.ShapValues(bn=self.__internal_model, target=target_node)
        return shap_obj.causal(train=data.sample(n=1000))

    def __build_internal_repr(
        self, res_potential: Any, is_cpt: Optional[bool] = True
    ) -> Union[CPT, DiscreteFactor]:
        """Method to convert the internal (pyagrum) representation of a factor/cpt
            into a CPT or DiscretFactor.
            This method is needed to encapsulate backend representation of results
            from the internal representations of Bayesian Networks.

        Args:
            res_potential (pyAgrum.Potential): Result of a query.
            is_cpt (bool, optional): Flag indicating if the result should be interpreted as
                    a CPT or DiscreteFactor.

        Returns:
            core.ConditionalProbabilityTable or core.DiscreteFactor: Internal representation
                    of query results.
        """
        if is_cpt:
            return CPTFactory.from_pyagrum_potential(res_potential)

        else:
            var_card = res_potential.shape[0]
            var_name = res_potential.names[0]
            values = res_potential.toarray()
            state_names = {}
            for var in res_potential.names:
                state_names[var] = list(
                    self.__internal_model.variable(str(var)).labels()
                )

            int_obj = DiscreteFactor(
                name=var_name,
                scope=res_potential.names[::-1],
                cardinalities=res_potential.shape[::-1],
                values=np.reshape(values, (var_card, -1)),
                state_names=state_names,
            )

            int_obj._DiscreteFactor__str_repr = str(res_potential)
            return int_obj
