import uuid
from pathlib import Path
from typing import Any, Dict, List, Union

from bayesnestor.core.backends.BackendPgmpy import PgmpyInference
from bayesnestor.core.backends.BackendPyAgrum import PyagrumInference
from bayesnestor.core.BayesianNetwork import BayesianNetwork
from bayesnestor.core.io.XmlBifReader import XMLBIFReader
from bayesnestor.utils.ParameterContainer import (
    EBackend,
    ENestorVariant,
    ERequestType,
    ModelMetadata,
)


class BackendFactory:

    @classmethod
    def __get_registered_backends(cls) -> List[EBackend]:
        """Helper function to manage an overview of currently selectable (useably implemented) backend-libraries.

        Returns:
            List[EBackend]: List of currently selectable backend-libraries.
        """
        return [(PgmpyInference, EBackend.PGMPY), (PyagrumInference, EBackend.PYAGRUM)]

    @staticmethod
    def create(
        request: Union[ENestorVariant, BayesianNetwork, str, Path]
    ) -> Dict[Any, ModelMetadata]:
        """Instantiate a given model in all available backends.

        Args:
            request (Union[ENestorVariant, BayesianNetwork, str]): Definition origin of the model.

        Raises:
            TypeError: Raised if provided definition of a models origin is not supported.
            NotImplementedError: Raised if an invalid Nestor-Version is requested OR if an invalid model format is provided as request.

        Returns:
            Dict[Any, ModelMetadata]: Dictionary containing the handles to the instantiated models (including their metadata; keyed by their id).
        """

        if not isinstance(request, (ENestorVariant, BayesianNetwork, str, Path)):

            raise TypeError(
                f"Provided information to request a model {type(request)} is not supported."
            )

        instances = dict()
        match request:

            case ENestorVariant():

                raise NotImplementedError(
                    "Requested category is a NestorVariant which is currently not implemented"
                )

            case str() | Path():

                bn = XMLBIFReader(request).get_model()

                for handle, backend_info in BackendFactory.__get_registered_backends():

                    inst = handle(bn)

                    meta = ModelMetadata(
                        name=bn.name,
                        id=str(uuid.uuid4()),
                        created_via=ERequestType.EXCHANGE_FORMAT,
                        network_defintion=bn,
                        backend_used=backend_info,
                        misc=dict(),
                    )

                    instances[inst] = meta
                return instances

            case BayesianNetwork():

                for handle, backend_info in BackendFactory.__get_registered_backends():

                    inst = handle(request)

                    meta = ModelMetadata(
                        name=request.name,
                        id=str(uuid.uuid4()),
                        created_via=ERequestType.NETWORK,
                        network_defintion=request,
                        backend_used=backend_info,
                        misc=dict(),
                    )

                    instances[inst] = meta
                return instances

            case _:

                raise NotImplementedError(
                    f"Requested category {type(request)} is currently not supported."
                )
