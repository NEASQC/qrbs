# -*- coding : utf-8 -*

from enum import Enum, auto

from .knowledge_rep import Fact, Rule, KnowledgeIsland


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


class InferenceEngine():
    """Class representing an Inference Engine. 
    
    An Inference Engine is an element of a Rule-Based System that manages its rules and knowledge islands, providing the tools to evaluate them in order.

    Attributes:
        _rules (List[:obj:`Rule`], optional): List of rules established for the system.
        _islands (List[:obj:`KnowledgeIsland`], optional): List of knowledge island established for the system.
    """

    def __init__(self, rules=[], islands=[]) -> None:
        super().__init__()
        self._rules = rules
        self._islands = islands

    def assert_rule(self, rule) -> Rule:
        """Asserts a rule into the engine.

        Args:
            rule (:obj:`Rule`): The rule to be asserted.

        Returns:
            :obj:`Rule`: The asserted rule.
        """
        self._rules.append(rule)
        return self._rules[self._rules.index(rule)]

    def retract_rule(self, rule) -> None:
        """Retracts a rule from the engine.

        Args:
            rule (:obj:`Rule`): The rule to be retracted.
        """
        self._rules.remove(rule)

    def assert_island(self, island) -> KnowledgeIsland:
        """Asserts a knowledge island into the engine.

        Args:
            island (:obj:`KnowledgeIsland`): The knowledge island to be asserted.

        Returns:
            :obj:`KnowledgeIsland`: The asserted knowledge island.
        """
        self._islands.append(island)
        return self._islands[self._islands.index(island)]

    def retract_island(self, island) -> None:
        """Retracts a knowledge island from the engine.

        Args:
            island (:obj:`KnowledgeIsland`): The knowledge island to be retracted.
        """
        self._islands.remove(island)


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
        

class QRBSHandler():
    """Class encapsulating QRBS handling methods. 
    
    This class proporcionates several methods to handle operations related to Quantum Rule-Based Systems, such as their evaluation or execution.
    """

    @staticmethod
    def evaluate(qrbs, qpu):
        """Evaluates whether a QRBS can be executed on a QPU

        Args:
            qrbs (:obj:`QRBS`): The QRBS to be evaluated.
            qpu (:obj:`QPU`): The QPU in which the QRBS must be evaluated.
        """
        pass

    @staticmethod
    def execute(qrbs, qpu):
        """Executes the QRBS on the QPU

        Args:
            qrbs (:obj:`QRBS`): The QRBS to be executed.
            qpu (:obj:`QPU`): The QPU in which the QRBS must be executed.
        """
        pass
      

class QPU(Enum):
    """Enumerate encapsulating QPUs. 
    
    This class proporcionates the available Quantum Processing Units (QPU).
    """

    PYLINALG = auto()
    """
    Python Linear-algebra simulator
    """