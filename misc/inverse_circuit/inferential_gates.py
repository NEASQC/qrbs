
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from random import random
import qat.lang.AQASM as qlm
from qat.qpus import CLinalg
from gates_qlm import *



class InferentialGate:
    """
    This gate has 2 input 1-qubit states |a> and |b> and we want a
    1-qubit state |c>. All the 1 qubit state will be of the same form:
    |i> = (1.0 - alpha_i) ** 0.5 |0> + alpha_i ** 0.5 |1>
    For defining the states c_i is needed.
    """

    def __init__(self, qpu, alpha_c):

        # Coefficient of the |1> component of the |a> state
        self.alpha_a = None
        # Coefficient of the |1> component of the |b> state
        self.alpha_b = None
        # Coefficient of the |1> component of the |c> state
        self.alpha_c = alpha_c
        # Inputs
        self.qpu = qpu

        # Initial guess for minimization
        self.guess_ = None
        self.job = None
        self.loss_ = None
        self.gate = None

        self.factor = 0.2

    def fit(self):
        self.guess()
        self.minimize()

    def guess(self):
        """
        Method for initializing guess variables for minimization
        """
        pass

    def minimize(self):
        """
        Method for optimize the circuit gate
        """
        pass

    def loss(self, guess, output):
        """
        Method for computing the loss
        """
        pass

    def circuit(self, alpha, beta):
        """
        Method for building the corresponding quantum circuit
        """
        pass


class AND(InferentialGate):

    def guess(self):
        """
        Method for initializing guess variables for minimization
        """
        self.alpha_a = random()
        self.alpha_b = random()
        condition = min(self.alpha_a, self.alpha_b)
        lower_limit = (1.0 - self.factor) * self.alpha_c
        higher_limit = (1.0 + self.factor) * self.alpha_c
        while (condition < lower_limit) or (condition > higher_limit):
            self.alpha_a = random()
            self.alpha_b = random()
            condition = min(self.alpha_a, self.alpha_b)

        # Inital guess for optimization
        self.guess_ = np.array([self.alpha_a, self.alpha_b])
    def circuit(self, alpha, beta):
        """
        Method for building the corresponding quantum circuit
        """
        routine = qlm.QRoutine()
        gate = and_gate()
        register = routine.new_wires(gate.arity)
        routine.apply(init_state(alpha), register[0])
        routine.apply(init_state(beta), register[1])
        routine.apply(gate, register)
        self.job = routine.to_circ().to_job(
            nbshots=0,
            qubits=[gate.arity - 1]
        )
    def loss(self, guess, output):
        """
        Method for computing the loss
        """
        alpha = guess[0]
        beta = guess[1]
        self.circuit(alpha, beta)
        pdf = solve_qjob(self.job, self.qpu)
        loss_ = (pdf[pdf["Int"] == 1]["Probability"] - output) ** 2
        return loss_
    def minimize(self):
        """
        Method for optimize the circuit gate
        """
        bnds = ((0.0, 1.0) for i in self.guess_)
        res = minimize(
            self.loss,
            self.guess_,
            args=self.alpha_c,
            bounds=bnds
        )
        self.alpha_a = res.x[0]
        self.alpha_b = res.x[1]


class OR(InferentialGate):

    def guess(self):
        """
        Method for initializing guess variables for minimization
        """
        self.alpha_a = random()
        self.alpha_b = random()
        condition = max(self.alpha_a, self.alpha_b)
        lower_limit = (1.0 - self.factor) * self.alpha_c
        higher_limit = (1.0 + self.factor) * self.alpha_c
        while (condition < lower_limit) or (condition > higher_limit):
            self.alpha_a = random()
            self.alpha_b = random()
            condition = max(self.alpha_a, self.alpha_b)

        # Inital guess for optimization
        self.guess_ = np.array([self.alpha_a, self.alpha_b])


    def circuit(self, alpha, beta):
        """
        Method for building the corresponding quantum circuit
        """
        routine = qlm.QRoutine()
        gate = or_gate()
        register = routine.new_wires(gate.arity)
        routine.apply(init_state(alpha), register[0])
        routine.apply(init_state(beta), register[1])
        routine.apply(gate, register)
        self.job = routine.to_circ().to_job(
            nbshots=0,
            qubits=[gate.arity - 1]
        )
    def loss(self, guess, output):
        """
        Method for computing the loss
        """
        alpha = guess[0]
        beta = guess[1]
        self.circuit(alpha, beta)
        pdf = solve_qjob(self.job, self.qpu)
        loss_ = (pdf[pdf["Int"] == 1]["Probability"] - output) ** 2
        return loss_
    def minimize(self):
        """
        Method for optimize the circuit gate
        """
        bnds = ((0.0, 1.0) for i in self.guess_)
        res = minimize(
            self.loss,
            self.guess_,
            args=self.alpha_c,
            bounds=bnds
        )
        self.alpha_a = res.x[0]
        self.alpha_b = res.x[1]

class NOT(InferentialGate):

    def guess(self):
        """
        Method for initializing guess variables for minimization
        """
        self.alpha_a = 1.0 - self.alpha_c
        # Inital guess for optimization
        self.guess_ = np.array([self.alpha_a])


    def circuit(self, alpha, beta=None):
        """
        Method for building the corresponding quantum circuit
        """
        routine = qlm.QRoutine()
        gate = not_gate()
        register = routine.new_wires(gate.arity)
        routine.apply(init_state(alpha), register[0])
        routine.apply(gate, register)
        self.job = routine.to_circ().to_job(
            nbshots=0,
            qubits=[gate.arity - 1]
        )
    def loss(self, guess, output):
        """
        Method for computing the loss
        """
        alpha = guess[0]
        self.circuit(alpha)
        pdf = solve_qjob(self.job, self.qpu)
        loss_ = (pdf[pdf["Int"] == 1]["Probability"] - output) ** 2
        return loss_
    def minimize(self):
        """
        Method for optimize the circuit gate
        """
        bnds = ((0.0, 1.0) for i in self.guess_)
        res = minimize(
            self.loss,
            self.guess_,
            args=self.alpha_c,
            bounds=bnds
        )
        self.alpha_a = res.x[0]

class PRECISION(InferentialGate):
    def guess(self):
        """
        Method for initializing guess variables for minimization
        """
        self.guess_ = np.array([self.alpha_c])

    def circuit(self, alpha):
        """
        Method for building the corresponding quantum circuit
        """
        routine = qlm.QRoutine()
        gate = precision_gate(alpha)
        register = routine.new_wires(gate.arity)
        routine.apply(gate, register)
        self.job = routine.to_circ().to_job(
            nbshots=0,
            qubits=[gate.arity - 1]
        )
    def loss(self, guess, output):
        """
        Method for computing the loss
        """
        alpha = guess[0]
        self.circuit(alpha)
        pdf = solve_qjob(self.job, self.qpu)
        loss_ = (pdf[pdf["Int"] == 1]["Probability"] - output) ** 2
        return loss_

    def minimize(self):
        """
        Method for optimize the circuit gate
        """
        bnds = ((0.0, 1.0) for i in self.guess_)
        res = minimize(
            self.loss,
            self.guess_,
            args=self.alpha_c,
            bounds=bnds
        )
        self.alpha_a = res.x[0]


class RULE(InferentialGate):
    def guess(self):
        """
        Method for initializing guess variables for minimization
        """
        self.alpha_b = random()
        self.alpha_a = self.alpha_c / self.alpha_b
        while self.alpha_a >= 1.0:
            self.alpha_b = random()
            self.alpha_a = self.alpha_c / self.alpha_b

        # Inital guess for optimization
        self.guess_ = np.array([self.alpha_a, self.alpha_b])

    def circuit(self, alpha, beta):
        """
        Method for building the corresponding quantum circuit
        """
        routine = qlm.QRoutine()
        gate = rule_gate(beta)
        register = routine.new_wires(gate.arity)
        routine.apply(init_state(alpha), register[0])
        routine.apply(gate, register)
        self.job = routine.to_circ().to_job(
            nbshots=0,
            qubits=[gate.arity - 1]
        )
    def loss(self, guess, output):
        """
        Method for computing the loss
        """
        alpha = guess[0]
        beta = guess[1]
        self.circuit(alpha, beta)
        pdf = solve_qjob(self.job, self.qpu)
        loss_ = (pdf[pdf["Int"] == 1]["Probability"] - output) ** 2
        return loss_

    def minimize(self):
        """
        Method for optimize the circuit gate
        """
        bnds = ((0.0, 1.0) for i in self.guess_)
        res = minimize(
            self.loss,
            self.guess_,
            args=self.alpha_c,
            bounds=bnds
        )
        self.alpha_a = res.x[0]
        self.alpha_b = res.x[1]


if __name__ == "__main__":
    from qat.core.console import display
    #opa = PRECISION(CLinalg(), 0.4)
    opa = RULE(CLinalg(), 0.6)

    #opa.guess()
    #print(opa.guess_)
    #opa.circuit(0.2, 0.6)
    #c = opa.job.circuit
    #display(c)
    opa.fit()
    print("alpha_a: {}. alpha_b: {}. alpha_c: {}".format(
        opa.alpha_a, opa.alpha_b, opa.alpha_c))


