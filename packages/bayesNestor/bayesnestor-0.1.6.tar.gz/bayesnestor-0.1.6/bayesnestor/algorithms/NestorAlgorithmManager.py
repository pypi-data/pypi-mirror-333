from typing import Any, Dict, List, Tuple

from bayesnestor.utils.ParameterContainer import EBackend, ModelMetadata


# Singleton
class NestorAlgorithmManager:
    __all_le_target_states = {
        "CT": "Yes",
        "BO": "Yes",
        "LG": "Yes",
        "MS": "Yes",
        "QU": "Yes",
        "EX": "Yes",
        "SU": "Yes",
        "AAM": "Yes",
        "VAM": "Yes",
        "TAM": "Yes",
    }

    __prioritized_backend = EBackend.PGMPY
    _instance = None

    def __new__(cls, *args, **kwargs):

        if cls._instance is None:

            cls._instance = super(NestorAlgorithmManager, cls).__new__(
                cls, *args, **kwargs
            )

        return cls._instance

    @classmethod
    def change_prioritized_backend(cls, new_prio: EBackend):
        """Changes the prioritzied backend for running infernces in the background, i.e., it allows to set the primarily used third-party library.

        Args:
            new_prio (EBackend): New prioritized Backend for running internal inferences and queries.

        Raises:
            TypeError: Raised if configured prioritized Backend is not an EBackend instance.
        """
        if isinstance(new_prio, EBackend):
            cls.__prioritized_backend = new_prio
        else:
            raise TypeError(f"Provided priority is unknown (type: {type(new_prio)})")

    def generate_learning_path(
        self,
        model_handles: Dict[str, Tuple[Any, ModelMetadata]],
        evidence: Dict[str, str],
    ) -> List[Tuple[str, float]]:
        """Predict a learning path using the currently selected Nestor-Model.

        Args:
            model_handles (Dict[str, Tuple[Any, ModelMetadata]]): Dictionary containing the handles to the instantiated models (including their metadata; keyed by their id).
            evidence (Dict[str, str]): Observation of the students pyschological properties that influence the predicted learning path.

        Returns:
            List[Tuple[str, float]]: Predicted learning path as a sequence of learning elements.
        """

        for id, (inst, meta) in model_handles.items():
            if meta.backend_used is self.__prioritized_backend:
                learn_path = []

                for learn_elem, target_state in self.__all_le_target_states.items():
                    query_res = inst.query(variables=[learn_elem], evidence=evidence)

                    learn_path.append(
                        (learn_elem, query_res.get_value({learn_elem: target_state}))
                    )

                return self.__sort_learn_path(learn_path)

    def gen_learningpath_single_node(
            self,
            model_handles: Dict[str, Tuple[Any, ModelMetadata]],
            evidence: Dict[str, str],
        ) -> List[Tuple[str, float]]:
            """Predict a learning path using the currently selected Nestor-Model.

            Args:
                model_handles (Dict[str, Tuple[Any, ModelMetadata]]): Dictionary containing the handles to the instantiated models (including their metadata; keyed by their id).
                evidence (Dict[str, str]): Observation of the students pyschological properties that influence the predicted learning path.

            Returns:
                List[Tuple[str, float]]: Predicted learning path as a sequence of learning elements.
            """

            for id, (inst, meta) in model_handles.items():
                if meta.backend_used is self.__prioritized_backend:
                    learn_path = []
                    target_candidates = meta.network_defintion.get_leaf_node_names()
                    if len(target_candidates) > 1:
                        raise ValueError(f"Please check your model - only one ultimate sink node (childless node) allowed.")
                    
                    query_res = inst.query(variables=[target_candidates[0]], evidence=evidence)

                    learn_path = list(zip(query_res.state_names[query_res.name], [round(float(x), 3) for x in query_res.values]))

                    return self.__sort_learn_path(learn_path)
    
    def explain(
        self,
        model_handles: Dict[str, Tuple[Any, ModelMetadata]],
        target_node: str = None,
        data: "Pandas-Dataframe" = None,
    ) -> None:
        """Experimental function that provides explanations of the current Nestor-Model used. Insights are calculated on the fly. This might take a considerable amount of time.


        Args:
            model_handles (Dict[str, Tuple[Any, ModelMetadata]]): Dictionary containing the handles to the instantiated models (including their metadata; keyed by their id).
            target_node (str, optional): Node for which additional explanation should be provided. Defaults to None.
            data (Pandas, optional): Data that is consistent with the current Nestor-Model. Defaults to None.

        Returns:
            None: Results are currently output on the terminal.
        """

        if not data:
            for id, (inst, meta) in model_handles.items():
                if meta.backend_used is EBackend.PGMPY:
                    data = inst.reconstruct_dataset()

        for id, (inst, meta) in model_handles.items():
            if meta.backend_used is EBackend.PYAGRUM:
                return inst.causal_shap(target_node, data)

    def __sort_learn_path(
        self, learn_path: List[Tuple[str, float]]
    ) -> List[Tuple[str, float]]:
        """Helper function to sort a generated learning path. Currently it sorts all elements based on their predicted probability.

        Args:
            learn_path (List[Tuple[str, float]]): Predicted and unsorted learning path as a sequence of learning elements.

        Returns:
            List[Tuple[str, float]]: Predicted and sorted learning path as a sequence of learning elements.
        """
        learn_path.sort(key=lambda x: x[1], reverse=True)
        return learn_path
