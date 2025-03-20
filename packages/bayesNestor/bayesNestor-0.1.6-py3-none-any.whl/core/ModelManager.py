from collections import defaultdict
from typing import Any, Dict, List, Tuple, Union

from bayesnestor.core.backends.BackendFactory import BackendFactory
from bayesnestor.core.BayesianNetwork import BayesianNetwork
from bayesnestor.utils.ParameterContainer import ENestorVariant, ModelMetadata


# Singleton
class ModelManager:

    _instance = None

    def __new__(cls, *args, **kwargs):

        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()

        return cls._instance

    def _initialize(self):
        """Helper function to set up the Singletons infrastructure."""
        self._objects = {}
        self._metadata = {}
        self._variant_records = defaultdict(list)
        self._initialized_variants = set()

    def create_model(
        self, request: Union[ENestorVariant, BayesianNetwork, str]
    ) -> List[str]:
        """Instantiate the referenced model.

        Args:
            request (Union[ENestorVariant, BayesianNetwork, str]): Source of the model to create.

        Returns:
            List[str]: List of created id's for the internally instantiated third-party backends representing the requested models.
        """

        objs_metadata = {}

        if request not in self._initialized_variants:
            objs_metadata = BackendFactory.create(request)

        created_ids = []

        for obj, metadata in objs_metadata.items():

            obj_id = metadata.id
            self._objects[obj_id] = obj
            self._metadata[obj_id] = metadata
            self._variant_records[request].append(obj_id)
            created_ids.append(obj_id)
            self._initialized_variants.add(request)

        return created_ids

    def get_handles(
        self, request: Union[ENestorVariant, BayesianNetwork, str]
    ) -> Dict[str, Tuple[Any, ModelMetadata]]:
        """Get access to the internally instantiated third-party backends for the requested model.

        Args:
            request (Union[ENestorVariant, BayesianNetwork, str]):  Source of the requested model.

        Raises:
            ValueError: Raised if an invalid request (i.e., source to create a model from) is provided.

        Returns:
            Dict[str, Tuple[Any, ModelMetadata]]: Dictionary containing the handles to the instantiated models (including their metadata; keyed by their id).
        """
        if request in self._variant_records:

            return {
                obj_id: (self._objects[obj_id], self._metadata[obj_id])
                for obj_id in self._variant_records[request]
            }

        else:

            raise ValueError(f"No objects found for variant: {request}")

    def get_object_metadata(self, obj_id: str) -> ModelMetadata:
        """Get the metadata for a specific instance of a model (i.e., the object governing an inferable third-party backend).

        Args:
            obj_id (str): ID of the third-party backend instance.

        Raises:
            KeyError: Raised if an invalid id is requested.

        Returns:
            ModelMetadata: Metadata for the instantiated model.
        """
        if obj_id in self._metadata:
            return self._metadata[obj_id]

        else:

            raise KeyError(f"No metadata for object ID: {obj_id}")

    @classmethod
    def get_instance(cls) -> "ModelManager":
        """Get the Singleton instance.

        Returns:
            ModelManager: Singleton instance.
        """
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance
