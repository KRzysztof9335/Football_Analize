# Results taken from http://www.worldfootball.net/schedule/bundesliga-2017-2018-spieltag/

# Standard modules
import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def init():
	global CONFIG_INFO_BANK_ROOT
	global CONFIG_REPO_ROOT
	global CONFIG_SUPPORTED_LEAGUES
	global CONFIG_MATCHES_INFO_URL
	global CONFIG_CURRENT_SEASON
	global CONFIG_SEASONS_BACK
	global CONFIG_ROUNDS
	global CONFIG_SEASONS

	CONFIG_REPO_ROOT = os.environ['REPO_ROOT']
	CONFIG_INFO_BANK_ROOT = os.path.join(CONFIG_REPO_ROOT,'infobank')
	CONFIG_SUPPORTED_LEAGUES = [('Germany','bundesliga')]
	CONFIG_MATCHES_INFO_URL = 'www.worldfootball.net/schedule'
	CONFIG_CURRENT_SEASON = 2018
	CONFIG_SEASONS_BACK = 3
	CONFIG_ROUNDS = 34
	CONFIG_SEASONS = range(CONFIG_CURRENT_SEASON-CONFIG_SEASONS_BACK, CONFIG_CURRENT_SEASON)
