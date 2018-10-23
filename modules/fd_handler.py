"""
This module is responsible for any kind of football data excel parsing actions
"""
# Standard modules
from collections import OrderedDict

import os
import sys


# User defined modules
sys.path.insert(0, '{0}/modules'.format(os.environ['REPO_ROOT']))
import modules.configuration as CFG
import modules.common as CMN
import modules.parser_html as PH
import modules.webhandler as WH


def fd_excel_download(country_league, season, fd_excel_path):
    """
    In - obj - countryleague
       - int - season - year for which excel will be downloaded
       - string - path where excel will be saved
    Out - none
    Function saves football data excel on hard drive
    """
    fd_res = WH.get_webpage_content(CFG.FD_URL_COUNTRY.format(country_league.fd_url_name))
    fd_excel_link = PH.fd_get_stats_link(country_league, season, fd_res)
    WH.download_file_and_save(fd_excel_link, fd_excel_path)




def fd_excel_translate_team_names(country_league, fd_excel_path):
    """
    In - string - full path to excel with football data
    Out - string - excel with names compliant with wordlfootball
    """
    league_name = country_league.league_name
    raw_excel_content = CMN.common_get_file_content(fd_excel_path)
    if league_name == "bundesliga_1":
        return CMN.translate(raw_excel_content, CFG.FD_TO_WF_BUNDESLIGA_1)
    else:
        CFG.LOGGER.critical("Translation for %s failed", league_name)
        sys.exit(1)



def fd_excel_get_header(fd_excel):
    """
    In - string - excel with football data
    Out - list - of columns headers
    """
    return fd_excel.split("\n")[0].split(",")




def fd_excel_get_rows_columns(fd_excel):
    """
    In - string - excel with football data
    Out - list of lists - containing match statisitcs
    """
    rows = []
    rows_splitted = fd_excel.split("\n")
    for row in rows_splitted[1:]:
        rows.append(row.split(","))
    return rows




def fd_excel_get_positions(fd_excel_header, fd_columns):
    """
    In - list - of columns headers
       - list - of columns to be searched
    Out - dictionary - fd_columns mapped with indexes where they are
    """
    positions = OrderedDict()
    for fd_column in fd_columns:
        positions[fd_column] = fd_excel_header.index(fd_column)
    return positions




def fd_get_excel_row_stats(fd_excel_positions, fd_excel_row):
    """
    In - dict - dictionary with interest data with position
       - list - one excel row
    Out - list - with reqeusted statistics for the particular excel row
    """
    fd_stats_list = []
    for key, value in fd_excel_positions.items():
        fd_stats_list.append(fd_excel_row[value])
    return fd_stats_list




def fd_get_match_stats_to_extend(wf_round_match, fd_excel_row_columns, fd_excel_positions):
    """
    In - list - of match statistics gathered from worldfootball
       - list of lists - of football data excel
       - dict - dictionary with interest data with position
    Out - list of stats for match which will be appended to final match stats
    """
    match_home_team = str(wf_round_match[2])
    match_away_team = str(wf_round_match[3])
    for fd_excel_row in fd_excel_row_columns:
        try:
            if (match_home_team in fd_excel_row[2]) and (match_away_team in fd_excel_row[3]):
                return fd_get_excel_row_stats(fd_excel_positions, fd_excel_row)
        except IndexError:
            CFG.LOGGER.critical("Adding fd data for %s-%s failed - wrongly converted?", match_home_team, \
                                match_away_team)
            sys.exit(1)




def fd_append_matches_stats(fd_excel_positions, fd_excel_row_columns, wf_round_matches):
    """
    In - dict - fd excel columns with positions
       - list of lists - contating each excel row with match stats
       - list of lists - containing statistics got from worldfootball
    Out - list of list - contating statistics from wf and fd
    """
    round_matches = []
    for wf_round_match in wf_round_matches:
        list_to_extend = fd_get_match_stats_to_extend(wf_round_match, fd_excel_row_columns, \
                                                      fd_excel_positions)
        wf_round_match.extend(list_to_extend)
        round_matches.append(wf_round_match)
    return round_matches
