#!/usr/bin/python3

# Standard modules
import os
import sys
import unittest

# User defined modules
sys.path.insert(0, '{0}'.format(os.environ['REPO_ROOT']))
sys.path.insert(0, '{0}/modules'.format(os.environ['REPO_ROOT']))

import modules.common as CMN
import modules.configuration as CFG
import modules.parser_html as PH

EXAMPLES_ROOT = os.path.join(os.environ['REPO_ROOT'],'tests/examples')


class function_remove_comments(unittest.TestCase):

    def setUp(self):
        self.raw_html_1 = CMN.common_get_file_content(os.path.join(EXAMPLES_ROOT, 'ut_parser_html_example_comments.html'))

    def test_removal_of_existing_comments(self):
        self.assertEqual(PH.remove_all_comments(self.raw_html_1,),'AABB\n\n\nDD\n')

class function_get_table_rows(unittest.TestCase):

    def setUp(self):
        self.raw_html_1 = CMN.common_get_file_content(os.path.join(EXAMPLES_ROOT, 'ut_parser_html_example_table.html'))

    def test_correct_rows(self):
        self.assertEqual(PH.get_table_rows(self.raw_html_1), ['\n\t\t\tR1\n\t\t', 'R2', '\n\tR3'])


class fnction_function_get_table_columns(unittest.TestCase):

    def setUp(self):
        self.raw_html_1 = CMN.common_get_file_content(os.path.join(EXAMPLES_ROOT, 'ut_parser_html_example_row.html'))

    def test_correct_columns(self):
        self.assertEqual(PH.get_table_columns(self.raw_html_1), ['26/08/2016', '<a href="Link" title="Title">Title</a>', '-', '<a href="Report" title="Report">6:0 (2:0) </a>'])

class fnction_get_table_rows_columns(unittest.TestCase):

    def test_correct_columns(self):
        self.assertEqual(PH.get_table_rows_columns(['<td d>C11</td>\t\n<td d>C12</td>', '<td d>C21</td>\t\n<td d>C22</td>']), [['C11','C12'], ['C21','C22']])

class function_wf_sanitize_round_matches(unittest.TestCase):

    def setUp(self):
        self.raw_round_matches_in = [['26/08/2016', '19:30', '<a href="/teams/team-a/" title="TA">team-a</a>', '-', '<a href="/teams/team-b/" title="TB">team-b</a>', '<a href="/report/report-1" title="TI2">6:0 (2:0) </a>', '', ''],
                                        ['', '14:30', '<a href="/teams/team-c/" title="TC">team-c</a>', '-', '<a href="/teams/team-d/" title="TB">team-d</a>', '<a href="/report/report-2" title="TI2">2:2 (2:1) </a>', '', '']]
        self.raw_round_matches_out = [['26/08/2016', '19:30', 'team-a', 'team-b', '6', '0', '2', '0', CFG.WF_URL_ROOT+'/report/report-1'],
                                         ['26/08/2016', '14:30', 'team-c', 'team-d', '2', '2', '2', '1', CFG.WF_URL_ROOT+'/report/report-2']]
        # ['date', 'hour', 'hometeamA', 'awayteamB', HTFT, 'ATFT', 'HTFT', 'ATHT', detail_raport],


    def test_correct_input(self):
        self.assertEqual(PH.wf_sanitize_round_matches(self.raw_round_matches_in), self.raw_round_matches_out)

class function_wf_sanitize_round_match(unittest.TestCase):

    def setUp(self):
        self.raw_round_match_in = ['26/08/2016', '19:30', '<a href="/teams/team-a/" title="TA">team-a</a>', '-', '<a href="/teams/team-b/" title="TB">team-b</a>', '<a href="/report/report-1" title="TI2">6:0 (2:0) </a>', '', '']
        self.raw_round_match_out =  ['26/08/2016', '19:30', 'team-a', 'team-b', '6', '0', '2', '0', CFG.WF_URL_ROOT+'/report/report-1']

    def test_correct(self):
        self.assertEqual(PH.wf_sanitize_round_match(self.raw_round_match_in, '26/08/2016'), self.raw_round_match_out)

class function_get_team_from_hyperlink(unittest.TestCase):

    def test_correct(self):
        self.assertEqual(PH.get_team_from_hyperlink('<a href="/teams/team-a/" title="TA">team-a</a>'), 'team-a')
        self.assertEqual(PH.get_team_from_hyperlink('<a href="/teams/teamA/" title="TA">teamA</a>'), 'teamA')
        self.assertEqual(PH.get_team_from_hyperlink('<a href="/teams/team_a/" title="TA">team_a</a>'), 'team_a')


class function_wf_get_round_match_report_link(unittest.TestCase):

    def test_correct(self):
        self.assertEqual(PH.wf_get_round_match_report_link('<a href="/report/report-1" title="TI2">6:0 (2:0) </a>)'), CFG.WF_URL_ROOT+'/report/report-1')


class function_get_round_match_score(unittest.TestCase):

    def test_correct(self):
        self.assertEqual(PH.wf_get_round_match_scores('<a href="/report/report-1" title="TI2">6:0 (2:0) </a>'), ('6', '0', '2', '0'))
        self.assertEqual(PH.wf_get_round_match_scores('<a href="/report/report-1" title="TI2">16:15 (11:14) </a>'), ('16', '15', '11', '14'))

class function_wf_sanitize_round_table_row(unittest.TestCase):

    def setUp(self):
        self.example_1 = ['1', '<img src="https:22.gif alt="team-a, country" title="team-a, country" />', '<a href="/teams/team-a/" title="team-a">', '1', '1', '0', '0', '6:0', '6', '3']
        self.example_1_out = ['1', 'team-a', '1', '1', '0', '0', '6', '0', '6', '3']

        self.example_2 = ['&nbsp', '<img src="https:22.gif alt="team-b, country" title="team-b, country" />', '<a href="/teams/team-b/" title="team-a">', '1', '0', '0', '1', '0:6', '-6', '0']
        self.example_2_out = ['16', 'team-b', '1', '0', '0', '1', '0', '6', '-6', '0']

    def test_correct(self):
        self.assertEqual(PH.wf_sanitize_round_table_row(self.example_1, 1), (self.example_1_out, '1'))
        self.assertEqual(PH.wf_sanitize_round_table_row(self.example_2, 15), (self.example_2_out, '16'))

class function_wf_sanitize_round_table(unittest.TestCase):

    def setUp(self):
        self.round_table_rows_in = [['1', '<img src="https:22.gif alt="team-a, country" title="team-a, country" />', '<a href="/teams/team-a/" title="team-a">', '1', '1', '0', '0', '6:0', '6', '3'],
                                    ['&nbsp', '<img src="https:22.gif alt="team-b, country" title="team-b, country" />', '<a href="/teams/team-b/" title="team-a">', '1', '0', '0', '1', '0:6', '-6', '0']]
        self.round_table_rows_out = [['1', 'team-a', '1', '1', '0', '0', '6', '0', '6', '3'],
                                     ['2', 'team-b', '1', '0', '0', '1', '0', '6', '-6', '0']]

    def test_correct(self):
        self.assertEqual(PH.wf_sanitize_round_table(self.round_table_rows_in), self.round_table_rows_out)

        
class function_fd_get_stats_link(unittest.TestCase):
    
    
    def setUp(self):
        self.fd_example = """<I>Season 2018/2019</I><BR>
                          <IMG SRC="Excel.gif" <A HREF="mmz4281/1819/D1.csv">Bundesliga 1</A><BR>
                          <IMG SRC="Excel.gif" <A HREF="mmz4281/1819/D2.csv">Bundesliga 2</A><BR><BR>

                          <I>Season 2017/2018</I><BR>
                          <IMG SRC="Excel.gif" <A HREF="mmz4281/1718/D1.csv">Bundesliga 1</A><BR>
                          <IMG SRC="Excel.gif" <A HREF="mmz4281/1718/D2.csv">Bundesliga 2</A><BR><BR>"""
        self.country_league = CFG.CountryLeague('C1', 'L1', 2, 3, 'LName', 'D1', 'C11')

    def test_correct(self):
        self.assertEqual(PH.fd_get_stats_link(self.country_league, '2018', self.fd_example), CFG.FD_URL_ROOT + '/mmz4281/1819/D1.csv')

if __name__ == '__main__':
    CFG.init()
    unittest.main()
