# -*- coding : utf-8 -*


from src.knowledge_rep.knowledgeisland import KnowledgeIsland
from src.knowledge_rep.lefthandside.fact import Fact
from src.knowledge_rep.rule import Rule
from src.qrbs.inferenceengine import InferenceEngine
from src.qrbs.workingmemory import WorkingMemory


class QRBS():
    """Class representing a Quantum Rule-Based System. 
    
    A Quantum Rule-Based System (QRBS) is a Rule-Based System implemented in a quantum computer, taking advatange of some of its capabilities, like quantum superposition, to represent certain aspects such as imprecission and uncertainty.

    Attributes:
        _memory (:obj:`WorkingMemory`): The Working Memory of the system.
        _engine (:obj:`InferenceEngine`): The Inference Engine of the system.
    """

    def __init__(self) -> None:
        super().__init__()
        self._memory = WorkingMemory()
        self._engine = InferenceEngine()

    def assert_fact(self, attribute, value, imprecission=0.0) -> Fact:
        """Creates a fact and asserts it into the system.

        Args:
            attribute (str): The attribute of the fact.
            value (float): The value of the fact.
            imprecission (float, optional): The imprecission of the rule.

        Returns:
            :obj:`Rule`: The asserted rule.
        """
        fact = Fact(attribute, value, imprecission)
        return self._memory.assert_fact(fact)

    def retract_fact(self, fact) -> None:
        """Retracts a fact from the system.

        Args:
            fact (:obj:`Fact`): The fact to be retracted.
        """
        self._memory.retract_fact(fact)

    def assert_rule(self, lefthandside, righthandside, uncertainty=0.0) -> Rule:
        """Creates a rule and asserts it into the system.

        Args:
            lefthandside (:obj:`LeftHandSide`): The left hand side of the rule.
            righthandside (:obj:`Fact`): The right hand side of the rule.
            uncertainty (float, optional): The uncertainty of the rule.

        Returns:
            :obj:`Rule`: The asserted rule.
        """
        rule = Rule(lefthandside, righthandside, uncertainty)
        return self._engine.assert_rule(rule)

    def retract_rule(self, rule) -> None:
        """Retracts a rule from the system.

        Args:
            rule (:obj:`Rule`): The rule to be retracted.
        """
        self._engine.retract_rule(rule)

    def assert_island(self, rules) -> KnowledgeIsland:
        """Creates a knowledge island and asserts it into the system.

        Args:
            rules (List[:obj:`Rule`]): The rules of the knowledge island.

        Returns:
            :obj:`KnowledgeIsland`: The asserted knowledge island.
        """
        island = KnowledgeIsland(rules)
        return self._engine.assert_island(island)

    def retract_island(self, island) -> None:
        """Retracts a knowledge island from the system.

        Args:
            island (:obj:`KnowledgeIsland`): The knowledge island to be retracted.
        """
        self._engine.retract_island(island)