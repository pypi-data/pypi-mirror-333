import numpy as np
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork

# Define the structure of the Bayesian Network
model = BayesianNetwork([("A", "C"), ("B", "C")])

# Define the CPDs (Conditional Probability Distributions)
cpd_a = TabularCPD(variable="A", variable_card=2, values=[[0.55], [0.45]])
cpd_b = TabularCPD(variable="B", variable_card=2, values=[[0.6], [0.4]])
cpd_c = TabularCPD(
    variable="C",
    variable_card=2,
    values=[[0.8, 0.1, 0.55, 0.5], [0.2, 0.9, 0.45, 0.5]],
    evidence=["A", "B"],
    evidence_card=[2, 2],
)

# Add CPDs to the model
model.add_cpds(cpd_a, cpd_b, cpd_c)

# Validate the model
assert model.check_model()


def prune_network(model, hypotheses, evidence):
    pruned_model = model.copy()
    all_nodes = set(model.nodes())
    evidence_vars = set(evidence.keys())
    hypotheses_vars = set(hypotheses)

    for node in all_nodes - evidence_vars - hypotheses_vars:
        should_remove = True
        for h in hypotheses:
            if model.is_dconnected(node, h, evidence_vars):
                should_remove = False
                break
        if should_remove:
            pruned_model.remove_node(node)

    return pruned_model


def compute_posteriors(model, evidence):
    inference = VariableElimination(model)
    posteriors = {}
    for node in model.nodes():
        if node not in evidence:
            result = inference.query(variables=[node], evidence=evidence)
            posteriors[node] = result.values
    return posteriors


def is_map_independent(model, R, h_star, evidence):
    compute_posteriors(model, evidence)
    R_values = model.get_cpds(R).state_names[R]

    for r in R_values:
        new_evidence = evidence.copy()
        new_evidence[R] = r
        posteriors_h_prime = compute_posteriors(model, new_evidence)
        max_h_prime = max(
            posteriors_h_prime, key=lambda h: np.sum(posteriors_h_prime[h])
        )
        if max_h_prime != h_star:
            return False
    return True


def find_relevant_singletons(model, hypotheses, evidence):
    relevant_singletons = set()
    for R in model.nodes():
        if R in hypotheses or R in evidence:
            continue

        h_star = max(
            hypotheses, key=lambda h: np.sum(compute_posteriors(model, evidence)[h])
        )

        if not is_map_independent(model, R, h_star, evidence):
            relevant_singletons.add(R)

    return relevant_singletons


def find_relevant_sets(model, hypotheses, evidence):
    relevant_singletons = find_relevant_singletons(model, hypotheses, evidence)
    relevant_sets = {frozenset([r]) for r in relevant_singletons}

    for R in relevant_singletons:
        for U in relevant_singletons:
            if R != U:
                combined_set = frozenset([R, U])
                if combined_set not in relevant_sets:
                    combined_evidence = evidence.copy()
                    for r_val in model.get_cpds(R).state_names[R]:
                        for u_val in model.get_cpds(U).state_names[U]:
                            combined_evidence[R] = r_val
                            combined_evidence[U] = u_val
                            if not model.d_separated(
                                hypotheses[0], list(combined_set), combined_evidence
                            ):
                                relevant_sets.add(combined_set)
                                break

    return relevant_sets


def compute_exp_relevance(model, R, hypotheses, evidence):
    exp_rel = 0
    h_star = max(
        hypotheses, key=lambda h: np.sum(compute_posteriors(model, evidence)[h])
    )
    posteriors_h_star = compute_posteriors(model, evidence)

    R_values = model.get_cpds(R).state_names[R]
    for r in R_values:
        new_evidence = evidence.copy()
        new_evidence[R] = r
        posteriors_h_prime = compute_posteriors(model, new_evidence)
        max_h_prime = max(
            posteriors_h_prime, key=lambda h: np.sum(posteriors_h_prime[h])
        )
        if max_h_prime != h_star:
            exp_rel += posteriors_h_star[R][R_values.index(r)]
    return exp_rel


def compute_avg_relevance(model, R, hypotheses, evidence):
    avg_rel = 0
    h_star = max(
        hypotheses, key=lambda h: np.sum(compute_posteriors(model, evidence)[h])
    )
    compute_posteriors(model, evidence)

    R_values = model.get_cpds(R).state_names[R]
    rel_count = 0
    for r in R_values:
        new_evidence = evidence.copy()
        new_evidence[R] = r
        posteriors_h_prime = compute_posteriors(model, new_evidence)
        max_h_prime = max(
            posteriors_h_prime, key=lambda h: np.sum(posteriors_h_prime[h])
        )
        avg_rel += np.sum(posteriors_h_prime[max_h_prime])
        rel_count += 1
    if rel_count > 0:
        avg_rel /= rel_count
    return avg_rel


def explain_relevance(model, hypotheses, evidence):
    relevant_singletons = find_relevant_singletons(model, hypotheses, evidence)
    explanations = {}

    for R in relevant_singletons:
        exp_rel = compute_exp_relevance(model, R, hypotheses, evidence)
        avg_rel = compute_avg_relevance(model, R, hypotheses, evidence)
        explanations[R] = {"Expected Relevance": exp_rel, "Average Relevance": avg_rel}

    return explanations


# Example usage
evidence = {}  # {"B": 0}
hypotheses = ["A"]
pruned_model = prune_network(model, hypotheses, evidence)
relevant_sets = find_relevant_sets(pruned_model, hypotheses, evidence)
explanations = explain_relevance(pruned_model, hypotheses, evidence)

print("Relevant sets:", relevant_sets)
print("Relevance explanations:", explanations)
