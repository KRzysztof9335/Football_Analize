# Standard modules
import datetime
import logging
import re
import os

#logging.basicConfig(level=logging.DEBUG)
#logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)
FORMAT = "%(levelname)s:[%(funcName)s()]: %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)



class CountryLeague():

	def __init__(self, country, league_name,
					   league_rounds, league_matches_in_round,
					   league_name_wf, league_name_fd):
		self.country = country
		self.league_name = league_name
		self.league_rounds = league_rounds
		self.league_matches_in_round = league_matches_in_round
		self.league_name_wf = league_name_wf
		self.league_name_fd = league_name_fd


def init():
	global CURRENT_YEAR
	global IB_ROOT
	global REPO_ROOT
	global SUPPORTED_LEAGUES
	global URL_WF_ROOT
	global CURRENT_SEASON
	global SEASONS_BACK
	global SEASONS
	global WEB_CONNECTION
	global SLEEP_LOW
	global SLEEP_HIGH
<<<<<<< HEAD

	CURRENT_YEAR = datetime.datetime.now().year
	REPO_ROOT = os.environ['REPO_ROOT']
	IB_ROOT = os.path.join(REPO_ROOT,'infobank')
	SUPPORTED_LEAGUES = [CountryLeague('Germany', 'bundesliga_1', 2, 3, 'bundesliga', 'D1')]

	SLEEP_LOW = 13
	SLEEP_HIGH = 20

	URL_WF_ROOT = 'www.worldfootball.net'
=======

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
	SUPPORTED_LEAGUES = [CountryLeague('Germany', 'bundesliga_1', 34, 3, 'bundesliga', 'D1')]

	SLEEP_LOW = 13
	SLEEP_HIGH = 20

	MATCHES_INFO_URL = 'www.worldfootball.net'
>>>>>>> 92a09ca91fa4b7e9bf0b279637e86e90ae753ea3
	WEB_CONNECTION = 'http://'
	CURRENT_SEASON = 2018 # Curremt is 2018-2019 (so 2018)
	SEASONS_BACK = 0 #3
	SEASONS = list(range(CURRENT_SEASON-SEASONS_BACK, CURRENT_SEASON + 1))

	global rx_html_comment
	global rx_html_table
	global rx_html_table_column
	global rx_html_table_row
	global rx_html_match_scores
	global rx_html_hyperlink
	global rx_html_hyperlink_team

	rx_html_comment = re.compile('<!--.*?-->', re.DOTALL)
	rx_html_table = re.compile('<table.*?</table>', re.DOTALL)
	rx_html_table_column = re.compile('<td.*?>(.*?)</td>',re.DOTALL)
	rx_html_table_row = re.compile('<tr>(.*?)</tr>',re.DOTALL)
	rx_html_match_scores = re.compile('<.*?>(\d+):(\d+)\s+\((\d+):(\d+)\)\s+<.*?>')
	rx_html_hyperlink = re.compile('<a\s+href="(\/.*?)".*')
	rx_html_hyperlink_team = re.compile("<a\s+href=\"\/teams\/(.*?)\/.*")
