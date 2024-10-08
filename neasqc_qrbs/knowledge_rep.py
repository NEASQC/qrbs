# -*- coding : utf-8 -*

from abc import ABC, abstractmethod
from typing import Dict, Tuple
import numpy as np
from qat.lang.AQASM import QRoutine, CNOT, CCNOT, X, AbstractGate, RY


class Buildable(ABC):  # pragma: no cover
    """Interface for knowledge elements that can be built into quantum routines.
    """

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def build(self, builder) -> QRoutine:
        pass


class LeftHandSide(Buildable):  # pragma: no cover
    """Interface for elements that can be part of the left hand side of a rule. This class is used to model the Composite design pattern, acting as the Component interface.
    """

    def __init__(self) -> None:
        super().__init__()

    def build(self, builder) -> QRoutine:
        pass


class Fact(LeftHandSide):
    """Class representing a Fact. 
    
    A Fact is the smallest unit of knowledge that can be represented. This class is used to model the Composite design pattern, acting as the Leaf class.

    Attributes:
        attribute (str): Attribute that the fact is representing.
        value (float): Value of the attribute that the fact is representing.
        precision (float, optional): Precision of the fact; the certainty of the attribute having said value (0 if not specified). Must be in range [0,1].
    """

    def __init__(self, attribute, value, precision=0.0) -> None:
        super().__init__()
        self.attribute = attribute
        self.value = value
        self.precision = precision

    @property
    def precision(self):
        return self._precision

    @precision.setter
    def precision(self, precision):
        if 0.0 <= precision <= 1.0:
            self._precision = precision
        else:
            raise ValueError('Precision must be in range [0,1]')

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.attribute == other.attribute and self.value == other.value and self.precision == other.precision

    def __contains__(self, other) -> bool:
        return self.__eq__(other)

    def __str__(self) -> str:
        return 'Fact(' + str(self.attribute) + ', ' + str(self.value) + ', ' + str(self.precision) + ')'

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __iter__(self):
        yield self

    def build(self, builder) -> QRoutine:
        return builder.build_fact(self)


class AndOperator(LeftHandSide):
    """Class representing an AndOperator.
    
    An AndOperator relates the statements of its children with an AND relationship. This class is used to model the Composite design pattern, acting as (one of) the Composite class.

    Attributes:
        left_child (:obj:`LeftHandSide`): One of the children which is relating.
        right_child (:obj:`LeftHandSide`): One of the children which is relating.
    """

    def __init__(self, left_child, right_child) -> None:
        super().__init__()
        self.left_child = left_child
        self.right_child = right_child

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.left_child == other.left_child and self.right_child == other.right_child

    def __contains__(self, child) -> bool:
        return child == self.left_child or child == self.right_child or child in self.left_child or child in self.right_child

    def __str__(self) -> str:
        return 'AndOperator(\n' + '\t' + str(self.left_child) + ',\n' + '\t' + str(self.right_child) + '\n' + ')'

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __iter__(self):
        yield from self.left_child
        yield from self.right_child

    def build(self, builder) -> QRoutine:
        return builder.build_and()


class OrOperator(LeftHandSide):
    """Class representing an OrOperator.
    
    An OrOperator relates the statements of its children with an OR relationship. This class is used to model the Composite design pattern, acting as (one of) the Composite class.

    Attributes:
        left_child (:obj:`LeftHandSide`): One of the children which is relating.
        right_child (:obj:`LeftHandSide`): One of the children which is relating.
    """

    def __init__(self, left_child, right_child) -> None:
        super().__init__()
        self.left_child = left_child
        self.right_child = right_child

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.left_child == other.left_child and self.right_child == other.right_child

    def __contains__(self, child) -> bool:
        return child == self.left_child or child == self.right_child or child in self.left_child or child in self.right_child

    def __str__(self) -> str:
        return 'OrOperator(\n' + '\t' + str(self.left_child) + ',\n' + '\t' + str(self.right_child) + '\n' + ')'

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __iter__(self):
        yield from self.left_child
        yield from self.right_child

    def build(self, builder) -> QRoutine:
        return builder.build_or()


class NotOperator(LeftHandSide):
    """Class representing a NotOperator.
    
    A NotOperator negates the statement of its child. This class is used to model the Composite design pattern, acting as (one of) the Composite class.

    Attributes:
        child (:obj:`LeftHandSide`): Child which statement is negating.
    """

    def __init__(self, child) -> None:
        super().__init__()
        self.child = child

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.child == other.child

    def __contains__(self, child) -> bool:
        return child == self.child or child in self.child

    def __str__(self) -> str:
        return 'NotOperator(\n' + '\t' + str(self.child) + '\n)'

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __iter__(self):
        yield from self.child

    def build(self, builder) -> QRoutine:
        return builder.build_not()


class Rule(Buildable):
    """Class representing a Rule.
    
    A Rule which establishes a relationship (to some level of uncertainty) between a left hand side element and a right hand side, which in this context is a Fact.

    Attributes:
        left_hand_side (:obj:`LeftHandSide`): Left hand side element of the rule (also known as precedent).
        right_hand_side (:obj:`Fact`): Right hand side element of the rule (also known as consequent).
        certainty (float, optional): Certainty of the relationship between precedent and consequent (0 if not specified). Must be in range [0,1].
    """

    def __init__(self, left_hand_side, right_hand_side, certainty=0.0) -> None:
        super().__init__()
        self.left_hand_side = left_hand_side
        self.right_hand_side = right_hand_side
        self.certainty = certainty

    @property
    def certainty(self):
        return self._certainty

    @certainty.setter
    def certainty(self, certainty):
        if 0.0 <= certainty <= 1.0:
            self._certainty = certainty
        else:
            raise ValueError('Certainty must be in range [0,1]')

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.left_hand_side == other.left_hand_side and self.right_hand_side == other.right_hand_side and self.certainty == other.certainty

    def __lt__(self, other) -> bool:
        return self.right_hand_side in other.left_hand_side

    def __str__(self) -> str:
        return 'Rule(\n' + '\t' + str(self.left_hand_side) + ',\n' + '\t' + str(self.right_hand_side) + ',\n' + '\t' + str(
            self.certainty) + '\n' + ')'

    def build(self, builder) -> QRoutine:
        return builder.build_rule(self)


class KnowledgeIsland(Buildable):
    """Class representing a Knowledge Island.
    
    A Knowledge Island is a set of rules that conform the inferential reasoning towards a hypothesis.

    Attributes:
        rules (List[:obj:`Rule`]): Set of rules that conform the knowledge island.
    """

    def __init__(self, rules) -> None:
        super().__init__()
        self.rules = rules

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.rules == other.rules

    def __str__(self) -> str:
        return 'KnowledgeIsland(\n' + ''.join(f'\t{rule},\n' for rule in self.rules) + ')'

    def build(self, builder) -> QRoutine:
        routine, _ = builder.build_island(self)
        return routine


class Builder(ABC):  # pragma: no cover
    """Interface for building the corresponding quantum routine from a Buildable element.
    """

    @staticmethod
    @abstractmethod
    def build_fact(fact) -> QRoutine:
        """Builds the quantum routine of a fact.

        Args:
            fact (:obj:`Fact`): The Fact whose quantum routine is being built. 
        
        Returns:
            :obj:`QRoutine`: The corresponding quantum routine.
        """
        pass

    @staticmethod
    @abstractmethod
    def build_and() -> QRoutine:
        """Builds the quantum routine of an and operator.
        
        Returns:
            :obj:`QRoutine`: The corresponding quantum routine.
        """
        pass

    @staticmethod
    @abstractmethod
    def build_or() -> QRoutine:
        """Builds the quantum routine of an or operator.
        
        Returns:
            :obj:`QRoutine`: The corresponding quantum routine.
        """
        pass

    @staticmethod
    @abstractmethod
    def build_not() -> QRoutine:
        """Builds the quantum routine of a not operator.
        
        Returns:
            :obj:`QRoutine`: The corresponding quantum routine.
        """
        pass

    @staticmethod
    @abstractmethod
    def build_rule(rule) -> QRoutine:
        """Builds the quantum routine of a rule.

        Args:
            rule (:obj:`Rule`): The Rule whose quantum routine is being built. 
        
        Returns:
            :obj:`QRoutine`: The corresponding quantum routine.
        """
        pass

    @staticmethod
    @abstractmethod
    def build_island(island) -> Tuple[QRoutine, Dict[LeftHandSide, int]]:
        """Builds the quantum routine of a knowledge island.

        Args:
            island (:obj:`KnowledgeIsland`): The KnowledgeIsland whose quantum routine is being built. 
        
        Returns:
            Tuple[:obj:`QRoutine`, Dict[:obj:`LeftHandSide`, int]]: A tuple containing the corresponding quantum routine and the index of which qubit corresponds to each LeftHandSide element.
        """
        pass


class BuilderImpl(Builder):
    """Implementation of Builder interface.
    """

    def _matrix_gen(inaccuracy):
        theta = inaccuracy * np.pi / 2
        return np.array([
            [np.cos(theta), np.sin(theta)],
            [np.sin(theta), -np.cos(theta)]
        ])

    M = AbstractGate("M", [float], arity=1, matrix_generator=_matrix_gen)

    @staticmethod
    def build_fact(fact) -> QRoutine:
        """Builds the quantum routine of a fact.

        Args:
            fact (:obj:`Fact`): The Fact whose quantum routine is being built. 
        
        Returns:
            :obj:`QRoutine`: The corresponding quantum routine.
        """

        routine = QRoutine()
        routine.apply(BuilderImpl.M(fact.precision), 0)
        return routine

    @staticmethod
    def build_and() -> QRoutine:
        """Builds the quantum routine of an and operator.
        
        Returns:
            :obj:`QRoutine`: The corresponding quantum routine.
        """
        routine = QRoutine()
        routine.apply(CCNOT, 0, 1, 2)
        return routine

    @staticmethod
    def build_or() -> QRoutine:
        """Builds the quantum routine of an or operator.
        
        Returns:
            :obj:`QRoutine`: The corresponding quantum routine.
        """
        routine = QRoutine()
        routine.apply(CCNOT, 0, 1, 2)
        routine.apply(CNOT, 0, 2)
        routine.apply(CNOT, 1, 2)
        return routine

    @staticmethod
    def build_not() -> QRoutine:
        """Builds the quantum routine of a not operator.
        
        Returns:
            :obj:`QRoutine`: The corresponding quantum routine.
        """
        routine = QRoutine()
        routine.apply(CNOT, 0, 1)
        routine.apply(X, 1)
        return routine

    @staticmethod
    def build_rule(rule) -> QRoutine:
        """Builds the quantum routine of a rule.

        Args:
            rule (:obj:`Rule`): The Rule whose quantum routine is being built. 
        
        Returns:
            :obj:`QRoutine`: The corresponding quantum routine.
        """
        routine, _ = BuilderImpl.build_island(KnowledgeIsland([rule]))
        return routine

    @staticmethod
    def build_island(island) -> Tuple[QRoutine, Dict[LeftHandSide, int]]:
        """Builds the quantum routine of a knowledge island.

        Args:
            island (:obj:`KnowledgeIsland`): The KnowledgeIsland whose quantum routine is being built. 
        
        Returns:
            Tuple[:obj:`QRoutine`, Dict[:obj:`LeftHandSide`, int]]: A tuple containing the corresponding quantum routine and the index of which qubit corresponds to each LeftHandSide element.
        """

        def build_precedent_routine(precedent, routine, elements):
            if isinstance(precedent, Fact):
                return
            else:
                qbits = []
                if isinstance(precedent, NotOperator):
                    if precedent.child not in elements:
                        build_precedent_routine(precedent.child, routine, elements)
                    qbits.extend([elements[precedent.child]])
                else:  # isinstance(precedent, AndOperator or OrOperator)
                    if precedent.left_child not in elements:
                        build_precedent_routine(precedent.left_child, routine, elements)
                    if precedent.right_child not in elements:
                        build_precedent_routine(precedent.right_child, routine, elements)
                    qbits.extend([elements[precedent.left_child], elements[precedent.right_child]])
                qbits.extend([routine.new_wires(1)])
                routine.apply(precedent.build(BuilderImpl), qbits)
                elements[precedent] = routine.max_wire

        def build_implication_routine(rule, routine, elements):
            routine.new_wires(1)
            routine.apply(BuilderImpl.M(rule.certainty), routine.max_wire)
            routine.apply(CCNOT, elements[rule.left_hand_side], routine.max_wire, elements[rule.right_hand_side])

        rules = island.rules
        rules.sort()
        elements = {}
        routine = QRoutine()
        for rule in rules:
            for fact in rule.left_hand_side:
                if fact not in [rule.right_hand_side for rule in rules] and fact not in elements.keys():
                    routine.new_wires(1)
                    elements[fact] = routine.max_wire
                    routine.apply(fact.build(BuilderImpl), elements[fact])
        for rule in rules:
            routine.new_wires(1)
            elements[rule.right_hand_side] = routine.max_wire
        for rule in rules:
            build_precedent_routine(rule.left_hand_side, routine, elements)
            build_implication_routine(rule, routine, elements)
        return routine, elements


class BuilderFuzzy(Builder):
    """Implementation of Builder interface for the fuzzy logic model.
    """

    @staticmethod
    def build_fact(fact) -> QRoutine:
        """Builds the quantum routine of a fact.

        Args:
            fact (:obj:`Fact`): The Fact whose quantum routine is being built. 
        
        Returns:
            :obj:`QRoutine`: The corresponding quantum routine.
        """

        routine = QRoutine()
        routine.apply(RY(fact.precision * np.pi), 0)
        return routine

    @staticmethod
    def build_and() -> QRoutine:
        """Builds the quantum routine of an and operator.
        
        Returns:
            :obj:`QRoutine`: The corresponding quantum routine.
        """
        routine = QRoutine()
        routine.apply(CCNOT, 0, 1, 2)
        return routine

    @staticmethod
    def build_or() -> QRoutine:
        """Builds the quantum routine of an or operator.
        
        Returns:
            :obj:`QRoutine`: The corresponding quantum routine.
        """
        routine = QRoutine()
        routine.apply(X, 0)
        routine.apply(X, 1)
        routine.apply(CCNOT, 0, 1, 2)
        routine.apply(X, 0)
        routine.apply(X, 1)
        routine.apply(X, 2)
        return routine

    @staticmethod
    def build_not() -> QRoutine:
        """Builds the quantum routine of a not operator.
        
        Returns:
            :obj:`QRoutine`: The corresponding quantum routine.
        """
        routine = QRoutine()
        routine.apply(CNOT, 0, 1)
        routine.apply(X, 1)
        return routine

    @staticmethod
    def build_rule(rule) -> QRoutine:
        """Builds the quantum routine of a rule.

        Args:
            rule (:obj:`Rule`): The Rule whose quantum routine is being built. 
        
        Returns:
            :obj:`QRoutine`: The corresponding quantum routine.
        """
        routine, _ = BuilderFuzzy.build_island(KnowledgeIsland([rule]))
        return routine

    @staticmethod
    def build_island(island) -> Tuple[QRoutine, Dict[LeftHandSide, int]]:
        """Builds the quantum routine of a knowledge island.

        Args:
            island (:obj:`KnowledgeIsland`): The KnowledgeIsland whose quantum routine is being built. 
        
        Returns:
            Tuple[:obj:`QRoutine`, Dict[:obj:`LeftHandSide`, int]]: A tuple containing the corresponding quantum routine and the index of which qubit corresponds to each LeftHandSide element.
        """

        def build_precedent_routine(precedent, routine, elements):
            if isinstance(precedent, Fact):
                return
            else:
                qbits = []
                if isinstance(precedent, NotOperator):
                    if precedent.child not in elements:
                        build_precedent_routine(precedent.child, routine, elements)
                    qbits.extend([elements[precedent.child]])
                else:  # isinstance(precedent, AndOperator or OrOperator)
                    if precedent.left_child not in elements:
                        build_precedent_routine(precedent.left_child, routine, elements)
                    if precedent.right_child not in elements:
                        build_precedent_routine(precedent.right_child, routine, elements)
                    qbits.extend([elements[precedent.left_child], elements[precedent.right_child]])
                qbits.extend([routine.new_wires(1)])
                routine.apply(precedent.build(BuilderFuzzy), qbits)
                elements[precedent] = routine.max_wire

        def build_implication_routine(rule, routine, elements):
            routine.new_wires(1)
            routine.apply(RY(rule.certainty * np.pi), routine.max_wire)
            routine.apply(CCNOT, elements[rule.left_hand_side], routine.max_wire, elements[rule.right_hand_side])

        rules = island.rules
        rules.sort()
        elements = {}
        routine = QRoutine()
        for rule in rules:
            for fact in rule.left_hand_side:
                if fact not in [rule.right_hand_side for rule in rules] and fact not in elements.keys():
                    routine.new_wires(1)
                    elements[fact] = routine.max_wire
                    routine.apply(fact.build(BuilderFuzzy), elements[fact])
        for rule in rules:
            routine.new_wires(1)
            elements[rule.right_hand_side] = routine.max_wire
        for rule in rules:
            build_precedent_routine(rule.left_hand_side, routine, elements)
            build_implication_routine(rule, routine, elements)
        return routine, elements


class BuilderBayes(Builder):
    """Implementation of Builder interface for the bayesian model.
    """

    def _matrix_gen(inaccuracy):
        theta = (inaccuracy * np.pi) / 2
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, np.cos(theta), -np.sin(theta)],
            [0, 0, np.sin(theta), np.cos(theta)]
        ])

    CRY = AbstractGate("CRY", [float], arity=2, matrix_generator=_matrix_gen)

    @staticmethod
    def build_fact(fact) -> QRoutine:
        """Builds the quantum routine of a fact.

        Args:
            fact (:obj:`Fact`): The Fact whose quantum routine is being built. 
        
        Returns:
            :obj:`QRoutine`: The corresponding quantum routine.
        """

        routine = QRoutine()
        routine.apply(RY(fact.precision * np.pi), 0)
        return routine

    @staticmethod
    def build_and() -> QRoutine:
        """Builds the quantum routine of an and operator.
        
        Returns:
            :obj:`QRoutine`: The corresponding quantum routine.
        """
        routine = QRoutine()
        routine.apply(CCNOT, 0, 1, 2)
        return routine

    @staticmethod
    def build_or() -> QRoutine:
        """Builds the quantum routine of an or operator.
        
        Returns:
            :obj:`QRoutine`: The corresponding quantum routine.
        """
        routine = QRoutine()
        routine.apply(X, 0)
        routine.apply(CCNOT, 0, 1, 2)
        routine.apply(X, 0)
        routine.apply(X, 1)
        routine.apply(CCNOT, 0, 1, 2)
        routine.apply(X, 1)
        routine.apply(CCNOT, 0, 1, 2)
        return routine

    @staticmethod
    def build_not() -> QRoutine:
        """Builds the quantum routine of a not operator.
        
        Returns:
            :obj:`QRoutine`: The corresponding quantum routine.
        """
        routine = QRoutine()
        routine.apply(CNOT, 0, 1)
        routine.apply(X, 1)
        return routine

    @staticmethod
    def build_rule(rule) -> QRoutine:
        """Builds the quantum routine of a rule.

        Args:
            rule (:obj:`Rule`): The Rule whose quantum routine is being built. 
        
        Returns:
            :obj:`QRoutine`: The corresponding quantum routine.
        """
        routine, _ = BuilderBayes.build_island(KnowledgeIsland([rule]))
        return routine

    @staticmethod
    def build_island(island) -> Tuple[QRoutine, Dict[LeftHandSide, int]]:
        """Builds the quantum routine of a knowledge island.

        Args:
            island (:obj:`KnowledgeIsland`): The KnowledgeIsland whose quantum routine is being built. 
        
        Returns:
            Tuple[:obj:`QRoutine`, Dict[:obj:`LeftHandSide`, int]]: A tuple containing the corresponding quantum routine and the index of which qubit corresponds to each LeftHandSide element.
        """

        def build_precedent_routine(precedent, routine, elements):
            if isinstance(precedent, Fact):
                return
            else:
                qbits = []
                if isinstance(precedent, NotOperator):
                    if precedent.child not in elements:
                        build_precedent_routine(precedent.child, routine, elements)
                    qbits.extend([elements[precedent.child]])
                else:  # isinstance(precedent, AndOperator or OrOperator)
                    if precedent.left_child not in elements:
                        build_precedent_routine(precedent.left_child, routine, elements)
                    if precedent.right_child not in elements:
                        build_precedent_routine(precedent.right_child, routine, elements)
                    qbits.extend([elements[precedent.left_child], elements[precedent.right_child]])
                qbits.extend([routine.new_wires(1)])
                routine.apply(precedent.build(BuilderBayes), qbits)
                elements[precedent] = routine.max_wire

        def build_implication_routine(rule, routine, elements):
            #routine.apply(BuilderBayes.CRY(rule.certainty), elements[rule.left_hand_side], elements[rule.right_hand_side])
            routine.apply(RY(np.pi * rule.certainty).ctrl(1), elements[rule.left_hand_side], elements[rule.right_hand_side])

        rules = island.rules
        rules.sort()
        elements = {}
        routine = QRoutine()
        for rule in rules:
            for fact in rule.left_hand_side:
                if fact not in [rule.right_hand_side for rule in rules] and fact not in elements.keys():
                    routine.new_wires(1)
                    elements[fact] = routine.max_wire
                    routine.apply(fact.build(BuilderBayes), elements[fact])
        for rule in rules:
            routine.new_wires(1)
            elements[rule.right_hand_side] = routine.max_wire
        for rule in rules:
            build_precedent_routine(rule.left_hand_side, routine, elements)
            build_implication_routine(rule, routine, elements)
        return routine, elements
