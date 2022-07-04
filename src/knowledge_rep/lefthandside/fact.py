# -*- coding : utf-8 -*

from src.knowledge_rep.buildable import Buildable
from src.knowledge_rep.lefthandside.lefthandside import LeftHandSide
from qat.lang.AQASM.routines import QRoutine

class Fact(LeftHandSide, Buildable):
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

    
    def build(self) -> QRoutine:
        return super().build()