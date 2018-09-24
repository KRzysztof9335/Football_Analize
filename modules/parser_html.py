"""
This module is responsible for any kind of html parses
"""
# Standard modules
import os
import re
import sys

# User defined modules
sys.path.insert(0, '{0}/modules'.format(os.environ['REPO_ROOT']))
import modules.configuration as CFG

def get_table_columns(table_row):
    """
    In - string - representing table row
    Out - array of strings - representing each column in row
    Note: column must be stripped since it contains some leading and trailing whitespaces
    """
    return [column.strip() for column in re.findall(CFG.RX_HTML_TABLE_COLUMN, table_row)]





def get_table_rows_columns(rows):
    """
    In - array of string representing row
    Out - array of arrays representing row each column
    """
    return [get_table_columns(row) for row in rows]





def get_table_rows(table):
    """
    In - string - html table
    Out - array of strings representing row
    """
    return [row for row in re.findall(CFG.RX_HTML_TABLE_ROW, table)]





def get_table_content(raw_table):
    """
    In - string - html table
    Out - array of arrays representing row each column
    """
    raw_table_rows = get_table_rows(raw_table)
    raw_table_rows_columns = get_table_rows_columns(raw_table_rows)
    return raw_table_rows_columns





def get_round_all_html_tables(html_document):
    """
    In - string - html document
    Out - array of string representing html html table
    """
    return re.findall(CFG.RX_HTML_TABLE, html_document)





def remove_all_comments(string_input):
    """
    In - string - html document
    Out - string - html document without comments
    """
    return re.sub(CFG.RX_HTML_COMMENT, '', string_input)





def get_team_from_hyperlink(hyperlink):
    """
    In - string - represents team in results e.ga '<a href="/teams/team-a/" title="TA">team-a</a>'
    Out - string - represents team e.g. team-a
    Note: previously here was try block
    """
    return re.search(CFG.RX_HTML_HYPERLINK_TEAM, hyperlink).group(1)




def wf_get_round_match_report_link(hyperlink):
    """
    In - string - representing match report part of url
    Out - string - reprsenting correct match report url
    """
    return CFG.WF_URL_ROOT + re.search(CFG.RX_HTML_HYPERLINK, hyperlink).group(1)





def wf_get_round_match_scores(hyperlink):
    """
    In - string - hyperlink with score, e.g <a href="/report/report-1" title="TI2">6:0 (2:0) </a>
    Out - string - htft
        - string - atht
        - string - htht
        - string - atht
    Function has try block since it may happen sth will go wrong
    """
    results = re.search(CFG.RX_HTML_MATCH_SCORES, hyperlink)
    return (results.group(1), results.group(2), results.group(3), results.group(4))





def get_table_goals_shot_lost(goals_input):
    """
    In - string - represents table goals shot, lost e.g. 32:23
    Out - string - goals shot
        - string - goals lost
    """
    goals = re.search(CFG.RX_WF_GOALS, goals_input)
    return goals.group(1), goals.group(2)





def wf_sanitize_round_match(raw_round_match, first_round_match_date):
    """
    In - array of round match stats
       - string - day of previous match (sometimes it was skipped)
    Out - array of strings representing sanitized round match stats
    """
    if raw_round_match[0]:
        match_date = raw_round_match[0]
    else:
        match_date = first_round_match_date
    match_hour = raw_round_match[1]
    match_home_team = get_team_from_hyperlink(raw_round_match[2])
    match_away_team = get_team_from_hyperlink(raw_round_match[4])
    match_report = wf_get_round_match_report_link(raw_round_match[5])
    htft, atft, htht, atht = wf_get_round_match_scores(raw_round_match[5])
    match_stats = [match_date, match_hour, match_home_team, match_away_team, \
                   htft, atft, htht, atht, match_report]
    if all(match_stats):
        return match_stats
    else:
        CFG.LOGGER.critical("CRITICAL: No round matches data - program - stop")
        sys.exit(1)




def wf_sanitize_round_matches(raw_round_matches):
    """
    htft = home team full time
    htht = home team half time
    atft = away team full time
    atht = away team half time
    Output: list of list e.g [['date', 'hour', 'hometeamA', 'awayteamB', \
                               'htft', 'atft', 'htft', 'atht', detail_raport],
                              ['date', 'hour', 'hometeamC', 'awayteamD', \
                               'htft', 'atft', 'htft', 'atht', detail_raport]]
    """
    sanitized_matches = []
    first_round_match_date = raw_round_matches[0][0]
    for raw_round_matches in raw_round_matches:
        sanitized_matches.append(wf_sanitize_round_match(raw_round_matches, first_round_match_date))
    return sanitized_matches




def wf_sanitize_round_table_row(round_table_row, place_in_table):
    """
    In - array of table row strings
       - place in table (sometimes it was skipped)
    Out - array of sanitized table row content
    """
    if '&nbsp' not in round_table_row[0]:
        place = round_table_row[0]
    else:
        place = str(int(place_in_table) + 1)
    team = get_team_from_hyperlink(round_table_row[2])
    matches_played = round_table_row[3]
    matches_won = round_table_row[4]
    matches_draw = round_table_row[5]
    matches_lost = round_table_row[6]
    goals_shot, goals_lost = get_table_goals_shot_lost(round_table_row[7])
    goals_diff = round_table_row[8]
    points = round_table_row[9]
    return [place, team, matches_played, matches_won, matches_draw, matches_lost, \
            goals_shot, goals_lost, goals_diff, points], place





def wf_sanitize_round_table(raw_round_table_rows):
    """
    In - array of rows representing round table (without table header)
    Out - array of strings of round table row (place, team, matches played, lost, won etc)
    Functions ruturn round table sanitized (no html content)
    """
    sanitized_round_table = []
    place_in_table = '1'
    for round_table_row in raw_round_table_rows:
        sanitized_round_table_row, place_in_table = wf_sanitize_round_table_row(round_table_row, \
                                                                                place_in_table)
        sanitized_round_table.append(sanitized_round_table_row)
    return sanitized_round_table





def wf_get_round_results(wf_raw_round_page):
    """
    In - string - representing infobank round
         string - downloaded from worldfootbal results from one round
    Out - array of strings of round table row (place, team, matches played, lost, won etc)
        - array of strings of match info (date, time, team1, team2, htft, atft, htht, atht, details)
    Function invokes other functions which parse html to get round_table and round_matches
    """
    html = remove_all_comments(wf_raw_round_page)
    all_html_tables = get_round_all_html_tables(html)

    raw_round_table = get_table_content(all_html_tables[3])
    wf_round_table = wf_sanitize_round_table(raw_round_table[1:])

    raw_round_matches = get_table_content(all_html_tables[1])
    round_matches = wf_sanitize_round_matches(raw_round_matches)

    return wf_round_table, round_matches
