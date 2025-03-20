import os
import sys

import numpy as np

cur_dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(cur_dir_path, os.pardir)))

from bayesnestor.core.BayesianNetwork import BayesianNetwork
from bayesnestor.core.ConditionalProbabilityTable import CPT
from bayesnestor.core.ModelManager import ModelManager


def generateCondProbs(var_card, ev_cards):

    length = np.prod(ev_cards) if len(ev_cards) > 0 else 1

    res = []

    for i in range(length):
        cur_probs = np.abs(np.random.normal(size=var_card))
        cur_probs /= cur_probs.sum()
        res.append(cur_probs)

    return np.array(res).transpose()


def make_bn(bn_name):

    node_connections = [
        ("NODE_A", "NODE_C"),
        ("NODE_B", "NODE_D"),
        ("NODE_C", "NODE_D"),
        ("NODE_A", "NODE_E"),
        ("NODE_B", "NODE_E"),
        ("NODE_C", "NODE_E"),
        ("NODE_D", "NODE_E"),
    ]

    bn = BayesianNetwork(bn_name, node_connections)

    NODE_A = CPT(
        name="NODE_A",
        variable_card=2,
        values=generateCondProbs(var_card=2, ev_cards=[]),
        evidence=None,
        evidence_card=None,
        state_names={"NODE_A": ["STATE_NODE_A_Yes", "STATE_NODE_A_No"]},
    )

    NODE_B = CPT(
        name="NODE_B",
        variable_card=2,
        values=generateCondProbs(var_card=2, ev_cards=[]),
        evidence=None,
        evidence_card=None,
        state_names={"NODE_B": ["STATE_NODE_B_Yes", "STATE_NODE_B_No"]},
    )

    NODE_C = CPT(
        name="NODE_C",
        variable_card=2,
        values=generateCondProbs(var_card=2, ev_cards=[2]),
        evidence=["NODE_A"],
        evidence_card=[2],
        state_names={
            "NODE_A": ["STATE_NODE_A_Yes", "STATE_NODE_A_No"],
            "NODE_C": ["STATE_NODE_C_Yes", "STATE_NODE_C_No"],
        },
    )

    NODE_D = CPT(
        name="NODE_D",
        variable_card=2,
        values=generateCondProbs(var_card=2, ev_cards=[2, 2]),
        evidence=["NODE_B", "NODE_C"],
        evidence_card=[2, 2],
        state_names={
            "NODE_B": ["STATE_NODE_B_Yes", "STATE_NODE_B_No"],
            "NODE_C": ["STATE_NODE_C_Yes", "STATE_NODE_C_No"],
            "NODE_D": ["STATE_NODE_D_Yes", "STATE_NODE_D_No"],
        },
    )

    NODE_E = CPT(
        name="NODE_E",
        variable_card=3,
        values=generateCondProbs(var_card=3, ev_cards=[2, 2, 2, 2]),
        evidence=["NODE_A", "NODE_B", "NODE_C", "NODE_D"],
        evidence_card=[2, 2, 2, 2],
        state_names={
            "NODE_A": ["STATE_NODE_A_Yes", "STATE_NODE_A_No"],
            "NODE_B": ["STATE_NODE_B_Yes", "STATE_NODE_B_No"],
            "NODE_C": ["STATE_NODE_C_Yes", "STATE_NODE_C_No"],
            "NODE_D": ["STATE_NODE_D_Yes", "STATE_NODE_D_No"],
            "NODE_E": ["STATE_NODE_E_1", "STATE_NODE_E_2", "STATE_NODE_E_3"],
        },
    )

    bn.add_cpts(NODE_A, NODE_B, NODE_C, NODE_D, NODE_E)

    return bn


TEST_FILE = r"examples\data\example_xmlbif.xml"

model_manager = ModelManager()

print("--- Create models from file")

model_manager.create_model(TEST_FILE)
instances = model_manager.get_handles(TEST_FILE)

q_res = []
for inst, meta in instances.values():

    q_res.append(
        round(
            inst.query(
                variables="dog_out",
            ).values[
                0
            ][0],
            4,
        )
    )

print(
    f"Asserting that all backends loaded the correct model and yield consistent inference results: {len(set(q_res)) == 1}"
)


print("--- Create models from custom BN defintion")
bn = make_bn("Test")
model_manager.create_model(bn)

instances = model_manager.get_handles(bn)

q_res = []
for inst, meta in instances.values():

    q_res.append(
        round(
            inst.query(
                variables="NODE_D",
            ).values[
                0
            ][0],
            4,
        )
    )

print(
    f"Asserting that all backends loaded the correct model and yield consistent inference results: {len(set(q_res)) == 1}"
)
