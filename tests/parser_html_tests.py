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

if __name__ == '__main__':
	CFG.init()
	unittest.main()
