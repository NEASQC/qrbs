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
    tree = KPTree(np.array([np.sqrt(1.0 - alpha), np.sqrt(alpha)])).get_routine()
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
    job = routine.to_circ().to_job(nbshots=0, qubits=[2])
    linalg_qpu = CLinalg()
    result = linalg_qpu.submit(job)
    return proccess_qresults(result), routine

def not_gate(alpha=0.8, precision=True):
    """
    Not Gate
    """
    routine = qlm.QRoutine()
    register = routine.new_wires(2)
    if precision == True:
        routine.apply(M(alpha), register[0])
    else:
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
    pdf, _ = rule(certainty, alpha, precision=precision)
    loss = (pdf["Probability"].iloc[1] - ouput_precision) ** 2
    return loss

def minimize_loss_rule(output_precision, precision=True):
    """
    Minimize loss function for rule
    """
    # Parameter to adjuts: Certainty of the rule
    rule_certainty = random()
    # Parameter to adjuts: Precision of precedent fact:
    precedent_precision = output_precision / rule_certainty
    # To avoid problems in minization some relationship
    # should be established
    while precedent_precision >= 1.0:
        rule_certainty = random()
        precedent_precision = output_precision / rule_certainty
    # print("rule_certainty: {}".format(rule_certainty))
    # print("pre:{}".format(precedent_precision))

    # Inital guess for optimization
    guest_rule = np.array([rule_certainty, precedent_precision])
    # Minimization
    res = minimize(
        loss_rule,
        guest_rule,
        args = (output_precision, precision),
        bounds = ((0.0, 1.0), (0.0, 1.0))
    )
    rule_certainty = res.x[0]
    precedent_precision = res.x[1]
    return rule_certainty, precedent_precision

def loss_not(x, ouput_precision, precision=True):
    """
    loss for NOT gate
    """
    alpha = x[0]
    pdf, _ = not_gate(alpha, precision=precision)
    loss = (pdf["Probability"].iloc[1] - ouput_precision) ** 2
    return loss

def minimize_loss_not(output_precision, precision=True):
    """
    minimize loss for NOT gate
    """
    # Parameter to adjuts: Precision of precedent fact:
    precedent_precision = 1.0 - output_precision
    # Inital guess for optimization
    guest_rule = np.array([precedent_precision])
    res = minimize(
        loss_not,
        guest_rule,
        args = (output_precision, precision),
        bounds = ((0.0, 1.0),)
    )
    precedent_precision = res.x[0]
    return precedent_precision


def loss_and(x, ouput_precision, precision_alpha=True, precision_beta=True):
    pdf, _ = and_gate(
        alpha=x[0],
        beta=x[1],
        precision_alpha=precision_alpha,
        precision_beta=precision_beta)
    loss = (pdf["Probability"].iloc[1] - ouput_precision) ** 2
    # print(loss)
    return loss

def minimize_loss_and(output_precision, precision_alpha=True, precision_beta=True):
    """
    Minimize loss function for AND
    """
    # Parameter to adjust: Precision of precedent facts:
    precision_a_fact = random()
    precision_b_fact = random()
    
    condition = min(precision_a_fact, precision_b_fact)
    while (condition < 0.8 * output_precision) or (condition > 1.2 * output_precision):
        precision_a_fact = random()
        precision_b_fact = random()
        condition = min(precision_a_fact, precision_b_fact)
        # print(
        #     precision_a_fact, precision_b_fact, condition,
        #     0.9 * output_precision, 1.1 * output_precision)


    # Inital guess for optimization
    guest_rule = np.array([precision_a_fact, precision_b_fact])
    # Minimization
    res = minimize(
        loss_and,
        guest_rule,
        args = (
            output_precision, 
            precision_alpha,
            precision_beta
        ),
        bounds = ((0.0, 1.0), (0.0, 1.0))
    )
    precision_a_fact = res.x[0]
    precision_b_fact = res.x[1]
    return precision_a_fact, precision_b_fact

def loss_or(x, ouput_precision, precision_alpha=True, precision_beta=True):
    pdf, _ = or_gate(
        alpha=x[0],
        beta=x[1],
        precision_alpha=precision_alpha,
        precision_beta=precision_beta
    )
    loss = (pdf["Probability"].iloc[1] - ouput_precision) ** 2
    # print(loss)
    return loss

def minimize_loss_or(output_precision, precision_alpha=True, precision_beta=True):
    """
    Minimize loss function for AND
    """
    # Parameter to adjust: Precision of precedent facts:
    precision_a_fact = random()
    precision_b_fact = random()
    condition = min(precision_a_fact, precision_b_fact)
    while (condition < 0.8 * output_precision) or (condition > 1.2 * output_precision):
        precision_a_fact = random()
        precision_b_fact = random()
        condition = max(precision_a_fact, precision_b_fact)
        # print(
        #     precision_a_fact, precision_b_fact, condition,
        #     0.9 * output_precision, 1.1 * output_precision)


    # Inital guess for optimization
    guest_rule = np.array([precision_a_fact, precision_b_fact])
    # Minimization
    res = minimize(
        loss_or,
        guest_rule,
        args = (output_precision, precision_alpha, precision_beta),
        bounds = ((0.0, 1.0), (0.0, 1.0))
    )
    precision_a_fact = res.x[0]
    precision_b_fact = res.x[1]
    return precision_a_fact, precision_b_fact

if __name__ == "__main__":
    from scipy.optimize import minimize
    from random import random

    # Precision del Hecho de Salida: P|1>
    output_precision = 0.4


    rule_certainty, precedent_precision = minimize_loss_rule(
        output_precision, precision=False
    )

    print("output_precision: "+str(output_precision))
    print("rule_certainty: "+str(rule_certainty))
    print("precedent_precision: "+str(precedent_precision))

    precedent_precision = minimize_loss_not(
        precedent_precision, precision=True
    )
    print("precedent_precision Not: "+str(precedent_precision))

    prec_a, prec_b = minimize_loss_and(precedent_precision, False, True)
    print("AND: prec_a: "+str(prec_a))
    print("AND: prec_b: "+str(prec_b))

    prec_a, prec_b = minimize_loss_or(precedent_precision, True, True)
    print("OR: prec_a: "+str(prec_a))
    print("OR: prec_b: "+str(prec_b))


    # pdf, c = rule(rule_c, alpha=precedent_p, precision=False)
    # display(c)
    # print(pdf)

    #res = minimize(
    #    loss_not,
    #    np.array([0.2]),
    #    args = (precedent_p, True),
    #    bounds = ((0.0, 1.0), )
    #)



    # res = minimize(
    #     loss_or,
    #     np.array([0.8, 0.8]),
    #     args = (precedent_p, True, True),
    #     bounds = ((0.0, 1.0), (0.0, 1.0))
    # )

    #print(res)

