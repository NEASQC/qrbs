import numpy as np
import pandas as pd
import qat.lang.AQASM as qlm
from qat.qpus import CLinalg
from qat.core.console import display

from qat.lang.models import KPTree

def proccess_qresults(result):
    """
    get quantum results
    """
    list_for_results = []
    for sample in result:
        list_for_results.append([
            sample.state, sample.state.lsb_int, sample.probability,
            sample.amplitude, sample.state.int,
        ])

    pdf = pd.DataFrame(
        list_for_results,
        columns=['States', "Int_lsb", "Probability", "Amplitude", "Int"]
    )
    pdf.sort_values(["Int_lsb"], inplace=True)
    return pdf

def _matrix_gen(inaccuracy):
    """
    Matrix M for M gate
    """
    theta = inaccuracy * np.pi / 2
    return np.array([
        [np.cos(theta), np.sin(theta)],
        [np.sin(theta), -np.cos(theta)]
    ])

M = qlm.AbstractGate("M", [float], arity=1, matrix_generator=_matrix_gen)

def init_state(alpha):
    """
    Initialize qubit state
    """
    tree = KPTree(np.array([np.sqrt(alpha), np.sqrt(1.0 - alpha)])).get_routine()
    return tree

def rule(certainty, alpha=0.8, precision=True):
    """
    Rule
    """

    routine = qlm.QRoutine()
    register = routine.new_wires(3)
    if precision == True:
        routine.apply(M(alpha), register[0])
    else:
        routine.apply(init_state(alpha), register[0])
    routine.apply(M(certainty), register[1])
    routine.apply(qlm.CCNOT, register[0], register[1], register[2])
    job = routine.to_circ().to_job(nbshots=0, qubits=[1])
    linalg_qpu = CLinalg()
    result = linalg_qpu.submit(job)
    return proccess_qresults(result), routine

def not_gate(alpha=0.8):
    """
    Not Gate
    """
    routine = qlm.QRoutine()
    register = routine.new_wires(2)
    routine.apply(init_state(alpha), register[0])
    routine.apply(qlm.CNOT, register[0], register[1])
    routine.apply(qlm.X, register[1])
    job = routine.to_circ().to_job(nbshots=0, qubits=[1])
    linalg_qpu = CLinalg()
    result = linalg_qpu.submit(job)
    return proccess_qresults(result), routine

def and_gate(alpha=0.8, beta=0.4, precision_alpha=True, precision_beta=True):
    """
    AND gate
    """
    routine = qlm.QRoutine()
    register = routine.new_wires(3)
    if precision_alpha == True:
        routine.apply(M(alpha), register[0])
    else:
        routine.apply(init_state(alpha), register[0])
    if precision_beta == True:
        routine.apply(M(beta), register[1])
    else:
        routine.apply(init_state(beta), register[1])
    routine.apply(qlm.CCNOT, register[0], register[1], register[2])
    job = routine.to_circ().to_job(nbshots=0, qubits=[2])
    linalg_qpu = CLinalg()
    result = linalg_qpu.submit(job)
    return proccess_qresults(result), routine

def or_gate(alpha=0.8, beta=0.4, precision_alpha=True, precision_beta=True):
    """
    OR gate
    """
    routine = qlm.QRoutine()
    register = routine.new_wires(3)
    if precision_alpha == True:
        routine.apply(M(alpha), register[0])
    else:
        routine.apply(init_state(alpha), register[0])
    if precision_beta == True:
        routine.apply(M(beta), register[1])
    else:
        routine.apply(init_state(beta), register[1])
    routine.apply(qlm.CCNOT, register[0], register[1], register[2])
    routine.apply(qlm.CNOT, register[0], register[2])
    routine.apply(qlm.CNOT, register[1], register[2])
    job = routine.to_circ().to_job(nbshots=0, qubits=[2])
    linalg_qpu = CLinalg()
    result = linalg_qpu.submit(job)
    return proccess_qresults(result), routine

def loss_rule(x, ouput_precision=0.8, precision=True):
    """
    loss for rule
    """
    certainty = x[0]
    alpha = x[1]
    pdf, _ = rule(certainty, alpha, precision=True)
    loss = (pdf["Probability"].iloc[1] - ouput_precision) ** 2
    print(loss)
    return loss

def loss_not(x, ouput_precision):
    alpha = x[0]
    pdf, _ = not_gate(alpha)
    print(pdf)
    loss = (pdf["Probability"].iloc[1] - ouput_precision) ** 2
    print(loss)
    return loss

def loss_and(x, ouput_precision, precision_alpha=True, precision_beta=True):
    pdf, _ = and_gate(alpha=x[0], beta=x[1], precision_alpha=True, precision_beta=True)
    loss = (pdf["Probability"].iloc[1] - ouput_precision) ** 2
    print(loss)
    return loss

def loss_or(x, ouput_precision, precision_alpha=True, precision_beta=True):
    pdf, _ = or_gate(alpha=x[0], beta=x[1], precision_alpha=True, precision_beta=True)
    loss = (pdf["Probability"].iloc[1] - ouput_precision) ** 2
    print(loss)
    return loss

from scipy.optimize import minimize

p_o = 0.8
p_r = 0.8
p_c = 0.6

x0 = np.array([p_r, p_c])

res = minimize(
    loss_rule,
    x0,
    args = (p_o, False),
    bounds = ((0.0, 1.0), (0.0, 1.0))
)



rule_c = res.x[0]
precedent_p = res.x[1]
print("Rule c before: {} and after {}".format(p_r, rule_c))
print("Precendent of rule before: {} and after {}".format(p_c, precedent_p))



res = minimize(
    loss_and,
    np.array([0.6, 0.9]),
    args = (precedent_p, True, True),
    bounds = ((0.0, 1.0), (0.0, 1.0))
)

print(res)

