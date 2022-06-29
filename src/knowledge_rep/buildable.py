# -*- coding : utf-8 -*

from abc import ABC, abstractmethod
from qat.lang.AQASM.routines import QRoutine

class Buildable(ABC):
    """
    Interface for knowledge elements that can be built into quantum circuits
    """

    def __init__(self) -> None:
        super().__init__()

    
    @abstractmethod
    def build(self) -> QRoutine:
        pass

