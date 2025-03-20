import time
from typing import Any, Dict, List, Tuple, Union

import networkx as nx
import numpy as np

from bayesnestor.core.BayesianNetwork import BayesianNetwork
from bayesnestor.reporting.IReporting import IReporting
from bayesnestor.reporting.ReportingContainers import (
    EBasicReportMetric,
    EReportOrigin,
    EReportScope,
    ReportEntry,
)
from bayesnestor.reporting.ReportingUtils import print_2d_table, print_dict_with_meta


class BasicReporter(IReporting):
    investigated_bn = None

    def __init__(self, bn: BayesianNetwork):
        if isinstance(bn, BayesianNetwork):
            self.investigated_bn = bn
        else:
            raise ValueError(
                f"The model to be investigated needs to be a BayesianNetwork but a variable with type {type(model)} was passed."
            )
        self.collected_results = {e: {} for e in EBasicReportMetric}

    def generate_report(
        self,
        requested_metrics: Union[EBasicReportMetric, List[EBasicReportMetric]] = None,
    ) -> List[ReportEntry]:
        """Main method to calculate and output different basic metrics with regard to a Bayesian Network.
            If no requested_metrics are provided, all implemented metrics are calculated.

        Args:
            requested_metrics (Union[EBasicReportMetric, List[EBasicReportMetric]], optional): Metrics which should be calculated. If no metric(s) are provided, all implmented algorithms are executed. Defaults to None.

        Returns:
            List[ReportEntry]: List of all calculated results.
        """
        requested_metrics = (
            [requested_metrics]
            if isinstance(requested_metrics, EBasicReportMetric)
            else (
                requested_metrics
                if isinstance(requested_metrics, list)
                else [e for e in EBasicReportMetric]
            )
        )

        for req_metric in requested_metrics:
            match req_metric:
                case EBasicReportMetric.ADJECENCY_MATRIX:
                    self.calc_adjacency_matrix()
                case EBasicReportMetric.MARKOV_BLANKET:
                    self.calc_markov_blankets()
                case EBasicReportMetric.CONNECTIVITY:
                    self.calc_connectivity_ranking()

        # print all results
        self._print_metric_results(self.collected_results, requested_metrics)
        return self.get_report_entries()

    def calc_adjacency_matrix(self) -> Tuple[np.array, List[str]]:
        """Calculates the adjecency matrix with regard to the provided network.

        Returns:
            Tuple[np.Array, List[str]]: The matrix where an entry representes a dircted edge between two nodes (provided via the list of nodes returned)
        """
        nodes = sorted(list(self.investigated_bn.model_elements.keys()))
        edges = self.investigated_bn.node_connections

        # get the adjecency matrix itself
        n = len(nodes)
        matrix = np.zeros((n, n), dtype=str)
        for i in range(n):
            for j in range(n):
                if (nodes[i], nodes[j]) in edges or (nodes[j], nodes[i]) in edges:
                    matrix[i, j] = matrix[j, i] = "X"
                else:
                    matrix[i, j] = matrix[j, i] = " "

        self.collected_results[EBasicReportMetric.ADJECENCY_MATRIX] = (
            result := (matrix, nodes)
        )
        return result

    def calc_markov_blankets(self):
        result = {}
        for node in sorted(self.investigated_bn.model_elements.keys()):
            children = list(self.investigated_bn.successors(node))
            parents = list(self.investigated_bn.predecessors(node))
            blanket_nodes = children + parents
            for child_node in children:
                blanket_nodes.extend(
                    list(self.investigated_bn.predecessors(child_node))
                )
            blanket_nodes = set(blanket_nodes)
            blanket_nodes.discard(node)
            result[node] = sorted(list(blanket_nodes))

        self.collected_results[EBasicReportMetric.MARKOV_BLANKET] = result
        return result

    def calc_connectivity_ranking(self):
        result = {}  # Dict[str, Tuple[int, List[str]]
        roots = self.investigated_bn.get_root_node_names()

        for node in sorted(self.investigated_bn.model_elements.keys()):
            indegree = len(self.investigated_bn.model_elements[node].evidence)
            ancestors = sorted(list(set(nx.ancestors(self.investigated_bn, node))))

            result[node] = (indegree, ancestors)

        self.collected_results[EBasicReportMetric.CONNECTIVITY] = result
        return result

    def _print_metric_results(
        self,
        metrics_results: Dict[EBasicReportMetric, Any],
        requested_metrics: List[EBasicReportMetric],
    ):

        print("\n=== Reporting basic results ===")

        # "print" graph structure
        nx.write_network_text(
            self.investigated_bn,
            vertical_chains=True,
            max_depth=20,
        )

        for calculated_metric, results in metrics_results.items():

            if not results:
                continue

            if calculated_metric not in requested_metrics:
                continue

            match calculated_metric:
                case EBasicReportMetric.ADJECENCY_MATRIX:

                    print(
                        "The adjacency matrix, sometimes also called the connection matrix, of a simple labeled graph is a matrix "
                        "with rows and columns labeled by graph vertices, with a 'X' or ' ' in position (v_i, v_j) according to whether v_i and v_j "
                        "are adjacent or not.  An entry therefore marks a (directed) edge between two vertices. "
                        "For a simple graph with no self-loops, the adjacency matrix must have no entries on the diagonal."
                    )

                    (matrix, node_order) = results
                    print_2d_table(matrix, col_header=node_order, row_header=node_order)
                    print("-" * 50)

                case EBasicReportMetric.MARKOV_BLANKET:
                    print(
                        "A Markov Blanket of a random variable in a Bayesian Network refers to a set of variables that, when observed, "
                        "shields the variable from the influence of all other nodes in the network. "
                        "Elements in the blanket consist of the parents, the children, and the parents of the children nodes with respect to a target node."
                    )
                    print_dict_with_meta(
                        results,
                        preamble=None,
                        postamble="-" * 50,
                        nested_key_prefix="",
                    )

                case EBasicReportMetric.CONNECTIVITY:
                    print(
                        "The below output provides an overview of the connectivity of a node in the underlying network."
                    )
                    total_nodes = len(self.investigated_bn.model_elements.keys())
                    total_indegree = 0

                    for node, (indegree, ancestors) in results.items():
                        total_indegree += indegree
                        print(
                            f">> {node} has an indeegree of {indegree}.\n"
                            f"It has a total of {len(ancestors)} ancestor nodes and is therefore influenced by {len(ancestors)} out of {total_nodes} / {round(100*(len(ancestors)/total_nodes), 3)}%  nodes in the model.\n"
                            f"The ancestors are: {ancestors}.\n"
                        )

                    print(
                        f"\nThe average indegree per node is {round(total_indegree/total_nodes, 4)}."
                    )
                    print("-" * 50)

    def get_report_entries(self) -> List[ReportEntry]:
        return [
            ReportEntry(
                scoped_name="Graph",
                metric=None,
                report_origin=EReportOrigin.BASIC_REPORTER,
                data=self.investigated_bn,
                timestamp=time.time(),
                scope=EReportScope.NETWORK_LEVEL,
                misc=None,
            )
        ]
