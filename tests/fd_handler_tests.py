#!/usr/bin/python3

# Standard modules
from collections import OrderedDict

import os
import sys
import unittest

# User defined modules
sys.path.insert(0, '{0}'.format(os.environ['REPO_ROOT']))
sys.path.insert(0, '{0}/modules'.format(os.environ['REPO_ROOT']))

import modules.configuration as CFG
import modules.fd_handler as FDH


class function_fd_append_matches_stats(unittest.TestCase):

    def setUp(self):
        self.fd_excel_positions = OrderedDict([('HS', 4), ('AS', 5), \
                                               ('HR', 6), ('AR', 7)])
        self.fd_excel_row_columns = [['D1', '24/08/2018', 'H1', 'A1', '32', '13', '31', '0'],\
                                     ['D1', '25/08/2018', 'H2', 'A2', '23', '33', '1', '1']]
        self.wf_round_matches = [['24/08/2018', '19:30', 'H1', 'A1', '3', '1', '1', '0', 'l1'],\
                                 ['25/08/2018', '19:30', 'H2', 'A2', '2', '1', '0', '0', 'l2']]
        self.expected_correct = [['24/08/2018', '19:30', 'H1', 'A1', '3', '1', '1', '0', 'l1', '32', '13', '31', '0'],\
                                 ['25/08/2018', '19:30', 'H2', 'A2', '2', '1', '0', '0', 'l2', '23', '33', '1', '1']]
        
    def test_expected_correct(self):
        self.assertEqual(FDH.fd_append_matches_stats(self.fd_excel_positions, \
                                                     self.fd_excel_row_columns, \
                                                     self.wf_round_matches), self.expected_correct)

if __name__ == '__main__':
    CFG.init()
    CFG.LOGGER.setLevel(CFG.logging.CRITICAL)
    unittest.main()