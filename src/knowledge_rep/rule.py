# -*- coding : utf-8 -*

from src.knowledge_rep.buildable import Buildable
from src.knowledge_rep.lefthandside.lefthandside import LeftHandSide
from qat.lang.AQASM.routines import QRoutine

class Rule(Buildable):
    """
    Class representing a Rule, which establishes a relationship (to some level of uncertainty) between a left hand side element and a right hand side, which in this context is a Fact.

    :param leftHandSide: Left hand side element of the rule (also known as precedent)
    :type leftHandSide: class:`lefthandside.LeftHandSide`
    :param rightHandSide: Right hand side element of the rule (also known as consecuent)
    :type rightHandSide: class:`lefthandside.Fact`
    :param uncertainty: Uncertainty of the relationship between precedent and consecuent
    :type uncertainty: float, optional
    """

    def __init__(self, lefthandside, righthandside, uncertainty=0.0) -> None:
        super().__init__()
        self.lefthandside = lefthandside
        self.righthandside = righthandside
        self.uncertainty = uncertainty


    def build(self) -> QRoutine:
        return super().build()