import numpy as np
import functools as ft

zero_ket = np.array([1, 0])
one_ket = np.array([0, 1])

def m_operator(inaccuracy):
    """
    Matrix M for indetermination using CF
    """
    theta = inaccuracy * np.pi / 2
    return np.array([
        [np.cos(theta), np.sin(theta)],
        [np.sin(theta), -np.cos(theta)]
    ])

def pauli_operators(pauli_index):
    """
    Return the correspondent Pauli matrix.

    Parameters
    ----------

    pauli_index : int
        Number for selecting the Pauli matrix:
        0 -> identity, 1-> X, 2-> Y, 3 -> Z

    Returns
    -------

    pauli = np.array
        2x2 Pauli Matrix

    """
    if pauli_index == 0:
        pauli = np.identity(2, dtype=np.complex128)
    elif pauli_index == 1:
        pauli = np.array([[0, 1], [1, 0]])
    elif pauli_index == 2:
        pauli = np.array([[0, -1j], [1j, 0]])
    elif pauli_index == 3:
        pauli = np.array([[1, 0], [0, -1]])
    return pauli

def toffoli():
    """
    Toffoli gate. In CF this the AND gate
    """
    toffoli_ = np.identity(8)
    toffoli_[6,6] = 0.0
    toffoli_[7,7] = 0.0
    toffoli_[6,7] = 1.0
    toffoli_[7,6] = 1.0
    return toffoli_

def cnot_gate(nqubits, control, target):
    lista0 = []
    lista1 = []
    for i in range(nqubits):
        if i == control:
            lista0.append(np.outer(zero_ket, zero_ket))
            lista1.append(np.outer(one_ket, one_ket))
        elif i == target:
            lista0.append(pauli_operators(0))
            lista1.append(pauli_operators(1))
        else:
            lista1.append(pauli_operators(0))
            lista0.append(pauli_operators(0))
    return ft.reduce(np.kron, lista0) + ft.reduce(np.kron, lista1)

def not_gate():
    """
    Not gate in CF
    """
    return np.kron(pauli_operators(0), pauli_operators(1)) @ cnot_gate(2, 0, 1)

def or_gate():
    toff_ =  toffoli()
    first_cnot = cnot_gate(3, 0, 2)
    second_cnot = cnot_gate(3, 1, 2)

    return  second_cnot @ first_cnot  @ toff_


def state(lista):
    """
    Given a list it creates the corresponding state vector
    """
    zero_ket = np.array([1, 0])
    one_ket = np.array([0, 1])
    ket = []
    for i in lista:
        if i == 0:
            ket.append(zero_ket)
        elif i == 1:
            ket.append(one_ket)
        else:
            raise ValueError("Only can be 0 o0r 1")
    return ft.reduce(np.kron, ket)

def implication(certainty):
    """
    Matrix for implication operator
    """
    before = ft.reduce(
        np.kron,
        [pauli_operators(0), m_operator(certainty), pauli_operators(0)]
    )

    return toffoli() @ before

if __name__ == "__main__":

    print("Test NOT gate")
    print(not_gate() @ state([0, 0]) == state([0, 1]))
    print(not_gate() @ state([1, 0]) == state([1, 0]))
    print("Test AND gate")
    print(toffoli() @ state([0, 0, 0]) == state([0, 0, 0]))
    print(toffoli() @ state([1, 0, 0]) == state([1, 0, 0]))
    print(toffoli() @ state([0, 1, 0]) == state([0, 1, 0]))
    print(toffoli() @ state([1, 1, 0]) == state([1, 1, 1]))
    print("Test OR gate")
    print(or_gate() @ state([0, 0, 0]) == state([0, 0, 0]))
    print(or_gate() @ state([1, 0, 0]) == state([1, 0, 1]))
    print(or_gate() @ state([0, 1, 0]) == state([0, 1, 1]))
    print(or_gate() @ state([1, 1, 0]) == state([1, 1, 1]))
    print("Implcation Gate")
    print(implication(1.0) @ state([1, 0, 1]))





