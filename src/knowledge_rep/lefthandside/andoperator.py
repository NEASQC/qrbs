# -*- coding : utf-8 -*

from src.knowledge_rep.buildable import Buildable
from src.knowledge_rep.lefthandside.lefthandside import LeftHandSide
from qat.lang.AQASM.routines import QRoutine

class AndOperator(LeftHandSide, Buildable):
    """
    Class representing an AndOperator, relating the statement of its children with and AND relationship. This class is used to model the Composite design pattern, acting as (one of) the Composite class.

    :param leftChild: One of the children which is relating
    :type leftChild: class:`lefthandside.LeftHandSide`
    :param rightChild: One of the children which is relating
    :type rightChild: class:`lefthandside.LeftHandSide`
    """

    def __init__(self, leftChild, rightChild) -> None:
        super().__init__()
        self.leftChild = leftChild
        self.rightChild = rightChild

    def build(self) -> QRoutine:
        return super().build()