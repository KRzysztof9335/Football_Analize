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



<<<<<<< HEAD

=======
	
>>>>>>> 92a09ca91fa4b7e9bf0b279637e86e90ae753ea3
def infobank_create_content_to_write_round_matches(round_table_matches):
	matches_names = []
	matches_content_to_write = []
	for round_table_match in round_table_matches:
		match_name = 'match_' + round_table_match[2] + '_' + round_table_match[3] + '.txt'
		match_content_to_write = "\n".join(round_table_match)
		matches_names.append(match_name)
		matches_content_to_write.append(match_content_to_write)
	return matches_content_to_write, matches_names




def infobank_create_country_league_season_round(infobank_round, raw_round_results):

	infobank_create_item(infobank_round)
	round_table, round_matches = PH.parser_html_get_round_results(infobank_round, raw_round_results)

	content_to_write_round_table = infobank_create_content_to_write_round_table(round_table)
	content_to_write_round_matches, round_matches_names = infobank_create_content_to_write_round_matches(round_matches)

	infobank_save_round_table(infobank_round, content_to_write_round_table)
	infobank_save_round_matches(infobank_round, round_matches_names, content_to_write_round_matches)





<<<<<<< HEAD
def infobank_verify_if_create_country_league_season_round_round_played(infobank_round, raw_round_matches):
=======
def infobank_verify_if_create_round_round_played(infobank_round, raw_round_matches):
>>>>>>> 92a09ca91fa4b7e9bf0b279637e86e90ae753ea3
	if "-:-" in raw_round_matches[0][5]:
		CFG.logger.debug("Round {0} is future round - skipping further rounds creation".format(infobank_round))
		return False
	return True




<<<<<<< HEAD
def infobank_verify_if_create_country_league_season_round_already_exists(infobank_round):
=======
def infobank_verify_if_create_round_already_exists(infobank_round):
>>>>>>> 92a09ca91fa4b7e9bf0b279637e86e90ae753ea3
	try:
		if os.stat(os.path.join(infobank_round,"round_table.txt")).st_size != 0:
			CFG.logger.debug("Round {0} alredy exists - skipping round creation".format(infobank_round))
			return True
	except (IOError, ValueError):
		return False # Catching error when file does not exist
	except:
			CFG.logger.critical("Critical error occured when tried to create: {0}".format(infobank_round))
			sys.exit(1)


<<<<<<< HEAD
def infobank_verify_if_create_country_league_season_round(country_league, season, play_round, infobank_round):
=======
def infobank_verify_if_create_round(country_league_object, season, play_round, infobank_round):
>>>>>>> 92a09ca91fa4b7e9bf0b279637e86e90ae753ea3
	"""
	This fucntion needs to download web content, so to not necessarily download content
	twice, it will return round content if round happened
	"""
<<<<<<< HEAD
	country = country_league.country
	league = country_league.league_name
	league_name_wf = country_league.league_name_wf

	if infobank_verify_if_create_country_league_season_round_already_exists(infobank_round): return "skip_round_creation", ""

	wf_round_url = "https://{0}/schedule/{1}-{2}-{3}-spieltag/{4}".format(CFG.URL_WF_ROOT, league_name_wf, season, season + 1, play_round)
=======
	country = country_league_object.country
	league = country_league_object.league_name
	league_name_wf = country_league_object.league_name_wf

	if infobank_verify_if_create_round_already_exists(infobank_round): return "skip_round_creation", ""

	wf_round_url = "https://{0}/schedule/{1}-{2}-{3}-spieltag/{4}".format(CFG.MATCHES_INFO_URL, league_name_wf, season, season+1, play_round)
>>>>>>> 92a09ca91fa4b7e9bf0b279637e86e90ae753ea3
	raw_round_results = WH.webhandler_get_round_results(wf_round_url)
	all_html_tables = PH.parser_html_get_round_all_html_tables(infobank_round, raw_round_results) # Return list of found tables
	raw_round_matches = PH.parser_html_get_table_content(all_html_tables[1])

<<<<<<< HEAD
	if not infobank_verify_if_create_country_league_season_round_round_played(infobank_round, raw_round_matches): return "skip_all", ""
=======
	if not infobank_verify_if_create_round_round_played(infobank_round, raw_round_matches): return "skip_all", ""
>>>>>>> 92a09ca91fa4b7e9bf0b279637e86e90ae753ea3
	return "create_round", raw_round_results




<<<<<<< HEAD
def infobank_verify_if_create_country_league_season_rounds(country_league, season):
	"""
	In - CountryLeague Object, season Int
	Out - Boolean
	Function checks if season integer is not future season
	"""
	country = country_league.country
	league = country_league.league_name

	if (season > CFG.CURRENT_YEAR):
=======
def infobank_verify_if_create_season(country_league_object, season):
	country = country_league_object.country
	league = country_league_object.league_name

	if (int(season) > CFG.CURRENT_YEAR):
>>>>>>> 92a09ca91fa4b7e9bf0b279637e86e90ae753ea3
		CFG.logger.debug("For {0}/{1} infobank creation stopped - season {2} is future season".format(country, league, season))
		return False
	return True




<<<<<<< HEAD
def infobank_create_country_league_season_rounds(country_league, season):
	"""
	In - CountryLeague Object, season Int
	Out - None
	Function invokes function checking what action should be done in context of
	round. If return of invoked function is to create_round, then round is created
	"""
	country = country_league.country
	league = country_league.league_name
	play_rounds = list(range(1,country_league.league_rounds + 1))

	for play_round in play_rounds:
		infobank_round = os.path.join(CFG.IB_ROOT, country, league, '{0}-{1}'.format(season, season+1),'round_{0}'.format(play_round))
		round_action, raw_round_results = infobank_verify_if_create_country_league_season_round(country_league, season, play_round, infobank_round)
		print(raw_round_results)
=======
def infobank_create_country_league_season_rounds(country_league_object, season, CFG_ROUNDS):
	country = country_league_object.country
	league = country_league_object.league_name
	play_rounds = list(range(1,country_league_object.league_rounds + 1))

	for play_round in play_rounds:
		infobank_round = os.path.join(CFG.INFO_BANK_ROOT, country, league, '{0}-{1}'.format(season, season+1),'round_{0}'.format(play_round))
		round_action, raw_round_results = infobank_verify_if_create_round(country_league_object, season, play_round,infobank_round)
>>>>>>> 92a09ca91fa4b7e9bf0b279637e86e90ae753ea3
		if round_action == "create_round": infobank_create_country_league_season_round(infobank_round, raw_round_results)
		elif round_action == "skip_round_creation": continue
		else: break




<<<<<<< HEAD

def infobank_create_country_league_seasons(country_league):
	"""
	In - CountryLeague object
	Out - None
	For each season defined in configuration SEASAONS, it checks if create season,
	and if so, it invokes function resposnible for season creation else it breaks.
	"""
	country = country_league.country
	league = country_league.league_name

	for season in CFG.SEASONS:
		create_season = infobank_verify_if_create_country_league_season_rounds(country_league, season)
		if create_season: infobank_create_country_league_season_rounds(country_league, season)
=======
def infobank_create_country_league_season(country_league_object, season):
	country = country_league_object.country
	league = country_league_object.league_name

	infobank_create_item(os.path.join(CFG.INFO_BANK_ROOT, country, league, '{0}-{1}'.format(season, season+1)))
	infobank_create_country_league_season_rounds(country_league_object, season, CFG.ROUNDS)




def infobank_create_country_league_seasons(country_league_object, seasons):
	country = country_league_object.country
	league = country_league_object.league_name

	for season in seasons:
		create_season = infobank_verify_if_create_season(country_league_object, season)
		if create_season: infobank_create_country_league_season(country_league_object, season)
>>>>>>> 92a09ca91fa4b7e9bf0b279637e86e90ae753ea3
		else: break




def infobank_create():
<<<<<<< HEAD
	"""
	In - None
	Out - None
	For each CountryLeague and seasons defined in configuration module, function
	is top level function for creation infobank with matches data.
	"""
	infobank_create_item(CFG.IB_ROOT)
	for country_league in CFG.SUPPORTED_LEAGUES:
		country = country_league.country
		league = country_league.league_name

		CFG.logger.info("Creating infobank for %s league: %s started",country, league)
		infobank_create_item(os.path.join(CFG.IB_ROOT, country))
		infobank_create_item(os.path.join(CFG.IB_ROOT, country, league))
		infobank_create_country_league_seasons(country_league)
=======
	infobank_create_item(CFG.INFO_BANK_ROOT)
	for country_league_object in CFG.SUPPORTED_LEAGUES:
		country = country_league_object.country
		league = country_league_object.league_name

		CFG.logger.info("Creating infobank for %s league: %s started",country, league)	
		infobank_create_item(os.path.join(CFG.INFO_BANK_ROOT, country))
		infobank_create_item(os.path.join(CFG.INFO_BANK_ROOT, country, league))
		infobank_create_country_league_seasons(country_league_object, CFG.SEASONS)
>>>>>>> 92a09ca91fa4b7e9bf0b279637e86e90ae753ea3
		CFG.logger.info("Creating infobank for %s league: %s finished",country, league)
