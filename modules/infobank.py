# Standard modules
import os

# User defined modules
import configuration as CFG
import parser_html as PH
import webhandler as WH

# Main.py
# 	Database"
#		Germany:
#			bundesliga
#				2017-2018 
# 					Round1
#						round_table.txt
#						match_1_team1_team2.txt
#						match_2_team3_team4.txt
#					Round2.txt
#						...
#					Round34.txt


def infobank_create_country_league_season_round(country, league, season, play_round):
	infobank_round = os.path.join(CFG.CONFIG_INFO_BANK_ROOT, country, league, '{0}-{1}'.format(season, season+1),'round_{0}'.format(play_round))
	raw_round_results = WH.webhandler_get_round_results(country, league, season, play_round)
	if not raw_round_results:
		CFG.logger.error("Round creation: {0} unexpected error".format(infobank_round))
		return False
	round_table, round_matches = PH.parser_html_get_round_results(infobank_round, raw_round_results)
	return True
	# Here will be code represnting what to do if we have web page as string 

def infobank_create_country_league_season_rounds(country, league, season, CFG_CONFIG_ROUNDS):
	for play_round in range(1,CFG_CONFIG_ROUNDS):
		infobank_create_country_league_season_round(country, league, season, play_round)

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
