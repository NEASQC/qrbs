# -*- coding : utf-8 -*-

"""
Test for KnowledgeIsland
"""


from src.knowledge_rep.lefthandside.fact import Fact
from src.knowledge_rep.lefthandside.notoperator import NotOperator
from src.knowledge_rep.rule import Rule
from src.knowledge_rep.knowledgeisland import KnowledgeIsland


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