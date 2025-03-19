import os
import sys
import warnings

warnings.filterwarnings("ignore")
warnings.simplefilter(action="ignore", category=FutureWarning)
cur_dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(cur_dir_path, os.pardir)))



from bayesnestor.core.backends.BackendPgmpy import PgmpyInference
from bayesnestor.core.backends.BackendPyAgrum import PyagrumInference
from bayesnestor.core.io.XmlBifReader import XMLBIFReader

TEST_FILE = r"pynestor\data\cn_weigthed.xml"

bn = XMLBIFReader(TEST_FILE).get_model()
agrum_model = PyagrumInference(bn)

underlying_data = PgmpyInference(bn).reconstruct_dataset(1e7).sample(n=1000)


pyagrum_bn = agrum_model._PyagrumInference__internal_model

import pyAgrum.lib.explain as expl

gumshap = expl.ShapValues(pyagrum_bn, "EX")

resultat = gumshap.conditional(
    underlying_data, plot=False, plot_importance=False, percentage=False
)
print(resultat)
a = 7
