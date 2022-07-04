# -*- coding : utf-8 -*

from src.knowledge_rep.lefthandside.fact import Fact


class WorkingMemory():
    """Class representing a Working Memory. 
    
    A Working Memory is an element of a Rule-Based System that manages its facts, keeping trace of their state.

    Attributes:
        _facts (List[:obj:`Fact`], optional): List of facts asserted into the system.
    """

    def __init__(self, facts=[]) -> None:
        super().__init__()
        self._facts = facts

    def assert_fact(self, fact) -> Fact:
        """Asserts a fact into the memory.

        Args:
            fact (:obj:`Fact`): The fact to be asserted.

        Returns:
            :obj:`Fact`: The asserted fact.
        """
        self._facts.append(fact)
        return self._facts[self._facts.index(fact)]

    def retract_fact(self, fact) -> None:
        """Retracts a fact from the memory.

        Args:
            fact (:obj:`Fact`): The fact to be retracted.
        """
        self._facts.remove(fact)
