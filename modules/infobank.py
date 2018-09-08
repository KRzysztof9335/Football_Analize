# Standard modules
import os

# User defined modules
import configuration as CFG
import common as CMN
import parser_html as PH
import webhandler as WH

def infobank_create_item(item_to_create):
	try:
		os.makedirs(item_to_create)
		CFG.logger.debug("Creating infobank item: {0} success".format(item_to_create))
	except FileExistsError:
		CFG.logger.debug("Creating infobank item: {0} already exists, skippking creation".format(item_to_create))
	except:
		CFG.logger.error("Creating infobank item: {0} unexpected error".format(item_to_create))

def infobank_save_round_table(infobank_round, content_to_write_round_table):
	round_table_file = os.path.join(infobank_round, "round_table.txt")
	CMN.common_write_to_file(round_table_file, content_to_write_round_table)

def infobank_save_round_matches(infobank_round, round_matches_names, content_to_write_round_matches):
	for  match_name, match_stats in zip(round_matches_names, content_to_write_round_matches):
		match_stats_file = os.path.join(infobank_round, match_name)
		CMN.common_write_to_file(match_stats_file, match_stats)

def infobank_create_content_to_write_round_table(round_table_rows):
	content_to_write_raw = [";".join(round_table_row) for round_table_row in round_table_rows]
	content_to_write = "\n".join(content_to_write_raw)
	return content_to_write
		
def infobank_create_content_to_write_round_matches(round_table_matches):
	matches_names = []
	matches_content_to_write = []
	for round_table_match in round_table_matches:
		match_name = 'match_' + round_table_match[2] + '_' + round_table_match[3] + '.txt'
		match_content_to_write = "\n".join(round_table_match)
		matches_names.append(match_name)
		matches_content_to_write.append(match_content_to_write)
	return matches_content_to_write, matches_names

def infobank_create_country_league_season_round(infobank_round, country, league, season, play_round, raw_round_results):
	infobank_create_item(infobank_round)
	round_table, round_matches = PH.parser_html_get_round_results(infobank_round, raw_round_results)

	content_to_write_round_table = infobank_create_content_to_write_round_table(round_table)
	content_to_write_round_matches, round_matches_names = infobank_create_content_to_write_round_matches(round_matches)

	infobank_save_round_table(infobank_round, content_to_write_round_table)
	infobank_save_round_matches(infobank_round, round_matches_names, content_to_write_round_matches)

def infobank_verify_if_create_round(infobank_round, country, league, season, play_round):
	"""
	This fucntion needs to download web content, so to not necessarily download content
	twice, it will return round content if round happened
	"""
	try:
		if os.stat(os.path.join(infobank_round,"round_table.txt")).st_size != 0:
			CFG.logger.debug("Round {0} alredy exists - skipping further rounds creation".format(infobank_round))
			return False, ""
	except (IOError, ValueError):
		pass # Catching error when file does not exist
	except:
			CFG.logger.critical("Critical error occured when tried to create: {0}".format(infobank_round))
			sys.exit(1)
	raw_round_results = WH.webhandler_get_round_results(country, league, season, play_round)
	all_html_tables = PH.parser_html_get_round_all_html_tables(infobank_round, raw_round_results) # Return list of found tables
	raw_round_matches = PH.parser_html_get_table_content(all_html_tables[1])
	if "-:-" in raw_round_matches[0][5]:
		CFG.logger.debug("Round {0} is future round - skipping further rounds creation".format(infobank_round))
		return False, ""
	return True, raw_round_results

def infobank_verify_if_create_season(season):
	if (int(season) > CFG.CURRENT_YEAR): return False
	return True

def infobank_create_country_league_season_rounds(country, league, season, CFG_ROUNDS):
	for play_round in range(1,CFG_ROUNDS):
		infobank_round = os.path.join(CFG.INFO_BANK_ROOT, country, league, '{0}-{1}'.format(season, season+1),'round_{0}'.format(play_round))
		create_round, raw_round_results = infobank_verify_if_create_round(infobank_round, country, league, season, play_round)
		if create_round:
			infobank_create_country_league_season_round(infobank_round, country, league, season, play_round, raw_round_results)
		else:
			break

def infobank_create_country_league_season(country, league, season):
	infobank_create_item(os.path.join(CFG.INFO_BANK_ROOT, country, league, '{0}-{1}'.format(season, season+1)))
	infobank_create_country_league_season_rounds(country, league, season, CFG.ROUNDS)
	
def infobank_create_country_league_seasons(country, league, seasons):
	for season in seasons:
		create_season = infobank_verify_if_create_season(season)
		if create_season:
			infobank_create_country_league_season(country, league, season)
		else:
			CFG.logger.debug("For {0}/{1} infobank creation stopped - season {2} is future season".format(country, league, season))
			break

def infobank_create():
	infobank_create_item(CFG.INFO_BANK_ROOT)
	for (country,league) in CFG.SUPPORTED_LEAGUES:
		CFG.logger.info("Creating infobank for %s league: %s started",country, league)	
		infobank_create_item(os.path.join(CFG.INFO_BANK_ROOT, country))
		infobank_create_item(os.path.join(CFG.INFO_BANK_ROOT, country, league))
		infobank_create_country_league_seasons(country, league, CFG.SEASONS)
		CFG.logger.info("Creating infobank for %s league: %s finished",country, league)
