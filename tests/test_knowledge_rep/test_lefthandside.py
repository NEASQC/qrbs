# -*- coding : utf-8 -*-

"""
Test for LeftHandSide elements
"""

from src.knowledge_rep.lefthandside.andoperator import AndOperator
from src.knowledge_rep.lefthandside.fact import Fact
from src.knowledge_rep.lefthandside.notoperator import NotOperator
from src.knowledge_rep.lefthandside.oroperator import OrOperator


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
        