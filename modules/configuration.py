# Standard modules
import logging
import re
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
	global CONFIG_MATCHES_IN_ROUND
	global CONFIG_SEASONS
	global CONFIG_WEB_CONNECTION

	global rx_html_comment
	global rx_html_table
	global rx_html_table_column
	global rx_html_table_row

	CONFIG_REPO_ROOT = os.environ['REPO_ROOT']
	CONFIG_INFO_BANK_ROOT = os.path.join(CONFIG_REPO_ROOT,'infobank')
	CONFIG_SUPPORTED_LEAGUES = [('Germany','bundesliga')]
	CONFIG_MATCHES_INFO_URL = 'www.worldfootball.net'
	CONFIG_WEB_CONNECTION = 'http://'
	CONFIG_CURRENT_SEASON = 2017
	CONFIG_SEASONS_BACK = 1 #3
	CONFIG_ROUNDS = 2 #9
	CONFIG_MATCHES_IN_ROUND = 1 # In other countries this may vary
	CONFIG_SEASONS = range(CONFIG_CURRENT_SEASON-CONFIG_SEASONS_BACK, CONFIG_CURRENT_SEASON)

	rx_html_comment = re.compile('<!--.*?-->', re.DOTALL)
	rx_html_table = re.compile('<table.*?</table>', re.DOTALL)
	rx_html_table_column = re.compile('<td.*?>(.*?)</td>',re.DOTALL)
	rx_html_table_row = re.compile('<tr>(.*?)</tr>',re.DOTALL)
