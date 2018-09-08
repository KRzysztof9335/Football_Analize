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
	global rx_html_match_scores
	global rx_html_hyperlink
	global rx_html_hyperlink_team

	CONFIG_REPO_ROOT = os.environ['REPO_ROOT']
	CONFIG_INFO_BANK_ROOT = os.path.join(CONFIG_REPO_ROOT,'infobank')
	CONFIG_SUPPORTED_LEAGUES = [('Germany','bundesliga')]
	CONFIG_MATCHES_INFO_URL = 'www.worldfootball.net'
	CONFIG_WEB_CONNECTION = 'http://'
	CONFIG_CURRENT_SEASON = 2017
	CONFIG_SEASONS_BACK = 1 #3
	CONFIG_ROUNDS = 9 #9
	CONFIG_MATCHES_IN_ROUND = 1 # In other countries this may vary
	CONFIG_SEASONS = range(CONFIG_CURRENT_SEASON-CONFIG_SEASONS_BACK, CONFIG_CURRENT_SEASON)

	rx_html_comment = re.compile('<!--.*?-->', re.DOTALL)
	rx_html_table = re.compile('<table.*?</table>', re.DOTALL)
	rx_html_table_column = re.compile('<td.*?>(.*?)</td>',re.DOTALL)
	rx_html_table_row = re.compile('<tr>(.*?)</tr>',re.DOTALL)
	rx_html_match_scores = re.compile('<.*?>(\d+):(\d+)\s+\((\d+):(\d+)\)\s+<.*?>')
	rx_html_hyperlink = re.compile('<a\s+href="(\/.*?)".*')
	rx_html_hyperlink_team = re.compile("<a\s+href=\"\/teams\/(.*?)\/.*")

# Structure

# Main.py
# 	Database"
#		Germany:
#			bundesliga
#				2017-2018 
# 					Round1
#						round_table.txt
#						match__team1_team2.txt
#						match__team3_team4.txt
#					Round2
#						...
#					Round3

# match__team1_team2.txt
#	match_date
#	match_hour
# 	match_home_team (team1)
# 	match_away_team (team1)
# 	HTFT
# 	ATFT
# 	HTHT
# 	ATHT
# 	match_reportdu -sh
# Place for additional info...

# round_table.txt
# place;team1;matches_played;matches_won;matches_draw;matches_lost;goals_shot:goals_lost;goals_diff;points
# place;team2;matches_played;matches_won;matches_draw;matches_lost;goals_shot:goals_lost;goals_diff;points
# ...
