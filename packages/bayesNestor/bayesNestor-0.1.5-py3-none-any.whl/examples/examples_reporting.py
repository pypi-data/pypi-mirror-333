import os
import sys
import warnings

warnings.filterwarnings("ignore")
warnings.simplefilter(action="ignore", category=FutureWarning)
cur_dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(cur_dir_path, os.pardir)))

import time

from bayesnestor.core.io.XmlBifReader import XMLBIFReader
from bayesnestor.reporting.BasicReporting import BasicReporter
from bayesnestor.reporting.DoWhyReporting import DoWhyReporter
from bayesnestor.reporting.ReportingContainers import EDoWhyReportMetric
from bayesnestor.reporting.VisualizeReporting import ReportVisualizer

TEST_FILE = r"pynestor\data\cn_LearnerCognitiveModel.xml"

bn = XMLBIFReader(TEST_FILE).get_model()


tic = time.perf_counter()

print("-- Generating a basic report of the model, using all implemented metrics ...")
base_reporter = BasicReporter(bn)
base_reporter.generate_report()
base_report_results = base_reporter.get_report_entries()


print(
    "-- Generate a 'causality'-based report for a specific target node with a sub-set of all metrics ..."
)
do_reporter = DoWhyReporter(bn)
print("-- Evaluate a metric directly...")
print(do_reporter.calc_average_causal_effect("LE"))

dowhy_report_results = do_reporter.generate_report(
    ["LE"],
    [
        EDoWhyReportMetric.PARENTAL_FEATURE_RELEVANCE,
        # EDoWhyReportMetric.AVERAGE_CAUSAL_EFFECT,
        # EDoWhyReportMetric.INTRINSIC_CAUSAL_INFLUENCE,
    ],
)

print("+" * 100)
rv = ReportVisualizer()
rv.visualize(base_report_results + dowhy_report_results, delay_mainproc=60)

toc = time.perf_counter()
print(f"Generating the reports took: {toc - tic:0.4f} seconds")
