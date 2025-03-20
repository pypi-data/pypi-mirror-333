import abc
from enum import Enum
from typing import Any, List, Union

from bayesnestor.reporting.ReportingContainers import ReportEntry


class IReporting(metaclass=abc.ABCMeta):
    """Interface-like definition for Reporter classes."""

    @classmethod
    def __subclasshook__(cls, subclass: Any) -> bool:
        """Define the set of mandatory methods for this interface."""
        return (
            hasattr(subclass, "generate_report")
            and callable(subclass.generate_report)
            or NotImplemented
        )

    @abc.abstractmethod
    def generate_report(
        self,
        requested_metrics: Union[Enum, List[Enum]] = None,
    ):
        """Main method to calculate and output different metrics with regard to a Bayesian Network.

        Args:
            requested_metrics (Union[Enum, List[Enum]], optional): Metrics which should be calculated. If no metric(s) are provided, all implmented algorithms are executed. Defaults to None.

        Raises:
            NotImplementedError: Default error raised if this method is not implement outside the base class.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_report_entries(self) -> List[ReportEntry]:
        """Returns all results that have been generated in the last executions of metrics evaluations.

        Raises:
            NotImplementedError: Default error raised if this method is not implement outside the base class.

        Returns:
            List[ReportEntry]: A List with all the currently stored results.
        """
        raise NotImplementedError
