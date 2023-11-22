# -*- coding : utf-8 -*-

"""
Test for QRBS
"""

import random
import pytest
from neasqc_qrbs.knowledge_rep import Fact, NotOperator, AndOperator, OrOperator, Rule, KnowledgeIsland
from neasqc_qrbs.qrbs import MyQlmQPU, WorkingMemory, InferenceEngine, QRBS


class TestWorkingMemory:
    """
    Test WorkingMemory class
    """
    fact_1 = Fact('fact_1', 1.0)
    fact_2 = Fact('fact_2', 0.7)
    fact_3 = Fact('fact_3', 0.5)

    def test_workingmemory_creation(self):
        """
        Test working memory creation
        """
        working_memory_1 = WorkingMemory()
        working_memory_2 = WorkingMemory([self.fact_1, self.fact_2, self.fact_3])
        working_memory_2_copy = WorkingMemory([self.fact_1, self.fact_2, self.fact_3])

        assert working_memory_1 != working_memory_2
        assert working_memory_2 == working_memory_2_copy

    def test_workingmemory_deletion(self):
        """
        Test working memory deletion
        """
        working_memory = WorkingMemory([self.fact_1, self.fact_2, self.fact_3])

        del working_memory

    def test_workingmemory_modification(self):
        """
        Test working memory modification
        """
        working_memory = WorkingMemory([self.fact_1, self.fact_2])

        # Modify the working memory by asserting a new fact
        working_memory.assert_fact(self.fact_3)
        assert working_memory._facts == [self.fact_1, self.fact_2, self.fact_3]

        # Modify the working memory by retracting an existing fact
        working_memory.retract_fact(self.fact_1)
        assert working_memory._facts == [self.fact_2, self.fact_3]


class TestInferenceEngine:
    """
    Testing InferenceEngine class 
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

    left_hand_3 = right_hand_2
    right_hand_3 = Fact('rh_3', 0.2)
    rule_3 = Rule(left_hand_3, right_hand_3)

    island_1 = KnowledgeIsland([rule_1])
    island_2 = KnowledgeIsland([rule_1, rule_2])
    island_3 = KnowledgeIsland([rule_1, rule_3])

    def test_inferenceengine_creation(self):
        """
        Test inference engine creation
        """
        inference_engine_1 = InferenceEngine()
        inference_engine_2 = InferenceEngine([self.rule_1, self.rule_2], [self.island_1, self.island_2])
        inference_engine_2_copy = InferenceEngine([self.rule_1, self.rule_2], [self.island_1, self.island_2])

        assert inference_engine_1 != inference_engine_2
        assert inference_engine_2 == inference_engine_2_copy

        # Raises an error due to absence of rules to compose islands with
        with pytest.raises(AttributeError) as ex_info:
            _ = InferenceEngine([], [self.island_1])
        assert ex_info.match('The rules of the knowledge island are not asserted in the system')

        # Raises an error due to lack of chaining between the island's rules
        with pytest.raises(AttributeError) as ex_info:
            _ = InferenceEngine([self.rule_1, self.rule_2, self.rule_3], [self.island_3])
        assert ex_info.match('The rules of the knowledge island are not chained')

    def test_inferenceengine_deletion(self):
        """
        Test inference engine deletion
        """
        inference_engine = InferenceEngine([self.rule_1, self.rule_2], [self.island_1, self.island_2])

        del inference_engine

    def test_inferenceengine_modification(self):
        """
        Test inference engine modification
        """
        inference_engine = InferenceEngine([self.rule_1, self.rule_2], [self.island_1])

        # Modify the inference engine by asserting a new rule
        inference_engine.assert_rule(self.rule_3)
        assert inference_engine._rules == [self.rule_1, self.rule_2, self.rule_3]

        # Modify the inference engine by asserting a new knowledge island
        inference_engine.assert_island(self.island_2)
        assert inference_engine._islands == [self.island_1, self.island_2]

        # Modify the inference engine by retracting an existing knowledge island
        inference_engine.retract_island(self.island_2)
        assert inference_engine._islands == [self.island_1]

        # Modify the inference engine by retracting an existing rule
        inference_engine.retract_rule(self.rule_3)
        assert inference_engine._rules == [self.rule_1, self.rule_2]

        # Raises an error due to retracting a rule that is part of a knowledge island
        with pytest.raises(AttributeError) as ex_info:
            inference_engine.retract_rule(self.rule_1)
        assert ex_info.match('The rule to be retracted is part of a knowledge island and cannot be retracted')
        

class TestQRBS:
    """
    Testing QRBS class  
    """

    def test_qrbs_creation(self):
        """
        Test QRBS creation
        """
        system_1 = QRBS()
        _ = system_1.assert_fact('fact_1', 0.8)

        system_2 = QRBS()
        _ = system_2.assert_fact('fact_2', 0.5)

        system_2_copy = QRBS()
        _ = system_2_copy.assert_fact('fact_2', 0.5)

        assert system_1 != system_2
        assert system_2 == system_2_copy

    def test_qrbs_deletion(self):
        """
        Test QRBS deletion
        """
        system = QRBS()

        del system

    def test_qrbs_modification(self):
        """
        Test QRBS modification
        """
        system = QRBS()

        # Modify the system by asserting several elements
        fact_1 = system.assert_fact('fact_1', 0.8)
        fact_2 = system.assert_fact('fact_2', 0.3)
        fact_3 = system.assert_fact('fact_3', 0.5)
        rule_1 = system.assert_rule(fact_1, fact_2)
        rule_2 = system.assert_rule(fact_2, fact_3)
        island_1 = system.assert_island([rule_1])
        island_2 = system.assert_island([rule_1, rule_2])
        assert system._memory._facts == [fact_1, fact_2, fact_3]
        assert system._engine._rules == [rule_1, rule_2]
        assert system._engine._islands == [island_1, island_2]

        # Modify the system by retracting an existing knowledge island
        system.retract_island(island_2)
        assert system._engine._islands == [island_1]

        # Modify the system by retracting an existing rule
        system.retract_rule(rule_2)
        assert system._engine._rules == [rule_1]

        # Modify the system by retracting an existing fact
        system.retract_fact(fact_3)
        assert system._memory._facts == [fact_1, fact_2]

        # Raises an error due to retracting a rule that is part of a knowledge island
        with pytest.raises(AttributeError) as ex_info:
            system.retract_rule(rule_1)
        assert ex_info.match('The rule to be retracted is part of a knowledge island and cannot be retracted')

        # Raises an error due to retracting a fact that is part of a rule
        with pytest.raises(AttributeError) as ex_info:
            system.retract_fact(fact_1)
        assert ex_info.match('The fact to be retracted is part of a rule and cannot be retracted')


class TestEvaluation:
    """
    Testing MyQlmQPU evaluation
    """

    def test_positive_evaluation(self):
        """
        Test the positive outcome of the QRBS evaluation
        """
        system = QRBS()
        fact_1 = system.assert_fact('fact_1', 0.8)
        fact_2 = system.assert_fact('fact_2', 0.3)
        fact_3 = system.assert_fact('fact_3', 0.5)
        rule_1 = system.assert_rule(fact_1, fact_2)
        rule_2 = system.assert_rule(fact_2, fact_3)
        _ = system.assert_island([rule_1])
        _ = system.assert_island([rule_1, rule_2])

        assert MyQlmQPU.evaluate(system)

    def test_negative_evaluation(self):
        """
        Test the negative outcome of the QRBS evaluation
        """
        FACTS = 20
        system = QRBS()
        facts = [system.assert_fact('fact_{}'.format(n), random.random()) for n in range(FACTS)]
        rules = [system.assert_rule(facts[i], facts[i+1], random.random()) for i in range(FACTS - 1)]
        _ = system.assert_island(rules)

        # Raises an error due to a knowledge island using more qubits than supported
        with pytest.raises(ValueError) as ex_info:
            MyQlmQPU.evaluate(system)
        assert ex_info.match(r'.*A KnowledgeIsland surpases capacity of QPU.*')


class TestExecution:
    """
    Testing MyQlmQPU execution
    """

    def test_successful_default(self):
        """
        Test the successful default execution
        """
        system = QRBS()
        precedent = system.assert_fact('precedent', 0.8, 1.0)
        consequent = system.assert_fact('consequent', 0.3)
        implication = system.assert_rule(precedent, consequent, 1.0)
        _ = system.assert_island([implication])

        MyQlmQPU.execute(system)
        assert consequent.imprecission == 1.0

    def test_failed_default_evaluation(self):
        """
        Test the failed default evaluation
        """
        FACTS = 20
        system = QRBS()
        facts = [system.assert_fact('fact_{}'.format(n), random.random()) for n in range(FACTS)]
        rules = [system.assert_rule(facts[i], facts[i+1], random.random()) for i in range(FACTS - 1)]
        _ = system.assert_island(rules)

        # Raises an error due to a knowledge island using more qubits than supported
        with pytest.raises(ValueError) as ex_info:
            MyQlmQPU.execute(system)
        assert ex_info.match(r'.*A KnowledgeIsland surpases capacity of QPU.*')

    def test_failed_default_execution(self):
        """
        Test the failed default execution
        """
        pass

    def test_successful_specified(self):
        """
        Test the successful specified execution
        """
        system = QRBS()
        precedent = system.assert_fact('precedent', 0.8, 1.0)
        consequent = system.assert_fact('consequent', 0.3)
        implication = system.assert_rule(precedent, consequent, 1.0)
        island = system.assert_island([implication])

        MyQlmQPU.execute(system, [island])
        assert consequent.imprecission == 1.0

    def test_failed_specified_evaluation(self):
        """
        Test the failed specified evaluation
        """
        FACTS = 20
        system = QRBS()
        facts = [system.assert_fact('fact_{}'.format(n), random.random()) for n in range(FACTS)]
        rules = [system.assert_rule(facts[i], facts[i+1], random.random()) for i in range(FACTS - 1)]
        island = system.assert_island(rules)

        # Raises an error due to a knowledge island using more qubits than supported
        with pytest.raises(ValueError) as ex_info:
            MyQlmQPU.execute(system, [island])
        assert ex_info.match(r'.*A KnowledgeIsland surpases capacity of QPU.*')

    def test_failed_specified_execution(self):
        """
        Test the failed specified execution
        """
        system_1 = QRBS()
        precedent = system_1.assert_fact('precedent', 0.8, 1.0)
        consequent = system_1.assert_fact('consequent', 0.3)
        implication = system_1.assert_rule(precedent, consequent, 1.0)
        island_1 = system_1.assert_island([implication])

        system_2 = QRBS()

        # Raises an error due to a knowledge island not being part of the system
        with pytest.raises(ValueError) as ex_info:
            MyQlmQPU.execute(system_2, [island_1])
        assert ex_info.match(r'.*A specified KnowledgeIsland is not part of the QRBS.*')


class TestEvaluationFuzzy:
    """
    Testing MyQlmQPU evaluation with the fuzzy model
    """

    def test_positive_evaluation(self):
        """
        Test the positive outcome of the QRBS evaluation
        """
        system = QRBS()
        fact_1 = system.assert_fact('fact_1', 0.8)
        fact_2 = system.assert_fact('fact_2', 0.3)
        fact_3 = system.assert_fact('fact_3', 0.5)
        rule_1 = system.assert_rule(fact_1, fact_2)
        rule_2 = system.assert_rule(fact_2, fact_3)
        _ = system.assert_island([rule_1])
        _ = system.assert_island([rule_1, rule_2])

        assert MyQlmQPU.evaluate(system, model='fuzzy')

    def test_negative_evaluation(self):
        """
        Test the negative outcome of the QRBS evaluation
        """
        FACTS = 20
        system = QRBS()
        facts = [system.assert_fact('fact_{}'.format(n), random.random()) for n in range(FACTS)]
        rules = [system.assert_rule(facts[i], facts[i+1], random.random()) for i in range(FACTS - 1)]
        _ = system.assert_island(rules)

        # Raises an error due to a knowledge island using more qubits than supported
        with pytest.raises(ValueError) as ex_info:
            MyQlmQPU.evaluate(system, model='fuzzy')
        assert ex_info.match(r'.*A KnowledgeIsland surpases capacity of QPU.*')


class TestExecutionFuzzy:
    """
    Testing MyQlmQPU execution with the fuzzy model
    """

    def test_successful_default(self):
        """
        Test the successful default execution
        """
        system = QRBS()
        precedent = system.assert_fact('precedent', 0.8, 1.0)
        consequent = system.assert_fact('consequent', 0.3)
        implication = system.assert_rule(precedent, consequent, 1.0)
        _ = system.assert_island([implication])

        MyQlmQPU.execute(system, model='fuzzy')
        assert consequent.imprecission == 1.0

    def test_failed_default_evaluation(self):
        """
        Test the failed default evaluation
        """
        FACTS = 20
        system = QRBS()
        facts = [system.assert_fact('fact_{}'.format(n), random.random()) for n in range(FACTS)]
        rules = [system.assert_rule(facts[i], facts[i+1], random.random()) for i in range(FACTS - 1)]
        _ = system.assert_island(rules)

        # Raises an error due to a knowledge island using more qubits than supported
        with pytest.raises(ValueError) as ex_info:
            MyQlmQPU.execute(system, model='fuzzy')
        assert ex_info.match(r'.*A KnowledgeIsland surpases capacity of QPU.*')

    def test_failed_default_execution(self):
        """
        Test the failed default execution
        """
        pass

    def test_successful_specified(self):
        """
        Test the successful specified execution
        """
        system = QRBS()
        precedent = system.assert_fact('precedent', 0.8, 1.0)
        consequent = system.assert_fact('consequent', 0.3)
        implication = system.assert_rule(precedent, consequent, 1.0)
        island = system.assert_island([implication])

        MyQlmQPU.execute(system, [island], model='fuzzy')
        assert consequent.imprecission == 1.0

    def test_failed_specified_evaluation(self):
        """
        Test the failed specified evaluation
        """
        FACTS = 20
        system = QRBS()
        facts = [system.assert_fact('fact_{}'.format(n), random.random()) for n in range(FACTS)]
        rules = [system.assert_rule(facts[i], facts[i+1], random.random()) for i in range(FACTS - 1)]
        island = system.assert_island(rules)

        # Raises an error due to a knowledge island using more qubits than supported
        with pytest.raises(ValueError) as ex_info:
            MyQlmQPU.execute(system, [island], model='fuzzy')
        assert ex_info.match(r'.*A KnowledgeIsland surpases capacity of QPU.*')

    def test_failed_specified_execution(self):
        """
        Test the failed specified execution
        """
        system_1 = QRBS()
        precedent = system_1.assert_fact('precedent', 0.8, 1.0)
        consequent = system_1.assert_fact('consequent', 0.3)
        implication = system_1.assert_rule(precedent, consequent, 1.0)
        island_1 = system_1.assert_island([implication])

        system_2 = QRBS()

        # Raises an error due to a knowledge island not being part of the system
        with pytest.raises(ValueError) as ex_info:
            MyQlmQPU.execute(system_2, [island_1], model='fuzzy')
        assert ex_info.match(r'.*A specified KnowledgeIsland is not part of the QRBS.*')


class TestEvaluationBayes:
    """
    Testing MyQlmQPU evaluation with the bayesian model
    """

    def test_positive_evaluation(self):
        """
        Test the positive outcome of the QRBS evaluation
        """
        system = QRBS()
        fact_1 = system.assert_fact('fact_1', 0.8)
        fact_2 = system.assert_fact('fact_2', 0.3)
        fact_3 = system.assert_fact('fact_3', 0.5)
        rule_1 = system.assert_rule(fact_1, fact_2)
        rule_2 = system.assert_rule(fact_2, fact_3)
        _ = system.assert_island([rule_1])
        _ = system.assert_island([rule_1, rule_2])

        assert MyQlmQPU.evaluate(system, model='bayes')

    def test_negative_evaluation(self):
        """
        Test the negative outcome of the QRBS evaluation
        """
        FACTS = 25
        system = QRBS()
        facts = [system.assert_fact('fact_{}'.format(n), random.random()) for n in range(FACTS)]
        rules = [system.assert_rule(facts[i], facts[i+1], random.random()) for i in range(FACTS - 1)]
        _ = system.assert_island(rules)

        # Raises an error due to a knowledge island using more qubits than supported
        with pytest.raises(ValueError) as ex_info:
            MyQlmQPU.evaluate(system, model='bayes')
        assert ex_info.match(r'.*A KnowledgeIsland surpases capacity of QPU.*')


class TestExecutionBayes:
    """
    Testing MyQlmQPU execution with the bayesian model
    """

    def test_successful_default(self):
        """
        Test the successful default execution
        """
        system = QRBS()
        precedent = system.assert_fact('precedent', 0.8, 1.0)
        consequent = system.assert_fact('consequent', 0.3)
        implication = system.assert_rule(precedent, consequent, 1.0)
        _ = system.assert_island([implication])

        MyQlmQPU.execute(system, model='bayes')
        assert consequent.imprecission == 1.0

    def test_failed_default_evaluation(self):
        """
        Test the failed default evaluation
        """
        FACTS = 30
        system = QRBS()
        facts = [system.assert_fact('fact_{}'.format(n), random.random()) for n in range(FACTS)]
        rules = [system.assert_rule(facts[i], facts[i+1], random.random()) for i in range(FACTS - 1)]
        _ = system.assert_island(rules)

        # Raises an error due to a knowledge island using more qubits than supported
        with pytest.raises(ValueError) as ex_info:
            MyQlmQPU.execute(system, model='bayes')
        assert ex_info.match(r'.*A KnowledgeIsland surpases capacity of QPU.*')

    def test_failed_default_execution(self):
        """
        Test the failed default execution
        """
        pass

    def test_successful_specified(self):
        """
        Test the successful specified execution
        """
        system = QRBS()
        precedent = system.assert_fact('precedent', 0.8, 1.0)
        consequent = system.assert_fact('consequent', 0.3)
        implication = system.assert_rule(precedent, consequent, 1.0)
        island = system.assert_island([implication])

        MyQlmQPU.execute(system, [island], model='bayes')
        assert consequent.imprecission == 1.0

    def test_failed_specified_evaluation(self):
        """
        Test the failed specified evaluation
        """
        FACTS = 30
        system = QRBS()
        facts = [system.assert_fact('fact_{}'.format(n), random.random()) for n in range(FACTS)]
        rules = [system.assert_rule(facts[i], facts[i+1], random.random()) for i in range(FACTS - 1)]
        island = system.assert_island(rules)

        # Raises an error due to a knowledge island using more qubits than supported
        with pytest.raises(ValueError) as ex_info:
            MyQlmQPU.execute(system, [island], model='bayes')
        assert ex_info.match(r'.*A KnowledgeIsland surpases capacity of QPU.*')

    def test_failed_specified_execution(self):
        """
        Test the failed specified execution
        """
        system_1 = QRBS()
        precedent = system_1.assert_fact('precedent', 0.8, 1.0)
        consequent = system_1.assert_fact('consequent', 0.3)
        implication = system_1.assert_rule(precedent, consequent, 1.0)
        island_1 = system_1.assert_island([implication])

        system_2 = QRBS()

        # Raises an error due to a knowledge island not being part of the system
        with pytest.raises(ValueError) as ex_info:
            MyQlmQPU.execute(system_2, [island_1], model='bayes')
        assert ex_info.match(r'.*A specified KnowledgeIsland is not part of the QRBS.*')
        