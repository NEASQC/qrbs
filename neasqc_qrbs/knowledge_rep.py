# -*- coding : utf-8 -*

from abc import ABC, abstractmethod
from qat.lang.AQASM.routines import QRoutine


class Buildable(ABC):
    """Interface for knowledge elements that can be built into quantum circuits.
    """

    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def build(self) -> QRoutine:
        pass


class LeftHandSide(Buildable):
    """Interface for elements that can be part of the left hand side of a rule. This class is used to model the Composite design pattern, acting as the Component interface.
    """

    def __init__(self) -> None:
        super().__init__()
    
    def build(self) -> QRoutine:
        return super().build()


class Fact(LeftHandSide):
    """Class representing a Fact. 
    
    A Fact is the smallest unit of knowledge that can be represented. This class is used to model the Composite design pattern, acting as the Leaf class.

    Attributes:
        attribute (str): Attribute that the fact is representing.
        value (float): Value of the attribute that the fact is representing.
        imprecission (float, optional): Imprecission of the fact; the certainty of the attribute having said value (0 if not specified).
    """

    def __init__(self, attribute, value, imprecission=0.0) -> None:
        super().__init__()
        self.attribute = attribute
        self.value = value
        self.imprecission = imprecission

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.attribute == other.attribute and self.value == other.value and self.imprecission == other.imprecission

    def build(self) -> QRoutine:
        return super().build()
        

class AndOperator(LeftHandSide):
    """Class representing an AndOperator.
    
    An AndOperator relates the statements of its children with an AND relationship. This class is used to model the Composite design pattern, acting as (one of) the Composite class.

    Attributes:
        leftChild (:obj:`LeftHandSide`): One of the children which is relating.
        rightChild (:obj:`LeftHandSide`): One of the children which is relating.
    """

    def __init__(self, leftChild, rightChild) -> None:
        super().__init__()
        self.leftChild = leftChild
        self.rightChild = rightChild

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.leftChild == other.leftChild and self.rightChild == other.rightChild

    def build(self) -> QRoutine:
        return super().build()
        

class OrOperator(LeftHandSide):
    """Class representing an OrOperator.
    
    An OrOperator relates the statements of its children with an OR relationship. This class is used to model the Composite design pattern, acting as (one of) the Composite class.

    Attributes:
        leftChild (:obj:`LeftHandSide`): One of the children which is relating.
        rightChild (:obj:`LeftHandSide`): One of the children which is relating.
    """

    def __init__(self, leftChild, rightChild) -> None:
        super().__init__()
        self.leftChild = leftChild
        self.rightChild = rightChild

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.leftChild == other.leftChild and self.rightChild == other.rightChild

    def build(self) -> QRoutine:
        return super().build()

        

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

    def build(self) -> QRoutine:
        return super().build()
        

class Rule(Buildable):
    """Class representing a Rule.
    
    A Rule which establishes a relationship (to some level of uncertainty) between a left hand side element and a right hand side, which in this context is a Fact.

    Attributes:
        leftHandSide (:obj:`LeftHandSide`): Left hand side element of the rule (also known as precedent).
        rightHandSide (:obj:`Fact`): Right hand side element of the rule (also known as consecuent).
        uncertainty (float, optional): Uncertainty of the relationship between precedent and consecuent (0 if not specified).
    """

    def __init__(self, lefthandside, righthandside, uncertainty=0.0) -> None:
        super().__init__()
        self.lefthandside = lefthandside
        self.righthandside = righthandside
        self.uncertainty = uncertainty

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.lefthandside == other.lefthandside and self.righthandside == other.righthandside and self.uncertainty == other.uncertainty

    def build(self) -> QRoutine:
        return super().build()
        

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

    def build(self) -> QRoutine:
        return super().build()