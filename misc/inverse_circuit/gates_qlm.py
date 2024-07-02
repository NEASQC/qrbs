"""
Inferential gates in qlm
"""
import numpy as np
import pandas as pd
import qat.lang.AQASM as qlm
from qat.lang.models import KPTree

def solve_qjob(job, qpu):
    """
    get quantum results
    """
    result = qpu.submit(job)
    return proccess_qresults(result, 1, complete=True)

def proccess_qresults(result, qubits, complete=False):
    """
    Post Process a QLM results for creating a pandas DataFrame

    Parameters
    ----------

    result : QLM results from a QLM qpu.
        returned object from a qpu submit
    qubits : int
        number of qubits
    complete : bool
        for return the complete basis state.
    """

    # Process the results
    if complete:
        states = []
        list_int = []
        list_int_lsb = []
        for i in range(2**qubits):
            reversed_i = int("{:0{width}b}".format(i, width=qubits)[::-1], 2)
            list_int.append(reversed_i)
            list_int_lsb.append(i)
            states.append("|" + bin(i)[2:].zfill(qubits) + ">")

        probability = np.zeros(2**qubits)
        amplitude = np.zeros(2**qubits, dtype=np.complex_)
        for samples in result:
            probability[samples.state.lsb_int] = samples.probability
            amplitude[samples.state.lsb_int] = samples.amplitude

        pdf = pd.DataFrame(
            {
                "States": states,
                "Int_lsb": list_int_lsb,
                "Probability": probability,
                "Amplitude": amplitude,
                "Int": list_int,
            }
        )
    else:
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

def init_state(alpha):
    """
    Initialize qubit state
    """
    tree = KPTree(np.array([np.sqrt(1.0 - alpha), np.sqrt(alpha)])).get_routine()
    return tree


def _matrix_gen(inaccuracy):
    """
    Matrix M for M gate
    """
    theta = inaccuracy * np.pi / 2
    return np.array([
        [np.cos(theta), np.sin(theta)],
        [np.sin(theta), -np.cos(theta)]
    ])
m_gate = qlm.AbstractGate("M", [float], arity=1, matrix_generator=_matrix_gen)

@qlm.build_gate("Precision", [float], arity=1)
def precision_gate(precision):
    """
    Implication Gate in QLM Abstract Gate
    """
    routine = qlm.QRoutine()
    register = routine.new_wires(1)
    routine.apply(m_gate(precision), register[0])
    return routine

@qlm.build_gate("Rule", [float], arity=3)
def rule_gate(certainty):
    """
    Implication Gate in QLM Abstract Gate
    """

    routine = qlm.QRoutine()
    register = routine.new_wires(3)
    routine.apply(m_gate(certainty), register[1])
    routine.apply(qlm.CCNOT, register[0], register[1], register[2])
    return routine

@qlm.build_gate("Not", [], arity=2)
def not_gate():
    """
    Not Gate
    """
    routine = qlm.QRoutine()
    register = routine.new_wires(2)
    routine.apply(qlm.CNOT, register[0], register[1])
    routine.apply(qlm.X, register[1])
    return routine

@qlm.build_gate("And", [], arity=3)
def and_gate():
    """
    AND gate
    """
    routine = qlm.QRoutine()
    register = routine.new_wires(3)
    routine.apply(qlm.CCNOT, register[0], register[1], register[2])
    return routine

@qlm.build_gate("Or", [], arity=3)
def or_gate():
    """
    OR gate
    """
    routine = qlm.QRoutine()
    register = routine.new_wires(3)
    routine.apply(qlm.CCNOT, register[0], register[1], register[2])
    routine.apply(qlm.CNOT, register[0], register[2])
    routine.apply(qlm.CNOT, register[1], register[2])
    return routine


