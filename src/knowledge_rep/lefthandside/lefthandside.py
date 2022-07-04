# -*- coding : utf-8 -*

from abc import ABC

class LeftHandSide(ABC):
    """Interface for elements that can be part of the left hand side of a rule. This class is used to model the Composite design pattern, acting as the Component interface.
    """

    def __init__(self) -> None:
        super().__init__()