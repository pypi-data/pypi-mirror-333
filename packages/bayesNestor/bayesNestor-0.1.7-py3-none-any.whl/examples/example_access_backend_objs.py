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

agrum_wrapped_model = PyagrumInference(bn)
pgmpy_wrapped_model = PgmpyInference(bn)


agrum_inst_model = agrum_wrapped_model._PyagrumInference__internal_model
pgmpy_inst_model = pgmpy_wrapped_model._PgmpyInference__internal_model

### use pgmpy library
from pgmpy.inference import VariableElimination

ie = VariableElimination(pgmpy_inst_model)
print(
    ie.query(
        variables=["AAM"],
        evidence={"Sequential_Global_Dim": "Global"},
    )
)


### use pyagrum library
from pyAgrum import LazyPropagation

ie = LazyPropagation(agrum_inst_model)
ie.setEvidence({"Sequential_Global_Dim": "Global"})
ie.makeInference()
ie.posterior("AAM")
print(ie.posterior("AAM"))
