import time
import warnings
from typing import Any, Dict, List, Union

import dowhy.causal_estimators.linear_regression_estimator as natural_effect_estimator
import numpy as np
import pandas as pd
from dowhy import CausalModel, gcm
from tqdm import tqdm

from bayesnestor.core.backends.BackendPgmpy import PgmpyInference
from bayesnestor.core.BayesianNetwork import BayesianNetwork
from bayesnestor.reporting.IReporting import IReporting
from bayesnestor.reporting.ReportingContainers import (
    EDoWhyReportMetric,
    EReportOrigin,
    EReportScope,
    ReportEntry,
)
from bayesnestor.reporting.ReportingUtils import print_dict_with_meta

warnings.filterwarnings("ignore")
warnings.simplefilter(action="ignore", category=FutureWarning)


NATURAL_EFFECT_CALC_STABLE_PIP_ENV = False


class DoWhyReporter(IReporting):

    investigated_bn = None
    dowhy_gcm = None
    underlying_data = None
    _raw_collected_results = (
        None
    )
    report_entries = None

    def __init__(self, bn: BayesianNetwork, data: pd.DataFrame = None):

        if isinstance(bn, BayesianNetwork):
            self.investigated_bn = bn
        else:
            raise ValueError(
                f"The model to be investigated needs to be a BayesianNetwork but a variable with type {type(model)} was passed."
            )

        if isinstance(data, pd.DataFrame):
            self.underlying_data = data

        else:
            self.underlying_data = PgmpyInference(bn).reconstruct_dataset(1e6)

        self._raw_collected_results = {e: {} for e in EDoWhyReportMetric}
        self._create_dowhy_gcms(self.investigated_bn, self.underlying_data)

    def _create_dowhy_gcms(
        self, bn: BayesianNetwork, data: pd.DataFrame = None, fast: bool = True
    ) -> None:
        """Internal helper function to initialize a doWhy-Causal Model object from the internal BayesianNetwork representation.
            If no data is provided, this method automatically generates consistent data by sampling from the internal, parameterized BN.
            Discrete BNs are assumed for assigning the causal mechanisms. If this option might not hold and automatical fit of
            causal mechanisms can be triggered by setting the 'fast' option to False. This might take a considerable amount of time.

        Args:
            bn (BayesianNetwork): Instance of a module internal BN.
            data (pd.DataFrame, optional): Data that is consistent with the BN. Defaults to None.
            fast (bool, optional): Whether or not causal mechanisms should be optimized (with regard to the data).
            Defaults to True and therefore a default set of mechanims is used assuming a discrete model.
        """

        dag = bn.get_dag()

        self.dowhy_gcm = gcm.InvertibleStructuralCausalModel(dag)

        if fast:
            for root_node in self.investigated_bn.get_root_node_names():
                self.dowhy_gcm.set_causal_mechanism(
                    root_node, gcm.stochastic_models.EmpiricalDistribution()
                )

            conditional_nodes = (
                set(self.investigated_bn.model_elements.keys())
                - set(self.investigated_bn.get_root_node_names())
                - set(self.investigated_bn.get_independent_nodes())
            )
            for conditional_node in conditional_nodes:
                self.dowhy_gcm.set_causal_mechanism(
                    conditional_node,
                    gcm.ClassifierFCM(
                        gcm.ml.create_logistic_regression_classifier(max_iter=8000)
                    ),
                )

        else:
            print(
                "Due to setting the 'fast' option to False the internal causal model is extensively evaluated.\n"
                "This might take a significant amount of time."
            )
            _ = gcm.auto.assign_causal_mechanisms(
                self.dowhy_gcm,
                data,
                override_models=True,
                quality=gcm.auto.AssignmentQuality.BETTER,
            )

        gcm.fit(self.dowhy_gcm, data)

    def generate_report(
        self,
        target_node: Union[str, List[str]] = None,
        requested_metrics: Union[EDoWhyReportMetric, List[EDoWhyReportMetric]] = None,
    ) -> List[ReportEntry]:
        """Main method to calculate and output different doWhy metrics with regard to a Bayesian Network.
            If no target_node(s) are provided, all specified metrics are calculated for all leaf nodes of the network.
            If no requested_metrics are provided, all implemented metrics are calculated.

        Args:
            target_node (Union[str, List[str]], optional): "Outcome" node which acts as a reference target node with regard to the specified metircs. Defaults to None.
            requested_metrics (Union[EBasicReportMetric, List[EBasicReportMetric]], optional): Metrics which should be calculated. If no metric(s) are provided, all implmented algorithms are executed. Defaults to None.

        Raises:
            ValueError: Raised if an invalid metric is requested.

        Returns:
            List[ReportEntry]: List of all calculated results.
        """
        targets = (
            [target_node]
            if isinstance(target_node, str)
            else self.investigated_bn.get_leaf_node_names()
        )

        requested_metrics = (
            [requested_metrics]
            if isinstance(requested_metrics, EDoWhyReportMetric)
            else (
                requested_metrics
                if isinstance(requested_metrics, list)
                else [e for e in EDoWhyReportMetric]
            )
        )

        for node in (pbar := tqdm(targets)):
            pbar.set_description(f"Calculating metrics for node {node}")

            for req_metric in requested_metrics:
                match req_metric:
                    case EDoWhyReportMetric.INTRINSIC_CAUSAL_INFLUENCE:
                        self.calc_intrinsic_causal_influence(node)
                    case EDoWhyReportMetric.PARENTAL_FEATURE_RELEVANCE:
                        self.calc_parental_feature_relevance(node)
                    case EDoWhyReportMetric.AVERAGE_CAUSAL_EFFECT:
                        self.calc_average_causal_effect(node)
                    case EDoWhyReportMetric.DIRECT_EFFECT:
                        self.calc_direct_effect(node)
                    case EDoWhyReportMetric.NATURAL_DIRECT_EFFECT:
                        self.calc_natural_effect(node, req_metric)
                    case EDoWhyReportMetric.NATURAL_INDIRECT_EFFECT:
                        self.calc_natural_effect(node, req_metric)
                    case _:
                        raise ValueError(
                            f"The requested metric {str(req_metric)} with type {type(req_metric)} is not supported."
                        )

        # print all results
        self._print_metric_results(self._raw_collected_results, requested_metrics)

        return self.get_report_entries()

    def calc_intrinsic_causal_influence(self, target_node: str) -> Dict[str, float]:
        """Calculates the Intrinsic Causal Influences with regard to the specified target node.
           See https://www.pywhy.org/dowhy/v0.11.1/user_guide/causal_tasks/quantify_causal_influence/icc.html

        Args:
            target_node (str): Target node who's statistical property is to be attributed.

        Returns:
            Dict[str, float]: Intrinsic Causal Influence of each ancestor node.
        """

        mean_absolute_deviation_estimator = lambda x, y: np.mean(abs(x - y))

        result = gcm.intrinsic_causal_influence(
            self.dowhy_gcm,
            target_node=target_node,
            num_samples_randomization=2000,
            max_batch_size=500,
            attribution_func=mean_absolute_deviation_estimator,
        )
        self._raw_collected_results[EDoWhyReportMetric.INTRINSIC_CAUSAL_INFLUENCE][
            target_node
        ] = result

        return result

    def calc_parental_feature_relevance(self, target_node: str) -> Dict[str, float]:
        """Calculates the Parental Feature Relevances with regard to the specified target node.
           See https://www.pywhy.org/dowhy/v0.11.1/user_guide/causal_tasks/root_causing_and_explaining/feature_relevance.html

        Args:
            target_node (str): Node of interest.

        Returns:
            Dict[str, float]: Parental Feature Relevance for each direct parent of the specified target node.
        """

        parent_relevances, noise_relevance = gcm.parent_relevance(
            self.dowhy_gcm,
            target_node=target_node,
            num_samples_randomization=2000,
            max_batch_size=500,
        )

        result = {parent: val for (parent, target), val in parent_relevances.items()}
        result["Noise"] = noise_relevance

        self._raw_collected_results[EDoWhyReportMetric.PARENTAL_FEATURE_RELEVANCE][
            target_node
        ] = result

        return result

    def calc_direct_effect(self, target_node: str) -> Dict[str, float]:
        """Calculate the Direct Effects (arrow strenghts) with regard to a target node.
           See https://www.pywhy.org/dowhy/v0.11.1/user_guide/causal_tasks/quantify_causal_influence/quantify_arrow_strength.html

        Args:
            target_node (str): Node of interest.

        Returns:
            Dict[str, float]: Causal strenght per ingoing edges.
        """
        mean_diff_estimator = lambda y_old, y_new: np.mean(y_new) - np.mean(y_old)

        arrow_strenghts = gcm.arrow_strength(
            self.dowhy_gcm,
            target_node=target_node,
            difference_estimation_func=mean_diff_estimator,
        )

        self._raw_collected_results[EDoWhyReportMetric.DIRECT_EFFECT][target_node] = (
            result := {parent: val for (parent, target), val in arrow_strenghts.items()}
        )

        return result

    def calc_average_causal_effect(
        self, target_node: str, treatment_opts: Union[str, List[str]] = None
    ) -> Dict[str, float]:
        """Calculate the Average Causal Effects (ACE) with regard to a target node.
            The target/treatment can be a continuous real-valued variable or a categorical variable but must be binary.
            If no treatment nodes are provided, this function defaults to calculating the ACEs of all direct parent nodes.
            See https://www.pywhy.org/dowhy/v0.11.1/user_guide/causal_tasks/estimating_causal_effects/effect_estimation_with_gcm.html

        Args:
            target_node (str): Node of interest ("outcome").
            treatment_opts (Union[str, List[str]], optional): List of individual "treatment" nodes. Defaults to None

        Returns:
            Dict[str, float]: The estimated ACE per treatment for the target_node.
        """

        target_card = self.investigated_bn.model_elements[target_node].variable_card
        if target_card != 2:
            print(
                f"Cannot calculate ACE for target node {target_node} given it has too many states ({target_card})"
            )
            return {}

        treatment_opts = (
            treatment_opts
            if isinstance(treatment_opts, list)
            else (
                [treatment_opts]
                if isinstance(treatment_opts, str)
                else self.investigated_bn.predecessors(target_node)
            )
        )
        result = {}

        for treatment in treatment_opts:
            treatment_card = self.investigated_bn.model_elements[
                treatment
            ].variable_card

            if treatment_card != 2:
                print(
                    f"Cannot calculate ACE for target node {target_node} given its treatment {treatment} as it has too many states ({treatment_card})"
                )

            else:
                treamtent_states = self.investigated_bn.model_elements[
                    treatment
                ].state_names.get(treatment, list(range(treatment_card)))

                ACE = gcm.average_causal_effect(
                    self.dowhy_gcm,
                    target_node=target_node,
                    interventions_alternative={
                        treatment: lambda x: treamtent_states[1]
                    },
                    interventions_reference={treatment: lambda x: treamtent_states[0]},
                    num_samples_to_draw=1000,
                )

                result[treatment] = ACE

        self._raw_collected_results[EDoWhyReportMetric.AVERAGE_CAUSAL_EFFECT][
            target_node
        ] = result

        return result

    def calc_natural_effect(
        self,
        target_node: str,
        kind: Union[
            EDoWhyReportMetric.NATURAL_DIRECT_EFFECT,
            EDoWhyReportMetric.NATURAL_INDIRECT_EFFECT,
        ],
        treatment_opts: Union[str, List[str]] = None,
    ) -> Dict[str, float]:
        """Calculate the Natural (IN)Direct Effect with regard to a target node.
            If no treatment nodes are provided, this function defaults to calculating the NDE/NIEs of all direct parent nodes.
            See https://www.pywhy.org/dowhy/v0.11.1/user_guide/causal_tasks/quantify_causal_influence/mediation_analysis.html

        Args:
            target_node (str): Node of interest.
            kind (Union[ EDoWhyReportMetric.NATURAL_DIRECT_EFFECT, EDoWhyReportMetric.NATURAL_INDIRECT_EFFECT, ]): Selector which effect should be calculated
            treatment_opts (Union[str, List[str]], optional): List of individual "treatment" nodes. Defaults to None.

        Returns:
            Dict[str, float]: The Natural Effect per treatment node.
        """
        result = {}
        treatment_opts = (
            treatment_opts
            if isinstance(treatment_opts, list)
            else (
                [treatment_opts]
                if isinstance(treatment_opts, str)
                else self.investigated_bn.predecessors(target_node)
            )
        )

        if (
            NATURAL_EFFECT_CALC_STABLE_PIP_ENV
        ):
            estimand_key_mapping = {
                DoWhyReporter.NATURAL_DIRECT_EFFECT: "nonparametric-nde",
                DoWhyReporter.NATURAL_INDIRECT_EFFECT: "nonparametric-nie",
            }

            for treatment in treatment_opts:
                tmp_causal_model = CausalModel(
                    data=self.underlying_data,
                    treatment=treatment,
                    outcome=target_node,
                    graph=self.investigated_bn,
                )

                estimand = tmp_causal_model.identify_effect(
                    estimand_type=estimand_key_mapping[kind],
                    proceed_when_unidentifiable=True,
                )
                result[treatment] = tmp_causal_model.estimate_effect(
                    identified_estimand=estimand,
                    method_name="mediation.two_stage_regression",
                    confidence_intervals=False,
                    test_significance=False,
                    method_params={
                        "first_stage_model": natural_effect_estimator.LinearRegressionEstimator,
                        "second_stage_model": natural_effect_estimator.LinearRegressionEstimator,
                    },
                )

        self._raw_collected_results[kind][target_node] = result
        return result

    def _print_metric_results(
        self,
        metrics_results: Dict[EDoWhyReportMetric, Any],
        requested_metrics: List[EDoWhyReportMetric],
    ):
        """Internal helper function to print the calculated metrics (requested via generate_report(...) to the terminal.

        Args:
            metrics_results (Dict[EDoWhyReportMetric, Any]): Internal storage of calcualted results.
            requested_metrics (List[EDoWhyReportMetric]): Metrics to print.
        """

        print("\n=== Reporting results using DoWhy ===")

        for calculated_metric, results in metrics_results.items():

            if not results:
                continue

            if calculated_metric not in requested_metrics:
                continue

            preamble_str = None
            match calculated_metric:
                case EDoWhyReportMetric.INTRINSIC_CAUSAL_INFLUENCE:
                    print(
                        "By quantifying intrinsic causal influence, we answer the question: \n"
                        "How strong is the causal influence of an upstream node to a target node that is not inherited from the parents of the upstream node?",
                    )
                    preamble_str = f"Intrinsic Causal Influences "

                case EDoWhyReportMetric.PARENTAL_FEATURE_RELEVANCE:
                    print(
                        "In the context of feature attribution, we address the following question: \n"
                        "How relevant is a feature for my target? "
                        "The output below evaluates the global relevance (population/distribution level) of the parents "
                        "with respect to their contribution to the variance of the target node.",
                    )
                    preamble_str = f"Feature relevances of the x "

                case EDoWhyReportMetric.DIRECT_EFFECT:
                    print(
                        "By quantifying the strength of an arrow, we answer the question: \n"
                        "How strong is the causal influence from a cause to its direct effect? "
                        "The output below measures the direct influence of a parent node with respect to the change in the "
                        "mean of a child, where influences through paths over other nodes are ignored.",
                    )
                    preamble_str = f"Direct effects of x "

                case EDoWhyReportMetric.AVERAGE_CAUSAL_EFFECT:
                    print(
                        "By quantifying the Average Causal Effect (ACE), we answer the question: \n"
                        "How much does a certain target quantity differ under two different interventions/treatments? "
                        "The output below quantifies the comparison of two treatments, i.e. what is the difference "
                        "of my target quantity on average given treatment A vs treatment B.",
                    )
                    preamble_str = f"Average Causal Effect of x "

                case EDoWhyReportMetric.NATURAL_DIRECT_EFFECT:
                    print(
                        "The Natural Direct Effect (NDE) measures the expected increase in the target variable as a treatment "
                        "changes from T_0 to T_1, while setting a mediator variable to whatever value it would have attained (for each individual) "
                        "prior to the change, that is, under T_0.\n"
                        "Semantically, NDE measures the portion of the total effect that would be transmitted to the target variable "
                        "absent a mediators ability to respond to a treatment."
                    )
                    preamble_str = f"Natural Direct effects (NDE) of x "

                case EDoWhyReportMetric.NATURAL_INDIRECT_EFFECT:
                    print(
                        "The Natural Indirect Effect (NIE) measures the expected increase in the target variable when a treatment T is held constant, "
                        "at T_0, and a mediator variable M changes to whatever value it would have attained (for each individual) under T_1. "
                        "Semantically, NIE measures the portion of the total effect transmitted absent the target variables ability to respond to "
                        "changes in the treatment, except those transmitted through nediators."
                    )
                    preamble_str = f"Natural Indirect Direct (NIE) effects of x "

            for target_node, data in results.items():
                print_dict_with_meta(
                    data,
                    preamble=preamble_str + f" for node {target_node}",
                    postamble="-" * 50,
                    nested_key_prefix="",
                )

    def get_report_entries(self) -> List[ReportEntry]:
        """Return all currently stored calculation results.

        Returns:
            List[ReportEntry]: Currently stored results.
        """
        self._report_entries = self._convert_to_report_entries(
            self._raw_collected_results
        )
        return self._report_entries

    def _convert_to_report_entries(
        self,
        metrics_results: Dict[EDoWhyReportMetric, Any],
    ) -> List[ReportEntry]:
        """Internal helper function to convert the internal data storage to a list of standardized ReportEntry-objects.

        Args:
            metrics_results (Dict[EDoWhyReportMetric, Any]):  Internal storage of calcualted results.

        Returns:
            List[ReportEntry]: Currently stored results.
        """

        report_entries = []
        for report_type, data in metrics_results.items():
            if data:
                for primary_node in self.investigated_bn.model_elements.keys():
                    result = data.get(primary_node, None)
                    if result:
                        report_entries.append(
                            ReportEntry(
                                scope=EReportScope.NODE_LEVEL,
                                scoped_name=primary_node,
                                metric=report_type,
                                report_origin=EReportOrigin.DOWHY_REPORTER,
                                data=result,
                                timestamp=time.time(),
                                misc=None,
                            )
                        )

        return report_entries
