# -*- coding : utf-8 -*-

"""
Test for KnowledgeRep elements
"""

from neasqc_qrbs.knowledge_rep import Fact, NotOperator, AndOperator, OrOperator, Rule, KnowledgeIsland


class TestFact:
    """
    Testing Fact class  
    """

    def test_instantiation(self):
        """
        Test the constructor
        """
        Fact('test1', 1.0)
        Fact('test2', 0.5, 0.5)


class TestNotOperator:
    """
    Testing NotOperator class  
    """

    def test_instantiation(self):
        """
        Test the constructor
        """
        NotOperator(Fact('test1', 1.0))


class TestOrOperator:
    """
    Testing OrOperator class  
    """

    def test_instantiation(self):
        """
        Test the constructor
        """
        OrOperator(Fact('test1', 1.0),Fact('test2', 0.5, 0.5))


class TestAndOperator:
    """
    Testing AndOperator class  
    """

    def test_instantiation(self):
        """
        Test the constructor
        """
        AndOperator(Fact('test1', 1.0),Fact('test2', 0.5, 0.5))


class TestRule:
    """
    Testing Rule class  
    """

    def test_instantiation(self):
        """
        Test the constructor
        """
        Rule(Fact('test1', 1.0),Fact('test2', 0.5), 0.675)


class TestKnowledgeIsland:
    """
    Testing KnowledgeIsland class  
    """

    def test_instantiation(self):
        """
        Test the constructor
        """
        KnowledgeIsland([
            Rule(Fact('test1', 1.0),Fact('test2', 0.5), 0.675),
            Rule(NotOperator(Fact('test3', 0.3)),Fact('test4', 0.86), 0.345)
        ])
        