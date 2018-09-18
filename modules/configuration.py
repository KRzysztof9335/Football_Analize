# Standard modules
import datetime
import logging
import re
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def init():
	global CURRENT_YEAR
	global INFO_BANK_ROOT
	global REPO_ROOT
	global SUPPORTED_LEAGUES
	global MATCHES_INFO_URL
	global CURRENT_SEASON
	global SEASONS_BACK
	global ROUNDS
	global MATCHES_IN_ROUND
	global SEASONS
	global WEB_CONNECTION

	global rx_html_comment
	global rx_html_table
	global rx_html_table_column
	global rx_html_table_row
	global rx_html_match_scores
	global rx_html_hyperlink
	global rx_html_hyperlink_team

	CURRENT_YEAR = datetime.datetime.now().year
	REPO_ROOT = os.environ['REPO_ROOT']
	INFO_BANK_ROOT = os.path.join(REPO_ROOT,'infobank')
	SUPPORTED_LEAGUES = [('Germany','bundesliga')]
	MATCHES_INFO_URL = 'www.worldfootball.net'
	WEB_CONNECTION = 'http://'
	CURRENT_SEASON = 2018 # Curremt is 2018-2019
	SEASONS_BACK = 0 #3
	ROUNDS = 10 #9
	MATCHES_IN_ROUND = 1 # In other countries this may vary
	SEASONS = list(range(CURRENT_SEASON-SEASONS_BACK, CURRENT_SEASON + 1))

	rx_html_comment = re.compile('<!--.*?-->', re.DOTALL)
	rx_html_table = re.compile('<table.*?</table>', re.DOTALL)
	rx_html_table_column = re.compile('<td.*?>(.*?)</td>',re.DOTALL)
	rx_html_table_row = re.compile('<tr>(.*?)</tr>',re.DOTALL)
	rx_html_match_scores = re.compile('<.*?>(\d+):(\d+)\s+\((\d+):(\d+)\)\s+<.*?>')
	rx_html_hyperlink = re.compile('<a\s+href="(\/.*?)".*')
	rx_html_hyperlink_team = re.compile("<a\s+href=\"\/teams\/(.*?)\/.*")
