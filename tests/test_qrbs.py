# -*- coding : utf-8 -*-

"""
Test for KnowledgeIsland
"""


from neasqc_qrbs.qrbs import QRBS


class TestQRBS:
    """
    Testing QRBS class  
    """

    def test_qrbs(self):
        """
        Test the constructor
        """
        system_a = QRBS()
        system_b = QRBS()
        
        assert system_a == system_b
        