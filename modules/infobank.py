"""
This module is responsible for downloading content from web sources, if necessary
parses them, creates data to write and finally writes to disc so it could be used
by neural network to create teach data and learning data.
"""

# Standard modules
import os

# User defined modules
import modules.configuration as CFG
import modules.common as CMN
import modules.parser_html as PH
import modules.webhandler as WH

def create_item(item_to_create):
    """
    In - string - absolute path which will be created
    Functions creates infobank directory
    """
    try:
        os.makedirs(item_to_create)
        CFG.LOGGER.debug("Item: %s success", item_to_create)
    except IOError:
        CFG.LOGGER.debug("Item: %s already exists, skippking creation", item_to_create)




def save_round_table(ib_round, table_to_write):
    """
    In - string - abs path to ib round
       - string - round table
    Function creates file round_table.txt in round directory and writes given table.
    """
    round_table_file = os.path.join(ib_round, "round_table.txt")
    CMN.common_write_to_file(round_table_file, table_to_write)




def save_round_matches(ib_round, round_matches_names, matches_stats):
    """
    In - string - abs path to round
       - list - of file names e.g. match_team1_team2.txt
       - list - of match stats [data, time, scores and so on]
    Out - no out
    Function combines matches_names with matches_stats and invokes function to write results to
    ib_round directory.
    """
    for  match_name, match_stats in zip(round_matches_names, matches_stats):
        match_stats_file = os.path.join(ib_round, match_name)
        CMN.common_write_to_file(match_stats_file, match_stats)




def create_to_write_table(round_table_rows):
    """
    In - array of arrays of round table rows. Table row consists of place, team1, matches_played,
         matches_won, matches_draw, matches_lost, goals_shot, goals_lost, goals_diff, points
    Out - string - table which will be written to file
    Function creates content which will be written to round_table.txt. Content is n-length rows
    table (n - team number). Elements in table separated with ";".
    """
    content_to_write_raw = [";".join(round_table_row) for round_table_row in round_table_rows]
    content_to_write = "\n".join(content_to_write_raw)
    return content_to_write




def create_to_write_matches(round_table_matches):
    """
    In - Array of arrays of matches played in round. Single match played in round consists of
         match_date, match_hour, match_home_team, match_away_team, HTFT, ATFT, HTHT, ATHT,
         match_report, match_statistics, HS, AS, HST, AST, HC, AC, HY, AY, HR, AR. B365H
         B365D, B365A
    Out - array of arrays of matches stats to write
        - array of matches_names
    """
    matches_names = []
    matches_content_to_write = []
    for round_table_match in round_table_matches:
        match_name = 'match_' + round_table_match[2] + '_' + round_table_match[3] + '.txt'
        match_content_to_write = "\n".join(round_table_match)
        matches_names.append(match_name)
        matches_content_to_write.append(match_content_to_write)
    return matches_content_to_write, matches_names





def verify_round_played(ib_round, raw_round_matches):
    """
    In - string - absolute path to /path/to/country/league/season/round
         string - raw round results
    Function checks in 'raw_round_matches' if match was played (the result is not '-:-').
    Returns True if round was played otherwise return false
    """
    if "-:-" in raw_round_matches[0][5]:
        CFG.LOGGER.debug("Round %s is future round - skipping further rounds", ib_round)
        return False
    return True




def verify_round_created(ib_round):
    """
    In - string - absolute path to /path/to/country/league/season/round
    Out - bool - represents if round was created previously
    Function checks if round is created (by checking if round_table.txt exists), if so
    returns True, otherwise returns False. If critical error - ends program
    """

    try:
        if os.stat(os.path.join(ib_round, "round_table.txt")).st_size != 0:
            CFG.LOGGER.debug("Round %s alredy exists - skipping round creation", ib_round)
            return True
    except (IOError, ValueError):
        return False # Catching error when file does not exist





def verify_round_to_be_created(country_league, season, play_round, ib_round):
    """
    This fucntion needs to download web content, so to not necessarily download content
    twice, it will return round content if round happened
    """

    league_name_wf = country_league.league_name_wf

    if verify_round_created(ib_round):
        return "skip_round_creation", ""

    wf_round_url = CFG.WF_URL_ROUND.format(league_name_wf, season, season + 1, play_round)
    wf_raw_round_results = WH.get_webpage_content(wf_round_url)
    all_html_tables = PH.get_round_all_html_tables(wf_raw_round_results)
    raw_round_matches = PH.get_table_content(all_html_tables[1])

    if not verify_round_played(ib_round, raw_round_matches):
        return "skip_all", ""
    return "create_round", wf_raw_round_results





def verify_rounds_to_be_created(country_league, season):
    """
    In - CountryLeague Object, season Int
    Out - Boolean
    Function checks if season integer is not future season
    """
    country = country_league.country
    league = country_league.league_name

    if season > CFG.CURRENT_YEAR:
        CFG.LOGGER.debug("For %s/%s ib stopped - %d is future", country, league, season)
        return False
    return True




def create_country_league_season_round(ib_round, wf_raw_round_results):
    """
    In - string - absolute path to /path/to/country/league/season/round
         string - raw round results from worldfootball
    Out - no out
    Function comissions other functions raw input from worldfootball (from other sources it
    downloads) to parse, prepare content to write and wirtes to file
    """
    create_item(ib_round)
    round_table, round_matches = PH.wf_get_round_results(wf_raw_round_results)

    table_to_write = create_to_write_table(round_table)
    matches_to_write, round_matches_names = create_to_write_matches(round_matches)

    save_round_table(ib_round, table_to_write)
    save_round_matches(ib_round, round_matches_names, matches_to_write)


    
    

def create_country_league_season_rounds(country_league, season):
    """
    In - CountryLeague Object, season Int
    Out - None
    Function invokes function checking what action should be done in context of
    round. If return of invoked function is to create_round, then round is created
    """
    country = country_league.country
    league = country_league.league_name
    play_rounds = list(range(1, country_league.league_rounds + 1))

    for play_round in play_rounds:
        ib_round = os.path.join(CFG.IB_ROOT,
                                country,
                                league,
                                '{0}-{1}'.format(season, season+1),
                                'round_{0}'.format(play_round))
        act, res = verify_round_to_be_created(country_league, season, play_round, ib_round)
        if act == "create_round":
            create_country_league_season_round(ib_round, res)
        elif act == "skip_round_creation":
            continue
        else:
            break



def create_country_league_seasons(country_league):
    """
    In - CountryLeague object
    Out - None
    For each season defined in configuration SEASAONS, it checks if create season,
    and if so, it invokes function resposnible for season creation else it breaks.
    """

    for season in CFG.SEASONS:
        create_season = verify_rounds_to_be_created(country_league, season)
        if create_season:
            create_country_league_season_rounds(country_league, season)



def create():
    """
    In - None
    Out - None
    For each CountryLeague and seasons defined in configuration module, function
    is top level function for creation infobank with matches data.
    """
    create_item(CFG.IB_ROOT)
    for country_league in CFG.SUPPORTED_LEAGUES:
        country = country_league.country
        league = country_league.league_name

        CFG.LOGGER.info("Creating infobank for %s league: %s started", country, league)
        create_item(os.path.join(CFG.IB_ROOT, country))
        create_item(os.path.join(CFG.IB_ROOT, country, league))
        create_country_league_seasons(country_league)
        CFG.LOGGER.info("Creating infobank for %s league: %s finished", country, league)
