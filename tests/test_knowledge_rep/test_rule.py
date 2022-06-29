# -*- coding : utf-8 -*-

"""
Test for Rule
"""


from src.knowledge_rep.lefthandside.fact import Fact
from src.knowledge_rep.rule import Rule


class TestRule:
    """
    Testing Rule class  
    """

    def test_instantiation(self):
        """
        Test the constructor
        """
        Rule(Fact('test1', 1.0),Fact('test2', 0.5), 0.675)