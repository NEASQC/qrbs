# -*- coding : utf-8 -*


from src.knowledge_rep.rule import Rule
from src.knowledge_rep.knowledgeisland import KnowledgeIsland


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