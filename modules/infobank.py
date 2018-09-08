# Standard modules
import os

# User defined modules
import configuration as CFG
import common as CMN
import parser_html as PH
import webhandler as WH

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

def infobank_create_country_league_season_round(infobank_round, country, league, season, play_round):
	infobank_create_item(infobank_round)

	raw_round_results = WH.webhandler_get_round_results(country, league, season, play_round)
	if not raw_round_results:CFG.logger.critical("Round creation: {0} unexpected error".format(infobank_round))
	round_table, round_matches = PH.parser_html_get_round_results(infobank_round, raw_round_results)

	content_to_write_round_table = infobank_create_content_to_write_round_table(round_table)
	content_to_write_round_matches, round_matches_names = infobank_create_content_to_write_round_matches(round_matches)

	infobank_save_round_table(infobank_round, content_to_write_round_table)
	infobank_save_round_matches(infobank_round, round_matches_names, content_to_write_round_matches)

def infobank_create_country_league_season_rounds(country, league, season, CFG_CONFIG_ROUNDS):
	for play_round in range(1,CFG_CONFIG_ROUNDS):
		infobank_round = os.path.join(CFG.CONFIG_INFO_BANK_ROOT, country, league, '{0}-{1}'.format(season, season+1),'round_{0}'.format(play_round))
		try:
			if os.stat(os.path.join(infobank_round,"round_table.txt")).st_size != 0: round_exists = True
			else: round_exists = False	
		except: round_exists = False
		if round_exists: CFG.logger.debug("Round {0} alredy exists - skipping creation".format(infobank_round))
		else:infobank_create_country_league_season_round(infobank_round, country, league, season, play_round)

def infobank_create_country_league_season(country, league, season):
	infobank_create_item(os.path.join(CFG.CONFIG_INFO_BANK_ROOT, country, league, '{0}-{1}'.format(season, season+1)))
	infobank_create_country_league_season_rounds(country, league, season, CFG.CONFIG_ROUNDS)
	
def infobank_create_country_league_seasons(country, league, seasons):
	for season in seasons:
		infobank_create_country_league_season(country, league, season)

def infobank_create_item(item_to_create):
	try:
		os.makedirs(item_to_create)
		CFG.logger.debug("Creating infobank item: {0} success".format(item_to_create))
	except FileExistsError:
		CFG.logger.debug("Creating infobank item: {0} already exists, skippking creation".format(item_to_create))
	except:
		CFG.logger.error("Creating infobank item: {0} unexpected error".format(item_to_create))

def infobank_create():
	infobank_create_item(CFG.CONFIG_INFO_BANK_ROOT)
	for (country,league) in CFG.CONFIG_SUPPORTED_LEAGUES:
		CFG.logger.info("Creating infobank for %s league: %s started",country, league)	
		infobank_create_item(os.path.join(CFG.CONFIG_INFO_BANK_ROOT, country))
		infobank_create_item(os.path.join(CFG.CONFIG_INFO_BANK_ROOT, country, league))
		infobank_create_country_league_seasons(country, league, CFG.CONFIG_SEASONS)
		CFG.logger.info("Creating infobank for %s league: %s finished",country, league)
