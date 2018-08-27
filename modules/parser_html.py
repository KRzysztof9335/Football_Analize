# Standard modules
import os
import re
import sys

# User defined modules
sys.path.insert(0, '{0}/modules'.format(os.environ['REPO_ROOT']))
import configuration as CFG

def parser_html_get_table_columns(table_row):
	return [column.strip() for column in re.findall(CFG.rx_html_table_column, table_row)]

def parser_html_get_table_rows_columns(rows):
	return [parser_html_get_table_columns(row) for row in rows]

def parser_html_get_table_rows(table):
	return [row for row in re.findall(CFG.rx_html_table_row, table)]

def parser_html_get_table_content(raw_table):
	raw_table_rows = parser_html_get_table_rows(raw_table)
	raw_table_rows_columns = parser_html_get_table_rows_columns(raw_table_rows)
	return raw_table_rows_columns

def parser_html_get_round_all_html_tables(infobank_round, string_input):
	return re.findall(CFG.rx_html_table, string_input)

def parser_html_remove_all_comments(string_input):
	return re.sub(CFG.rx_html_comment, '', string_input)

def parser_html_get_round_results(infobank_round, string_input):
	html = parser_html_remove_all_comments(string_input)
	all_html_tables = parser_html_get_round_all_html_tables(infobank_round, html) # Return list of found tables
	raw_round_table = parser_html_get_table_content(all_html_tables[3])
	raw_round_matches = parser_html_get_table_content(all_html_tables[1])


	for r in raw_round_matches:
		print("\n".join(r))
	# Here should be continuation of code...
	sys.exit(1)
