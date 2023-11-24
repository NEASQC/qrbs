# -*- coding : utf-8 -*-

"""
Test for KnowledgeRep elements
"""

import numpy as np
import pytest
from neasqc_qrbs.knowledge_rep import BuilderBayes, BuilderImpl, BuilderFuzzy, Fact, NotOperator, AndOperator, OrOperator, Rule, KnowledgeIsland
from qat.lang.AQASM import QRoutine, Program, CCNOT, CNOT, X, RY


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
        rule.left_hand_side = self.left_hand_modified
        rule.right_hand_side = self.right_hand_modified

        assert rule.left_hand_side == self.left_hand_modified
        assert rule.right_hand_side == self.right_hand_modified


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


class TestCertainty:
    """
    Testing precision and uncertainty
    """
    def test_precision(self):
        """
        Test precision
        """
        fact = Fact('fact', 0.5, 0.5)
        assert fact.precision == 0.5

        # Raises an error due to invalid precision values
        with pytest.raises(ValueError) as ex_info:
            fact.precision = -0.5
        assert ex_info.match(r'Precision must be in range \[0,1\]')
        with pytest.raises(ValueError) as ex_info:
            fact.precision = 1.5
        assert ex_info.match(r'Precision must be in range \[0,1\]')

    def test_certainty(self):
        """
        Test certainty
        """
        fact_1 = Fact('fact_1', 0.5)
        fact_2 = Fact('fact_2', 0.5)
        rule = Rule(fact_1, fact_2, 0.5)
        assert rule.certainty == 0.5

        # Raises an error due to invalid uncertainty values
        with pytest.raises(ValueError) as ex_info:
            rule.certainty = -0.5
        assert ex_info.match(r'Certainty must be in range \[0,1\]')
        with pytest.raises(ValueError) as ex_info:
            rule.certainty = 1.5
        assert ex_info.match(r'Certainty must be in range \[0,1\]')


class TestBuilder:
    """
    Testing BuilderImpl
    """
    in_1 = Fact('lh_1', 1.0)
    in_2 = Fact('lh_2', 0.7)
    in_3 = Fact('lh_3', 0.5)

    not_op = NotOperator(in_2)
    or_op = OrOperator(in_1, not_op)
    right_hand_1 = Fact('rh_1', 0.5)
    rule_1 = Rule(or_op, right_hand_1)

    and_op = AndOperator(right_hand_1, in_3)
    right_hand_2 = Fact('rh_2', 0.0)
    rule_2 = Rule(and_op, right_hand_2)

    island = KnowledgeIsland([rule_1, rule_2])

    def _build_circ(self, routine):
        prog = Program()
        qbits = prog.qalloc(routine.arity)
        prog.apply(routine, qbits)
        return prog

    def test_build_fact(self):
        """
        Test building fact
        """
        built_routine = self.in_1.build(BuilderImpl)

        test_routine = QRoutine()
        test_routine.apply(BuilderImpl.M(self.in_1.precision), 0)
        
        [built_circ, test_circ] = [self._build_circ(routine).to_circ() for routine in [built_routine, test_routine]]

        for (built_op, test_op) in zip(built_circ.iterate_simple(), test_circ.iterate_simple()):
            assert built_op == test_op

    def test_build_and(self):
        """
        Test building and operator
        """
        built_routine = self.and_op.build(BuilderImpl)

        test_routine = QRoutine()
        test_routine.apply(CCNOT, 0, 1, 2)
        
        [built_circ, test_circ] = [self._build_circ(routine).to_circ() for routine in [built_routine, test_routine]]

        for (built_op, test_op) in zip(built_circ.iterate_simple(), test_circ.iterate_simple()):
            assert built_op == test_op

    def test_build_or(self):
        """
        Test building or operator
        """
        built_routine = self.or_op.build(BuilderImpl)

        test_routine = QRoutine()
        test_routine.apply(CCNOT, 0, 1, 2)
        test_routine.apply(CNOT, 0, 2)
        test_routine.apply(CNOT, 1, 2)
        
        [built_circ, test_circ] = [self._build_circ(routine).to_circ() for routine in [built_routine, test_routine]]

        for (built_op, test_op) in zip(built_circ.iterate_simple(), test_circ.iterate_simple()):
            assert built_op == test_op

    def test_build_not(self):
        """
        Test building not operator
        """
        built_routine = self.not_op.build(BuilderImpl)

        test_routine = QRoutine()
        test_routine.apply(CNOT, 0, 1)
        test_routine.apply(X, 1)
        
        [built_circ, test_circ] = [self._build_circ(routine).to_circ() for routine in [built_routine, test_routine]]

        for (built_op, test_op) in zip(built_circ.iterate_simple(), test_circ.iterate_simple()):
            assert built_op == test_op

    def test_build_rule(self):
        """
        Test building rule
        """
        built_routine = self.rule_1.build(BuilderImpl)

        test_routine = QRoutine()
        test_routine.apply(BuilderImpl.M(self.in_1.precision), 0)
        test_routine.apply(BuilderImpl.M(self.in_2.precision), 1)
        test_routine.apply(CNOT, 1, 3)
        test_routine.apply(X, 3)
        test_routine.apply(CCNOT, 0, 3, 4)
        test_routine.apply(CNOT, 0, 4)
        test_routine.apply(CNOT, 3, 4)
        test_routine.apply(BuilderImpl.M(self.rule_1.certainty), 5)
        test_routine.apply(CCNOT, 4, 5, 2)
        
        [built_circ, test_circ] = [self._build_circ(routine).to_circ() for routine in [built_routine, test_routine]]

        for (built_op, test_op) in zip(built_circ.iterate_simple(), test_circ.iterate_simple()):
            assert built_op == test_op

    def test_build_island(self):
        """
        Test building island
        """
        built_routine = self.island.build(BuilderImpl)

        test_routine = QRoutine()
        test_routine.apply(BuilderImpl.M(self.in_1.precision), 0)
        test_routine.apply(BuilderImpl.M(self.in_2.precision), 1)
        test_routine.apply(BuilderImpl.M(self.in_3.precision), 2)
        test_routine.apply(CNOT, 1, 5)
        test_routine.apply(X, 5)
        test_routine.apply(CCNOT, 0, 5, 6)
        test_routine.apply(CNOT, 0, 6)
        test_routine.apply(CNOT, 5, 6)
        test_routine.apply(BuilderImpl.M(self.rule_1.certainty), 7)
        test_routine.apply(CCNOT, 6, 7, 3)
        test_routine.apply(CCNOT, 3, 2, 8)
        test_routine.apply(BuilderImpl.M(self.rule_2.certainty), 9)
        test_routine.apply(CCNOT, 8, 9, 4)
        
        [built_circ, test_circ] = [self._build_circ(routine).to_circ() for routine in [built_routine, test_routine]]

        for (built_op, test_op) in zip(built_circ.iterate_simple(), test_circ.iterate_simple()):
            assert built_op == test_op


class TestBuilderFuzzy:
    """
    Testing BuilderFuzzy
    """
    in_1 = Fact('lh_1', 1.0)
    in_2 = Fact('lh_2', 0.7)
    in_3 = Fact('lh_3', 0.5)

    not_op = NotOperator(in_2)
    or_op = OrOperator(in_1, not_op)
    right_hand_1 = Fact('rh_1', 0.5)
    rule_1 = Rule(or_op, right_hand_1)

    and_op = AndOperator(right_hand_1, in_3)
    right_hand_2 = Fact('rh_2', 0.0)
    rule_2 = Rule(and_op, right_hand_2)

    island = KnowledgeIsland([rule_1, rule_2])

    def _build_circ(self, routine):
        prog = Program()
        qbits = prog.qalloc(routine.arity)
        prog.apply(routine, qbits)
        return prog

    def test_build_fact(self):
        """
        Test building fact
        """
        built_routine = self.in_1.build(BuilderFuzzy)

        test_routine = QRoutine()
        test_routine.apply(RY(self.in_1.precision), 0)
        
        [built_circ, test_circ] = [self._build_circ(routine).to_circ() for routine in [built_routine, test_routine]]

        for (built_op, test_op) in zip(built_circ.iterate_simple(), test_circ.iterate_simple()):
            assert built_op == test_op

    def test_build_and(self):
        """
        Test building and operator
        """
        built_routine = self.and_op.build(BuilderFuzzy)

        test_routine = QRoutine()
        test_routine.apply(CCNOT, 0, 1, 2)
        
        [built_circ, test_circ] = [self._build_circ(routine).to_circ() for routine in [built_routine, test_routine]]

        for (built_op, test_op) in zip(built_circ.iterate_simple(), test_circ.iterate_simple()):
            assert built_op == test_op

    def test_build_or(self):
        """
        Test building or operator
        """
        built_routine = self.or_op.build(BuilderFuzzy)

        test_routine = QRoutine()
        test_routine.apply(X, 0)
        test_routine.apply(X, 1)
        test_routine.apply(CCNOT, 0, 1, 2)
        test_routine.apply(X, 0)
        test_routine.apply(X, 1)
        test_routine.apply(X, 2)
        
        [built_circ, test_circ] = [self._build_circ(routine).to_circ() for routine in [built_routine, test_routine]]

        for (built_op, test_op) in zip(built_circ.iterate_simple(), test_circ.iterate_simple()):
            assert built_op == test_op

    def test_build_not(self):
        """
        Test building not operator
        """
        built_routine = self.not_op.build(BuilderFuzzy)

        test_routine = QRoutine()
        test_routine.apply(CNOT, 0, 1)
        test_routine.apply(X, 1)
        
        [built_circ, test_circ] = [self._build_circ(routine).to_circ() for routine in [built_routine, test_routine]]

        for (built_op, test_op) in zip(built_circ.iterate_simple(), test_circ.iterate_simple()):
            assert built_op == test_op

    def test_build_rule(self):
        """
        Test building rule
        """
        built_routine = self.rule_1.build(BuilderFuzzy)

        test_routine = QRoutine()
        test_routine.apply(RY(self.in_1.precision * np.pi), 0)
        test_routine.apply(RY(self.in_2.precision * np.pi), 1)
        test_routine.apply(CNOT, 1, 3)
        test_routine.apply(X, 3)
        test_routine.apply(X, 0)
        test_routine.apply(X, 3)
        test_routine.apply(CCNOT, 0, 3, 4)
        test_routine.apply(X, 0)
        test_routine.apply(X, 3)
        test_routine.apply(X, 4)
        test_routine.apply(RY(self.rule_1.certainty * np.pi), 5)
        test_routine.apply(CCNOT, 4, 5, 2)
        
        [built_circ, test_circ] = [self._build_circ(routine).to_circ() for routine in [built_routine, test_routine]]

        for (built_op, test_op) in zip(built_circ.iterate_simple(), test_circ.iterate_simple()):
            assert built_op == test_op

    def test_build_island(self):
        """
        Test building island
        """
        built_routine = self.island.build(BuilderFuzzy)

        test_routine = QRoutine()
        test_routine.apply(RY(self.in_1.precision * np.pi), 0)
        test_routine.apply(RY(self.in_2.precision * np.pi), 1)
        test_routine.apply(RY(self.in_3.precision * np.pi), 2)
        test_routine.apply(CNOT, 1, 5)
        test_routine.apply(X, 5)
        test_routine.apply(X, 0)
        test_routine.apply(X, 5)
        test_routine.apply(CCNOT, 0, 5, 6)
        test_routine.apply(X, 0)
        test_routine.apply(X, 5)
        test_routine.apply(X, 6)
        test_routine.apply(RY(self.rule_1.certainty * np.pi), 7)
        test_routine.apply(CCNOT, 6, 7, 3)
        test_routine.apply(CCNOT, 3, 2, 8)
        test_routine.apply(RY(self.rule_2.certainty * np.pi), 9)
        test_routine.apply(CCNOT, 8, 9, 4)
        
        [built_circ, test_circ] = [self._build_circ(routine).to_circ() for routine in [built_routine, test_routine]]

        for (built_op, test_op) in zip(built_circ.iterate_simple(), test_circ.iterate_simple()):
            assert built_op == test_op


class TestBuilderBayes:
    """
    Testing BuilderBayes
    """
    in_1 = Fact('lh_1', 1.0)
    in_2 = Fact('lh_2', 0.7)
    in_3 = Fact('lh_3', 0.5)

    not_op = NotOperator(in_2)
    or_op = OrOperator(in_1, not_op)
    right_hand_1 = Fact('rh_1', 0.5)
    rule_1 = Rule(or_op, right_hand_1)

    and_op = AndOperator(right_hand_1, in_3)
    right_hand_2 = Fact('rh_2', 0.0)
    rule_2 = Rule(and_op, right_hand_2)

    island = KnowledgeIsland([rule_1, rule_2])

    def _build_circ(self, routine):
        prog = Program()
        qbits = prog.qalloc(routine.arity)
        prog.apply(routine, qbits)
        return prog

    def test_build_fact(self):
        """
        Test building fact
        """
        built_routine = self.in_1.build(BuilderBayes)

        test_routine = QRoutine()
        test_routine.apply(RY(self.in_1.precision), 0)
        
        [built_circ, test_circ] = [self._build_circ(routine).to_circ() for routine in [built_routine, test_routine]]

        for (built_op, test_op) in zip(built_circ.iterate_simple(), test_circ.iterate_simple()):
            assert built_op == test_op

    def test_build_and(self):
        """
        Test building and operator
        """
        built_routine = self.and_op.build(BuilderBayes)

        test_routine = QRoutine()
        test_routine.apply(CCNOT, 0, 1, 2)
        
        [built_circ, test_circ] = [self._build_circ(routine).to_circ() for routine in [built_routine, test_routine]]

        for (built_op, test_op) in zip(built_circ.iterate_simple(), test_circ.iterate_simple()):
            assert built_op == test_op

    def test_build_or(self):
        """
        Test building or operator
        """
        built_routine = self.or_op.build(BuilderBayes)

        test_routine = QRoutine()
        test_routine.apply(X, 0)
        test_routine.apply(CCNOT, 0, 1, 2)
        test_routine.apply(X, 0)
        test_routine.apply(X, 1)
        test_routine.apply(CCNOT, 0, 1, 2)
        test_routine.apply(X, 1)
        test_routine.apply(CCNOT, 0, 1, 2)
        
        [built_circ, test_circ] = [self._build_circ(routine).to_circ() for routine in [built_routine, test_routine]]

        for (built_op, test_op) in zip(built_circ.iterate_simple(), test_circ.iterate_simple()):
            assert built_op == test_op

    def test_build_not(self):
        """
        Test building not operator
        """
        built_routine = self.not_op.build(BuilderBayes)

        test_routine = QRoutine()
        test_routine.apply(CNOT, 0, 1)
        test_routine.apply(X, 1)
        
        [built_circ, test_circ] = [self._build_circ(routine).to_circ() for routine in [built_routine, test_routine]]

        for (built_op, test_op) in zip(built_circ.iterate_simple(), test_circ.iterate_simple()):
            assert built_op == test_op

    def test_build_rule(self):
        """
        Test building rule
        """
        built_routine = self.rule_1.build(BuilderBayes)

        test_routine = QRoutine()
        test_routine.apply(RY(self.in_1.precision * np.pi), 0)
        test_routine.apply(RY(self.in_2.precision * np.pi), 1)
        test_routine.apply(CNOT, 1, 3)
        test_routine.apply(X, 3)
        test_routine.apply(X, 0)
        test_routine.apply(CCNOT, 0, 3, 4)
        test_routine.apply(X, 0)
        test_routine.apply(X, 3)
        test_routine.apply(CCNOT, 0, 3, 4)
        test_routine.apply(X, 3)
        test_routine.apply(CCNOT, 0, 3, 4)
        test_routine.apply(BuilderBayes.CRY(self.rule_1.certainty), 4, 2)
        
        [built_circ, test_circ] = [self._build_circ(routine).to_circ() for routine in [built_routine, test_routine]]

        for (built_op, test_op) in zip(built_circ.iterate_simple(), test_circ.iterate_simple()):
            assert built_op == test_op

    def test_build_island(self):
        """
        Test building island
        """
        built_routine = self.island.build(BuilderBayes)

        test_routine = QRoutine()
        test_routine.apply(RY(self.in_1.precision * np.pi), 0)
        test_routine.apply(RY(self.in_2.precision * np.pi), 1)
        test_routine.apply(RY(self.in_3.precision * np.pi), 2)
        test_routine.apply(CNOT, 1, 5)
        test_routine.apply(X, 5)
        test_routine.apply(X, 0)
        test_routine.apply(CCNOT, 0, 5, 6)
        test_routine.apply(X, 0)
        test_routine.apply(X, 5)
        test_routine.apply(CCNOT, 0, 5, 6)
        test_routine.apply(X, 5)
        test_routine.apply(CCNOT, 0, 5, 6)
        test_routine.apply(BuilderBayes.CRY(self.rule_1.certainty), 6, 3)
        test_routine.apply(CCNOT, 3, 2, 7)
        test_routine.apply(BuilderBayes.CRY(self.rule_1.certainty), 7, 4)
        
        [built_circ, test_circ] = [self._build_circ(routine).to_circ() for routine in [built_routine, test_routine]]

        for (built_op, test_op) in zip(built_circ.iterate_simple(), test_circ.iterate_simple()):
            assert built_op == test_op
