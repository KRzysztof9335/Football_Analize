#!/usr/bin/python3

# Standard modules
import os
import sys
import unittest

# User defined modules
sys.path.insert(0, '{0}'.format(os.environ['REPO_ROOT']))
sys.path.insert(0, '{0}/modules'.format(os.environ['REPO_ROOT']))

import modules.configuration as CFG
import modules.common as CMN

class function_translate(unittest.TestCase):
    
    def setUp(self):
        self.dict = {"ABC":"CCC",
                     "ZZZ":"XXX",
                     "M'glad":"M_glad"}
    def test_oneline(self):
        self.assertEqual(CMN.translate("ABC", self.dict), "CCC")
        self.assertEqual(CMN.translate("ABCZZZ", self.dict), "CCCXXX")
        
    def test_quote_mark(self):
        self.assertEqual(CMN.translate("M'glad", self.dict), "M_glad")
        
    def test_no_translate(self):
        self.assertEqual(CMN.translate("AC", self.dict), "AC")
    
    def test_multiline(self):
        self.assertEqual(CMN.translate("ABC\nABC", self.dict), "CCC\nCCC")
        self.assertEqual(CMN.translate("ZZZABC\nABCZZZ", self.dict), "XXXCCC\nCCCXXX")


if __name__ == '__main__':
    CFG.init()
    CFG.LOGGER.setLevel(CFG.logging.CRITICAL)
    unittest.main()