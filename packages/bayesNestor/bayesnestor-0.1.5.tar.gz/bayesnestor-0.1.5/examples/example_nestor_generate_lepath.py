import os
import sys

cur_dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(cur_dir_path, os.pardir)))
from bayesnestor import nestor
from bayesnestor.utils.ParameterContainer import ENestorVariant

QUERY_EVIDENCE = {
    "Active_Reflective_Dim": "Active",
    "Sensory_Intuitive_Dim": "Intuitive",
    "Visual_Verbal_Dim": "Visual",
    "Sequential_Global_Dim": "Global",
    "cs": "agree",
    "bfia": "disagree"
}

mynestor = nestor()
for tup in mynestor.generate(evidence=QUERY_EVIDENCE):
    print(tup)

print("-" * 50)
print(
    "Changing Nestor-Variant and re-generating a learning path for the same observation"
)
print("-" * 50)
mynestor.configure(ENestorVariant.FULL_COGNITIVE)
for tup in mynestor.generate(evidence=QUERY_EVIDENCE):
    print(tup)
