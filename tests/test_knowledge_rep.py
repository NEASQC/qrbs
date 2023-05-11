# -*- coding : utf-8 -*-

"""
Test for KnowledgeRep elements
"""

import pytest
from neasqc_qrbs.knowledge_rep import Fact, NotOperator, AndOperator, OrOperator, Rule, KnowledgeIsland


class TestFact:
    """
    Testing Fact class  
    """

    fact_attribute = 'test_fact'
    fact_value = 1.0

    str_modification = 'modified'
    float_modification = 0.2

    def test_fact_creation(self):
        """
        Test fact creation
        """
        fact_1 = Fact(self.fact_attribute, self.fact_value + self.float_modification)
        fact_2 = Fact(self.fact_attribute, self.fact_value)
        fact_2_copy = Fact(self.fact_attribute, self.fact_value)

        assert fact_1 != fact_2
        assert fact_2 == fact_2_copy

    def test_fact_deletion(self):
        """
        Test fact deletion
        """
        fact = Fact(self.fact_attribute, self.fact_value)

        del fact

    def test_fact_modification(self):
        """
        Test fact modification
        """
        fact = Fact(self.fact_attribute, self.fact_value)
        fact.attribute = self.str_modification
        fact.value = self.float_modification
        
        assert fact.attribute == self.str_modification
        assert fact.value == self.float_modification

class TestRule:
    """
    Testing Rule class  
    """

    in_1 = Fact('lh_1', 1.0)
    in_2 = Fact('lh_2', 0.7)
    in_3 = Fact('lh_3', 0.5)
    left_hand = OrOperator(AndOperator(in_1, in_2),NotOperator(in_3))
    right_hand = Fact('rh', 0.5)

    left_hand_modified = AndOperator(OrOperator(NotOperator(in_1), in_2), in_3)
    right_hand_modified = Fact('rh_modified', 0.0)

    def test_rule_creation(self):
        """
        Test rule creation
        """
        rule_1 = Rule(self.in_1, self.right_hand)
        rule_2 = Rule(self.left_hand, self.right_hand)
        rule_2_copy = Rule(self.left_hand, self.right_hand)

        assert rule_1 != rule_2
        assert rule_2 == rule_2_copy

    def test_rule_deletion(self):
        """
        Test rule deletion
        """
        rule = Rule(self.left_hand, self.right_hand)

        del rule

    def test_rule_modification(self):
        """
        Test rule modification
        """
        rule = Rule(self.left_hand, self.right_hand)
        rule.lefthandside = self.left_hand_modified
        rule.righthandside = self.right_hand_modified

        assert rule.lefthandside == self.left_hand_modified
        assert rule.righthandside == self.right_hand_modified


class TestKnowledgeIsland:
    """
    Testing KnowledgeIsland class  
    """
    in_1 = Fact('lh_1', 1.0)
    in_2 = Fact('lh_2', 0.7)
    in_3 = Fact('lh_3', 0.5)
    left_hand_1 = OrOperator(in_1, NotOperator(in_2))
    right_hand_1 = Fact('rh_1', 0.5)
    rule_1 = Rule(left_hand_1, right_hand_1)

    left_hand_2 = AndOperator(right_hand_1, in_3)
    right_hand_2 = Fact('rh_2', 0.0)
    rule_2 = Rule(left_hand_2, right_hand_2)

    def test_island_creation(self):
        """
        Test the constructor
        """
        island_1 = KnowledgeIsland([self.rule_1])
        island_2 = KnowledgeIsland([self.rule_1, self.rule_2])
        island_2_copy = KnowledgeIsland([self.rule_1, self.rule_2])

        assert island_1 != island_2
        assert island_2 == island_2_copy

    def test_island_deletion(self):
        """
        Test knowledge island deletion
        """
        island = KnowledgeIsland([self.rule_1, self.rule_2])

        del island

    def test_island_modification(self):
        """
        Test knowledge island modification
        """
        island = KnowledgeIsland([self.rule_1])

        island.rules = [self.rule_2]

        assert island.rules == [self.rule_2]


class TestUncerainty:
    """
    Testing imprecission and uncertainty
    """
    def test_imprecission(self):
        """
        Test imprecission
        """
        fact = Fact('fact', 0.5, 0.5)
        assert fact.imprecission == 0.5

        # Raises an error due to invalid imprecission values
        with pytest.raises(ValueError) as ex_info:
            fact.imprecission = -0.5
        assert ex_info.match(r'Imprecission must be in range \[0,1\]')
        with pytest.raises(ValueError) as ex_info:
            fact.imprecission = 1.5
        assert ex_info.match(r'Imprecission must be in range \[0,1\]')

    def test_uncertainty(self):
        """
        Test uncertainty
        """
        fact_1 = Fact('fact_1', 0.5)
        fact_2 = Fact('fact_2', 0.5)
        rule = Rule(fact_1, fact_2, 0.5)
        assert rule.uncertainty == 0.5

        # Raises an error due to invalid uncertainty values
        with pytest.raises(ValueError) as ex_info:
            rule.uncertainty = -0.5
        assert ex_info.match(r'Uncertainty must be in range \[0,1\]')
        with pytest.raises(ValueError) as ex_info:
            rule.uncertainty = 1.5
        assert ex_info.match(r'Uncertainty must be in range \[0,1\]')
