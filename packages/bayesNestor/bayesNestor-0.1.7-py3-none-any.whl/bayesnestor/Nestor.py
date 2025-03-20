from pathlib import Path
from typing import Dict, List, Tuple

from bayesnestor.algorithms.NestorAlgorithmManager import NestorAlgorithmManager
from bayesnestor.core.ModelManager import ModelManager
from bayesnestor.utils.ParameterContainer import ENestorVariant

base_path = Path(__file__).parent


class Nestor:

    _configured_version = None  # ENetorVariant
    _model_handles = None  # dict(str/id, (instance, meta))
    _created_ids = None

    def __init__(self, variant: ENestorVariant = ENestorVariant.FULL_COGNITIVE):
        """Ctor of the 'main class' of the Nestor-package.

        Args:
            variant (ENestorVariant, optional): Requested model variant of Nestor (i.e., BayesianNetwork to be used). Defaults to ENestorVariant.UN_WEIGHTED.
        """
        self._algo_manager = NestorAlgorithmManager()
        self._model_manager = ModelManager()
        self.configure(variant)

    def configure(self, variant: ENestorVariant = ENestorVariant.FULL_COGNITIVE) -> None:
        """Define the Nestor-Variant (i.e., the BayesianNetwork) to be used for all calculations (e.g., learning path, explanation...)

        Args:
            variant (ENestorVariant, optional): Nestor-Variant to be used. Defaults to ENestorVariant.UN_WEIGHTED.

        Raises:
            NotImplementedError: Raised if the requested Nestor-Variant is not supported.
        """
        ## due to how configure works, only the 'current' configuration is accessible
        model_file = None
        match variant:
            case ENestorVariant.UN_WEIGHTED:
                self._configured_version = ENestorVariant.UN_WEIGHTED
                model_file = str((base_path / "data/cn_not_weighted.xml").resolve())
            case ENestorVariant.WEIGHTED:
                self._configured_version = ENestorVariant.WEIGHTED
                model_file = str((base_path / "data/cn_weighted.xml").resolve())

            case ENestorVariant.FULL_COGNITIVE:
                self._configured_version = ENestorVariant.FULL_COGNITIVE
                model_file = str((base_path / "data/cn_LearnerCognitiveModel.xml").resolve())
            case _:
                raise NotImplementedError(
                    f"Requested variant ({type(variant)}) is currently not supported."
                )

        self._created_ids = self._model_manager.create_model(model_file)
        self._model_handles = self._model_manager.get_handles(model_file)

    def generate(self, evidence: Dict[str, str]) -> List[Tuple[str, float]]:
        """Generate a learning path form the currently configured Nestor-Variant.

        Args:
            evidence (Dict[str, str]): Observation of the students pyschological properties that influence the predicted learning path.

        Returns:
            List[Tuple[str, float]]: Predicted learning path as a sequence of learning elements.
        """
        match self._configured_version:
            case ENestorVariant.WEIGHTED | ENestorVariant.UN_WEIGHTED:
                return self._algo_manager.generate_learning_path(self._model_handles, evidence)
            case ENestorVariant.FULL_COGNITIVE:
                return self._algo_manager.gen_learningpath_single_node(self._model_handles, evidence)
            case _:
                raise ValueError(f"Unsupported Nestor version was provided {self._configured_version}")

    def explain(self, target_node):
        """Experimental function that provides explanations of the current Nestor-Model used. Insights are calculated on the fly. This might take a considerable amount of time.

        Args:
            target_node (_type_): Experimental function that provides explanations of the current Nestor-Model used. Insights are calculated on the fly. This might take a considerable amount of time.

        Returns:
            None: Results are currently output on the terminal.
        """
        return self._algo_manager.explain(self._model_handles, target_node)

    def update(self):
        raise NotImplementedError(
            f"The update feature using learning analytics is currently not implemented."
        )
