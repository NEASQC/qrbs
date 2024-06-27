"""
Reverse inferential circuits
"""
import numpy as np
import functools as ft
from gates import *


def funcion(certainty, alpha):
    """
    Contruyo Implicacion. Fijo precision del hecho antecedente
    Quiero saber la precision de salida (dar output_precision =0)
    """
    # El primer qubit es una combinacion lineal
    #first_qubit = np.sqrt(alpha) * state([0]) + np.sqrt(1-alpha) * state([1])
    first_qubit = m_operator(alpha) @ state([0])
    input_vector = ft.reduce(np.kron,[first_qubit, state([0]), state([0])])
    input_vector = implication(certainty) @ input_vector
    list_finals = []
    for state_ in [[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]]:
        list_finals.append(np.real(state(state_).T @ input_vector) **2)
    return np.sum(list_finals)
x = 0.8
print(funcion(x, 0.8))

def loss(x, alpha, output_precision):
    return abs(funcion(x[0], alpha) - output_precision)

# from scipy.optimize import minimize
# 
# x0 = [0.5] #, 0.5]
# bnds = ((0, None))
# res = minimize(loss, [0.5], args = (0.7, 0.6))
# print(res)
