# -*- coding : utf-8 -*

from src.knowledge_rep.buildable import Buildable
from qat.lang.AQASM.routines import QRoutine

class KnowledgeIsland(Buildable):
    """Class representing a Knowledge Island.
    
    A Knowledge Island is a set of rules that conform the inferential reasoning towards a hypothesis.

    Attributes:
        rules (List[:obj:`Rule`]): Set of rules that conform the knowledge island.
    """

    def __init__(self, rules) -> None:
        super().__init__()
        self.rules = rules

    def build(self) -> QRoutine:
        return super().build()