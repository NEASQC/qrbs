# -*- coding : utf-8 -*

from enum import Enum, auto


class QPU(Enum):
    """Enumerate encapsulating QPUs. 
    
    This class proporcionates the available Quantum Processing Units (QPU).
    """

    PYLINALG = auto()
    """
    Python Linear-algebra simulator
    """