# -*- coding : utf-8 -*

from src.knowledge_rep.buildable import Buildable
from src.knowledge_rep.lefthandside.lefthandside import LeftHandSide
from qat.lang.AQASM.routines import QRoutine

class OrOperator(LeftHandSide, Buildable):
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

    def build(self) -> QRoutine:
        return super().build()