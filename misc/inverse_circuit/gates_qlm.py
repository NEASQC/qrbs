"""
Inferential gates in qlm
"""
import numpy as np
import qat.lang.AQASM as qlm

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


def m_gate(inaccuracy):
    def _matrix_gen(inaccuracy):
        """
        Matrix M for M gate
        """
        theta = inaccuracy * np.pi / 2
        return np.array([
            [np.cos(theta), np.sin(theta)],
            [np.sin(theta), -np.cos(theta)]
        ])
    gate_m = qlm.AbstractGate(
        "M", [float], arity=1, matrix_generator=_matrix_gen)
    return gate_m


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


