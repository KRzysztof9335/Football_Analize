# Standard modules
import os
import re
import sys

# User defined modules
sys.path.insert(0, '{0}/modules'.format(os.environ['REPO_ROOT']))
import modules.configuration as CFG

def parser_html_get_table_columns(table_row):
	return [column.strip() for column in re.findall(CFG.RX_HTML_TABLE_COLUMN, table_row)]

def parser_html_get_table_rows_columns(rows):
	return [parser_html_get_table_columns(row) for row in rows]

def parser_html_get_table_rows(table):
	return [row for row in re.findall(CFG.RX_HTML_TABLE_ROW, table)]

def parser_html_get_table_content(raw_table):
	raw_table_rows = parser_html_get_table_rows(raw_table)
	raw_table_rows_columns = parser_html_get_table_rows_columns(raw_table_rows)
	return raw_table_rows_columns

def parser_html_get_round_all_html_tables(infobank_round, string_input):
	return re.findall(CFG.RX_HTML_TABLE, string_input)

def parser_html_remove_all_comments(string_input):
	return re.sub(CFG.RX_HTML_COMMENT, '', string_input)

def parser_html_get_team_from_hyperlink(hyperlink):
	try: return re.search(CFG.RX_HTML_HYPERLINK_TEAM, hyperlink).group(1)
	except: return None

def parser_html_wf_get_round_match_report_link(hyperlink):
	try: return CFG.WF_URL_ROOT + re.search(CFG.RX_HTML_HYPERLINK, hyperlink).group(1)
	except: None

def parser_html_wf_get_round_match_scores(hyperlink):
	try: 
		results = re.search(CFG.RX_HTML_MATCH_SCORES, hyperlink)
		return (results.group(1), results.group(2), results.group(3), results.group(4))
	except: return None 

def parser_html_wf_sanitize_round_match(raw_round_match, first_round_match_date):
	if raw_round_match[0]: match_date = raw_round_match[0]
	else: match_date = first_round_match_date
	match_hour = raw_round_match[1]
	match_home_team = parser_html_get_team_from_hyperlink(raw_round_match[2])
	match_away_team = parser_html_get_team_from_hyperlink(raw_round_match[4])
	match_report = parser_html_wf_get_round_match_report_link(raw_round_match[5])
	HTFT, ATFT, HTHT, ATHT = parser_html_wf_get_round_match_scores(raw_round_match[5])
	match_stats = [match_date, match_hour, match_home_team, match_away_team, HTFT, ATFT, HTHT, ATHT, match_report]
	if all(match_stats): return match_stats
	else:
		CFG.LOGGER.critical("CRITICAL: No round matches data - program - stop")
		sys.exit(1)

def parser_html_wf_sanitize_round_matches(raw_round_matches):
	"""
	HTFT = home team full time
	HTHT = home team half time
	ATFT = away team full time
	ATHT = away team half time
	Output: list of list e.g [['date', 'hour', 'hometeamA', 'awayteamB', 'HTFT', 'ATFT', 'HTFT', 'ATHT', detail_raport],
							  ['date', 'hour', 'hometeamC', 'awayteamD', 'HTFT', 'ATFT', 'HTFT', 'ATHT', detail_raport]]
	"""
	sanitized_matches = []
	first_round_match_date = raw_round_matches[0][0]
	for raw_round_matches in raw_round_matches:
		sanitized_matches.append(parser_html_wf_sanitize_round_match(raw_round_matches, first_round_match_date))
	return sanitized_matches

def parser_html_get_goals(goals_input):
	rx_get_goals = re.compile('(\d+):(\d+)')
	goals = re.search(rx_get_goals, goals_input)
	return goals.group(1), goals.group(2)

def parser_html_wf_sanitize_round_table_row(round_table_row, place_in_table):
	if not '&nbsp' in round_table_row[0]: place = round_table_row[0]
	else: place = str(int(place_in_table) + 1)
	team  = parser_html_get_team_from_hyperlink(round_table_row[2])
	matches_played = round_table_row[3]
	matches_won = round_table_row[4]
	matches_draw = round_table_row[5]
	matches_lost = round_table_row[6]
	goals_shot, goals_lost = parser_html_get_goals(round_table_row[7])
	goals_diff = round_table_row[8]
	points = round_table_row[9]
	return [place, team, matches_played, matches_won, matches_draw, matches_lost, goals_shot, goals_lost, goals_diff, points], place

def parser_html_wf_sanitize_round_table(raw_round_table_rows):
	sanitized_round_table = []
	place_in_table = '1'
	for round_table_row in raw_round_table_rows:
		sanitized_round_table_row, place_in_table = parser_html_wf_sanitize_round_table_row(round_table_row, place_in_table)
		sanitized_round_table.append(sanitized_round_table_row)
	return sanitized_round_table

def parser_html_get_round_results(infobank_round, string_input):
	html = parser_html_remove_all_comments(string_input)
	all_html_tables = parser_html_get_round_all_html_tables(infobank_round, html) # Return list of found tables

	raw_round_table = parser_html_get_table_content(all_html_tables[3])
	wf_round_table = parser_html_wf_sanitize_round_table(raw_round_table[1:])

	raw_round_matches = parser_html_get_table_content(all_html_tables[1])
	round_matches = parser_html_wf_sanitize_round_matches(raw_round_matches)

	return wf_round_table, round_matches
