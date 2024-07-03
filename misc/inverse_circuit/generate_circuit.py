"""
Generate the random  inferential circuit
"""
from inferential_gates import *
from gates_qlm import *
from qat.core.console import display

def quantum_circuit(circuit_list):
    """
    Given a list with the inferential gates build the corresponding
    QLM quantum circuit

    Parameters
    ----------
    circuit_list : list
        List where each element has the complete configuration info
        for building a qlm quantum gate. Each element is a list of three
        elements: first indicates the type of gate. Valid strings are:
        And, Or, Not, Precision, Rule. Other elements configure the
        precision (first elemnt) or the certainty (second element) of the
        Precision and Rule gates
    Return
    ------
    routine : QLM routine
        QLM routine with the complete quantum QLM circuit of the
        inferential circuit
    """

    circuit_list.reverse()
    routine = qlm.QRoutine()
    for step in circuit_list:
        routine = quantum_gate(step, routine)

    return routine

def quantum_gate(step, routine):
    """
    Implements the QLM quantum version of an input inferential gate
    into the final QLM quantum circuit

    Parameters
    ----------
    step : list
        List of three elements that configures the QLM version of the
        inferential gate. First element indicates the type of gate.
        Valid strings are:
        And, Or, Not, Precision, Rule.
        Other elements configure the precision (first elemnt) or the
        certainty (second element) of the Precision and Rule gates
    Return
    ------
    routine : QLM routine
        QLM routine with the complete quantum QLM circuit of the
        inferential circuit
    """

    if step[0] == "Precision":

        routine.new_wires(1)
        routine.apply(precision_gate(step[1]), routine.max_wire)

    if  step[0] == "And":
        routine.new_wires(1)
        routine.apply(
            and_gate(),
            routine.max_wire-2,
            routine.max_wire-1,
            routine.max_wire,
        )
    if  step[0] == "Or":
        routine.new_wires(1)
        routine.apply(
            or_gate(),
            routine.max_wire-2,
            routine.max_wire-1,
            routine.max_wire,
        )
    if  step[0] == "Not":
        routine.new_wires(1)
        routine.apply(
            not_gate(),
            routine.max_wire-1,
            routine.max_wire,
        )
    if step[0] == "Rule":
        routine.new_wires(1)
        routine.new_wires(1)
        routine.apply(
            rule_gate(step[-1]),
            routine.max_wire-2,
            routine.max_wire-1,
            routine.max_wire,
        )

    return routine

def generate_circ(nqubits, precision, qpu):
    """
    Given a number of qubits and a desired precision builds the
    corresponding QLM quantum circuit of a inferential circuit.
    First the different inferential gates are optimized in order
    to get the desired precision and certainties.
    Second build the corresponding QLM qunantum inferential circuit

    Parameters
    ----------
    nqubits : int
        Number of qubits of the final QLM quantum inferential circuit
    precision : float
        Desired precision of the output fact of the inferential circuit
    qpu : QLM qpu
        QLM qpu for solving the circuits
    Return
    ------
    routine : QLM routine
        QLM routine with the complete quantum QLM circuit of the
        inferential circuit
    """
    if isinstance(nqubits, int) != True:
        raise ValueError("nqubits SHOULD BE an integer!")
    if nqubits < 3:
        raise ValueError("nqubits SHOULD BE higher than 3!")
    if (precision >= 1.0) or (precision <= 0.0):
        raise ValueError("precision MUST BE between 0 and 1")

    lista_circuit = [generate_gate("Rule", precision, qpu)]
    nqubits = nqubits - 3
    and_gate_bool = True
    while nqubits >=0:
        # Look for |1> component of the ouput
        # Never can be a Precision Operator
        i = -1
        before = lista_circuit[i]
        # print("before: "+str(before))
        while before[0] == "Precision":
            i = i - 1
            before = lista_circuit[i]
            # print("before: "+str(before))
        output_step = before[1]

        if nqubits >= 2:
            # Add Or, And
            if and_gate_bool:
                before = lista_circuit[-1]
                step = generate_gate("And", output_step, qpu)
                lista_circuit = lista_circuit + [step[0]] + [step[1]]
                and_gate_bool = False
            else:
                step = generate_gate("Or", output_step, qpu)
                lista_circuit = lista_circuit + [step[0]] + [step[1]]
                and_gate_bool = True
            nqubits = nqubits - 2
        elif nqubits == 1:
            lista_circuit = lista_circuit + [generate_gate(
                "Not", output_step, qpu)]
            nqubits = nqubits - 1
        elif nqubits == 0:

            lista_circuit = lista_circuit + [generate_gate(
                "Precision", output_step, qpu)]
            nqubits = nqubits - 1


    q_routine = quantum_circuit(lista_circuit)
    return q_routine


"""
    display(q_routine, max_depth=None)
    job = q_routine.to_circ().to_job(
        nbshots=0,
        qubits=[q_routine.max_wire]
    )
    pdf = solve_qjob(job, qpu)
    print(pdf)
"""


def generate_gate(gate_type, alpha, qpu):

    #print("ADD: {}".format(gate_type))
    if gate_type == "Precision":
        state = PRECISION(qpu, alpha)
        state.fit()
        # print("\t state.alpha_a: {}".format(state.alpha_a))
        # print("\t state.alpha_c: {}".format(state.alpha_c))
        return ["Precision", state.alpha_a, None]

    elif gate_type == "Rule":
        object_rule = RULE(qpu, alpha)
        object_rule.fit()
        # print("\t object_rule.alpha_a : {}".format(object_rule.alpha_a))
        # print("\t object_rule.alpha_b : {}".format(object_rule.alpha_b))
        # print("\t object_rule.alpha_c : {}".format(object_rule.alpha_c))
        return ["Rule", object_rule.alpha_a, object_rule.alpha_b]

    elif gate_type == "Not":
        object_not = NOT(qpu, alpha)
        object_not.fit()
        # print("\t object_not.alpha_a: {}".format(object_not.alpha_a))
        # print("\t object_not.alpha_c: {}".format(object_not.alpha_c))
        return ["Not", object_not.alpha_a, None]

    elif gate_type == "And":
        object_and = AND(qpu, alpha)
        object_and.fit()
        # print("\t object_and.alpha_a : {}".format(object_and.alpha_a))
        # print("\t object_and.alpha_b : {}".format(object_and.alpha_b))
        # print("\t object_and.alpha_c : {}".format(object_and.alpha_c))
        step =["And", object_and.alpha_a, None]
        step = [step] + [generate_gate("Precision", object_and.alpha_b, qpu)]
        return step

    elif gate_type == "Or":
        object_or = OR(qpu, alpha)
        object_or.fit()
        # print("\t object_or.alpha_a : {}".format(object_or.alpha_a))
        # print("\t object_or.alpha_b : {}".format(object_or.alpha_b))
        # print("\t object_or.alpha_c : {}".format(object_or.alpha_c))
        step = ["Or", object_or.alpha_a, None]
        step = [step] + [generate_gate("Precision", object_or.alpha_b, qpu)]
        return step
    else:
        raise ValueError("gate_type MUST BE: Precision, Rule, Not, And, Or")

if __name__ == "__main__":

    generate_circ(30, 0.60)
