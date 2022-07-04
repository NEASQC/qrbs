# -*- coding : utf-8 -*

from src.knowledge_rep.buildable import Buildable
from src.knowledge_rep.lefthandside.lefthandside import LeftHandSide
from qat.lang.AQASM.routines import QRoutine

class NotOperator(LeftHandSide, Buildable):
    """Class representing a NotOperator.
    
    A NotOperator negates the statement of its child. This class is used to model the Composite design pattern, acting as (one of) the Composite class.

    Attributes:
        child (:obj:`LeftHandSide`): Child which statement is negating.
    """

    def __init__(self, child) -> None:
        super().__init__()
        self.child = child

    def build(self) -> QRoutine:
        return super().build()