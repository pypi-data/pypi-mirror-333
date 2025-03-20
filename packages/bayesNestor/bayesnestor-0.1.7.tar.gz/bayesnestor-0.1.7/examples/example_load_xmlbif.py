import os
import sys

cur_dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(cur_dir_path, os.pardir)))

from bayesnestor.core.backends.BackendPgmpy import PgmpyInference
from bayesnestor.core.backends.BackendPyAgrum import PyagrumInference
from bayesnestor.core.io.XmlBifReader import XMLBIFReader

TEST_FILE = r"bayesiannestor\data\cn_not_weighted.xml"

bn = XMLBIFReader(TEST_FILE).get_model()

bn.plot_graph()

agrum_model = PyagrumInference(bn)
pgmpy_model = PgmpyInference(bn)


print(
    "Asserting that all backends loaded the correct model and yield equal inference results:"
)
print(
    bool(
        agrum_model.query(
            variables="AAM", evidence={"Sequential_Global_Dim": "Global"}
        ).values[0]
        == pgmpy_model.query(
            variables="AAM", evidence={"Sequential_Global_Dim": "Global"}
        ).values[0]
    )
)
