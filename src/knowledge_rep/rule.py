# -*- coding : utf-8 -*

from src.knowledge_rep.buildable import Buildable
from qat.lang.AQASM.routines import QRoutine

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


    def build(self) -> QRoutine:
        return super().build()