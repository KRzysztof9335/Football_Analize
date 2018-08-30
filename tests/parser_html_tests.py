#!/usr/bin/python3

# Standard modules
import os
import sys
import unittest

# User defined modules
sys.path.insert(0, '{0}'.format(os.environ['REPO_ROOT']))
sys.path.insert(0, '{0}/modules'.format(os.environ['REPO_ROOT']))

import common as CMN
import configuration as CFG
import parser_html as PH

EXAMPLES_ROOT = os.path.join(os.environ['REPO_ROOT'],'tests/examples')


class function_parser_html_remove_comments(unittest.TestCase):

	def setUp(self):
		self.raw_html_1 = CMN.common_get_file_content(os.path.join(EXAMPLES_ROOT, 'ut_parser_html_example_comments.html'))

	def test_removal_of_existing_comments(self):
		self.assertEqual(PH.parser_html_remove_all_comments(self.raw_html_1,),'AABB\n\n\nDD\n')

class function_parser_html_get_table_rows(unittest.TestCase):

	def setUp(self):
		self.raw_html_1 = CMN.common_get_file_content(os.path.join(EXAMPLES_ROOT, 'ut_parser_html_example_table.html'))

	def test_correct_rows(self):
		self.assertEqual(PH.parser_html_get_table_rows(self.raw_html_1), ['\n\t\t\tR1\n\t\t', 'R2', '\n\tR3'])


class fnction_function_parser_html_get_table_columns(unittest.TestCase):

	def setUp(self):
		self.raw_html_1 = CMN.common_get_file_content(os.path.join(EXAMPLES_ROOT, 'ut_parser_html_example_row.html'))

	def test_correct_columns(self):
		self.assertEqual(PH.parser_html_get_table_columns(self.raw_html_1), ['26/08/2016', '<a href="Link" title="Title">Title</a>', '-', '<a href="Report" title="Report">6:0 (2:0) </a>'])

class fnction_parser_html_get_table_rows_columns(unittest.TestCase):

	def test_correct_columns(self):
		self.assertEqual(PH.parser_html_get_table_rows_columns(['<td d>C11</td>\t\n<td d>C12</td>', '<td d>C21</td>\t\n<td d>C22</td>']), [['C11','C12'], ['C21','C22']])

class function_parser_html_sanitize_round_matches(unittest.TestCase):

	def setUp(self):
		self.raw_round_matches_in = [['26/08/2016', '19:30', '<a href="/teams/team-a/" title="TA">team-a</a>', '-', '<a href="/teams/team-b/" title="TB">team-b</a>', '<a href="/report/report-1" title="TI2">6:0 (2:0) </a>', '', ''],
							   	     ['', '14:30', '<a href="/teams/team-c/" title="TC">team-c</a>', '-', '<a href="/teams/team-d/" title="TB">team-d</a>', '<a href="/report/report-2" title="TI2">2:2 (2:1) </a>', '', '']]
		self.raw_round_matches_out = [['26/08/2016', '19:30', 'team-a', 'team-b', '6', '0', '2', '0', CFG.CONFIG_MATCHES_INFO_URL+'/report/report-1'],
							   	      ['26/08/2016', '14:30', 'team-c', 'team-d', '2', '2', '2', '1', CFG.CONFIG_MATCHES_INFO_URL+'/report/report-2']]
		# ['date', 'hour', 'hometeamA', 'awayteamB', HTFT, 'ATFT', 'HTFT', 'ATHT', detail_raport],


	def test_correct_input(self):
		self.assertEqual(PH.parser_html_sanitize_round_matches(self.raw_round_matches_in), self.raw_round_matches_out)


class function_parser_html_sanitize_round_match(unittest.TestCase):

	def setUp(self):
		self.raw_round_match_in = ['26/08/2016', '19:30', '<a href="/teams/team-a/" title="TA">team-a</a>', '-', '<a href="/teams/team-b/" title="TB">team-b</a>', '<a href="/report/report-1" title="TI2">6:0 (2:0) </a>', '', '']
		self.raw_round_match_out =  ['26/08/2016', '19:30', 'team-a', 'team-b', '6', '0', '2', '0', CFG.CONFIG_MATCHES_INFO_URL+'/report/report-1']

	def test_correct(self):
		self.assertEqual(PH.parser_html_sanitize_round_match(self.raw_round_match_in, '26/08/2016'), self.raw_round_match_out)

class function_parser_html_get_team_from_hyperlink(unittest.TestCase):

	def test_correct(self):
		self.assertEqual(PH.parser_html_get_team_from_hyperlink('<a href="/teams/team-a/" title="TA">team-a</a>'), 'team-a')
		self.assertEqual(PH.parser_html_get_team_from_hyperlink('<a href="/teams/teamA/" title="TA">teamA</a>'), 'teamA')
		self.assertEqual(PH.parser_html_get_team_from_hyperlink('<a href="/teams/team_a/" title="TA">team_a</a>'), 'team_a')

	def test_incorrect(self):
		self.assertEqual(PH.parser_html_get_team_from_hyperlink('<a href="/tems/team-a/" title="TA">team-a</a>'), None)

class function_parser_html_get_round_match_report_link(unittest.TestCase):

	def test_correct(self):
		self.assertEqual(PH.parser_html_get_round_match_report_link('<a href="/report/report-1" title="TI2">6:0 (2:0) </a>)'), CFG.CONFIG_MATCHES_INFO_URL+'/report/report-1')

	def test_incorrect(self):
		self.assertEqual(PH.parser_html_get_round_match_report_link('<a href="report/report-1" title="TI2">6:0 (2:0) </a>)'), None)


class function_parser_html_get_round_match_score(unittest.TestCase):

	def test_correct(self):
		self.assertEqual(PH.parser_html_get_round_match_scores('<a href="/report/report-1" title="TI2">6:0 (2:0) </a>'), ('6', '0', '2', '0'))
		self.assertEqual(PH.parser_html_get_round_match_scores('<a href="/report/report-1" title="TI2">16:15 (11:14) </a>'), ('16', '15', '11', '14'))









if __name__ == '__main__':
	CFG.init()
	unittest.main()
