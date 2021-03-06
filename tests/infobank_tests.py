#!/usr/bin/python3

# Standard modules
import os
import sys
import unittest

# User defined modules
sys.path.insert(0, '{0}'.format(os.environ['REPO_ROOT']))
sys.path.insert(0, '{0}/modules'.format(os.environ['REPO_ROOT']))

import modules.configuration as CFG
import modules.infobank as IB
        


class function_create_country_league_season_round_table(unittest.TestCase):

    def setUp(self):
        self.round_table_in = [['A1', 'A2', 'A3'], ['B1'], ['C1','C2']]
        self.round_table_out = "A1;A2;A3\nB1\nC1;C2"

    def test_correct_in(self):
        self.assertEqual(IB.create_to_write_table(self.round_table_in), self.round_table_out)

class function_create_to_write_matches(unittest.TestCase):

    def setUp(self):
        self.input = [['date', 'hour', 'hometeamA', 'awayteamB', 'HTFT', 'ATFT', 'HTFT', 'ATHT', 'detail_raport'],
                      ['date', 'hour', 'hometeamC', 'awayteamD', 'HTFT', 'ATFT', 'HTFT', 'ATHT', 'detail_raport']]
        self.output_names = ['match_hometeamA_awayteamB.txt', 'match_hometeamC_awayteamD.txt']
        self.output_matches = ['date\nhour\nhometeamA\nawayteamB\nHTFT\nATFT\nHTFT\nATHT\ndetail_raport',
                               'date\nhour\nhometeamC\nawayteamD\nHTFT\nATFT\nHTFT\nATHT\ndetail_raport']

    def test_correct_in(self):
        round_matches, names = IB.create_to_write_matches(self.input)    
        self.assertEqual(round_matches, self.output_matches)
        self.assertEqual(names, self.output_names)


class funtion_verify_round_to_be_created(unittest.TestCase):

    def setUp(self):
        self.round = os.path.join(os.environ['REPO_ROOT'], 'tests/examples/Country/league/2017-2018/round1')
        self.country_league = CFG.CountryLeague('C1', 'L1', 5, 3, 'L11', 'L12', 'U1')

    def test_round_created_previously(self):
        create, content = IB.verify_round_to_be_created(self.country_league, '2001', 9, self.round)
        self.assertEqual(create, "skip_round_creation")


class function_verify_rounds_to_be_created(unittest.TestCase):

    def setUp(self):
        self.country_league = CFG.CountryLeague('C1', 'L1', 5, 3, 'L11', 'L12', 'U1')
        
    def test_year_too_big(self):
        self.assertEqual(IB.verify_rounds_to_be_created(self.country_league, 3000), False)
        self.assertEqual(IB.verify_rounds_to_be_created(self.country_league, CFG.CURRENT_YEAR + 1), False)

    def test_correct_year(self):
        self.assertEqual(IB.verify_rounds_to_be_created(self.country_league, 2000), True)
        self.assertEqual(IB.verify_rounds_to_be_created(self.country_league, CFG.CURRENT_YEAR), True)

if __name__ == '__main__':
    CFG.init()
    CFG.LOGGER.setLevel(CFG.logging.CRITICAL)
    unittest.main()
