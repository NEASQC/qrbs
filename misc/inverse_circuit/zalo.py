"""
Reverse inferential circuits
"""
import numpy as np
import functools as ft
from gates import *


def solve_implication(certainty, alpha):
    """
    Implication quantum circuit
    
    Parameters
    ----------

    certainty : float
        float with rule certainty's
    alpha : float
        value of the |0> coefficient

    """
    # El primer qubit es una combinacion lineal

    first_qubit = alpha * state([0]) + np.sqrt(1-alpha) * state([1])
    #first_qubit = m_operator(alpha) @ state([0])
    input_vector = ft.reduce(np.kron,[first_qubit, state([0]), state([0])])
    input_vector = implication(certainty) @ input_vector
    list_finals = []
    for state_ in [[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]]:
        list_finals.append(np.real(state(state_).T @ input_vector) **2)
    return np.sum(list_finals)

def solve_not(alpha):
    """
    Not quantum circuit
    
    Parameters
    ----------

    alpha : float
        value of the |0> coefficient

    """
    first_qubit = alpha * state([0]) + np.sqrt(1-alpha) * state([1])
    input_vector = ft.reduce(np.kron,[first_qubit, state([0])])
    input_vector = not_gate() @ input_vector
    list_finals = []
    for state_ in [[0, 1], [1, 1]]:
        list_finals.append(np.real(state(state_).T @ input_vector) **2)
    return np.sum(list_finals)

def solve_and(alpha):
    first_qubit = alpha * state([0]) + np.sqrt(1-alpha) * state([1])
    input_vector = ft.reduce(np.kron,[first_qubit, state([0])])
    input_vector = toffoli() @ input_vector
    list_finals = []
    for state_ in [[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]]:
        list_finals.append(np.real(state(state_).T @ input_vector) **2)
    return np.sum(list_finals)




