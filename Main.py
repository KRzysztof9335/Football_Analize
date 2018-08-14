#!/usr/bin/python3

import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Results taken from http://www.worldfootball.net/schedule/bundesliga-2017-2018-spieltag/
CONFIG_REPO_ROOT = os.environ['REPO_ROOT']
CONFIG_INFO_BANK_ROOT = os.path.join(CONFIG_REPO_ROOT,'infobank')
CONFIG_SUPPORTED_LEAGUES = [('Germany','bundesliga')]
CONFIG_MATCHES_INFO_URL = 'www.worldfootball.net/schedule'
CONFIG_CURRENT_SEASON = 2018
CONFIG_SEASONS_BACK = 3
CONFIG_SEASONS = range(CONFIG_CURRENT_SEASON-CONFIG_SEASONS_BACK, CONFIG_CURRENT_SEASON)
CONFIG_CHECK_FOR_UPDATES_ONLY_CURRENT_SEASON = False

# Main
# 	Database"
#		Germany:
#			bundesliga
#				2017-2018: 
# 					Round1.txt
#					Round2.txt
#						...
#					Round34.txt

def create_infobank_item(item_to_create):
	logger.debug("Creating infobank item: {0}".format(item_to_create))
	try:
		os.makedirs(item_to_create)
		logger.debug("Creating infobank item: {0} success".format(item_to_create))
	except FileExistsError:
		logger.debug("Creating infobank item: {0} already exists, skippking creation".format(item_to_create))
	except:
		logger.error("Creating infobank item: {0} unexpected error".format(item_to_create))

def create_infobank_country_league_season(country, league, season):
	create_infobank_item(os.path.join(CONFIG_INFO_BANK_ROOT, country, league, '{0}-{1}'.format(season, season+1)))
	
def create_infobank_country_league_seasons(country, league, seasons):
	for season in seasons:
		create_infobank_country_league_season(country, league, season)

def create_infobank_country_league(country, league):
	create_infobank_item(os.path.join(CONFIG_INFO_BANK_ROOT, country, league))

def create_infobank_country(country):
	create_infobank_item(os.path.join(CONFIG_INFO_BANK_ROOT, country))

def create_infobank():
	create_infobank_item(CONFIG_INFO_BANK_ROOT)
	for (country,league) in CONFIG_SUPPORTED_LEAGUES:
		logger.info("Creating infobank for %s league: %s started",country, league)	
		create_infobank_country(country)
		create_infobank_country_league(country, league)
		create_infobank_country_league_seasons(country, league, CONFIG_SEASONS)
		logger.info("Creating infobank for %s league: %s finished",country, league)


def main():
	logger.info("Main started")
	logger.info("Creating infobank: started")
	create_infobank()








#	check_for_updates(CONFIG_SUPPORTED_LEAGUES)
	logger.info("Creating infobank: success")
	logger.info("Main finished")


if __name__ == "__main__":
    main()
