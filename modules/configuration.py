"""
This module is responsible for setting configuration - only this file should be changed when
adding new supported league.
"""
# Standard modules
import collections
import datetime
import logging
import random
import re
import os

#logging.basicConfig(level=logging.DEBUG)
#LOGGER = logging.getLOGGER(__name__)

LOGGER = logging.getLogger(__name__)
FORMAT = "%(levelname)s:[%(funcName)s():%(lineno)d]: %(message)s"
logging.basicConfig(format=FORMAT)
LOGGER.setLevel(logging.DEBUG)

CountryLeague = collections.namedtuple('CL', 'country \
                                              league_name \
                                              league_rounds \
                                              league_matches_in_round \
                                              league_name_wf \
                                              league_name_fd \
                                              fd_url_name')

def init():
    """
    This function is necessary to set variables.
    """
    global CURRENT_YEAR
    global IB_ROOT
    global REPO_ROOT

    CURRENT_YEAR = datetime.datetime.now().year
    REPO_ROOT = os.environ['REPO_ROOT']
    IB_ROOT = os.path.join(REPO_ROOT, 'infobank')
    ###############################################################################################
    global SUPPORTED_LEAGUES

    SUPPORTED_LEAGUES = [CountryLeague('Germany', 'bundesliga_1', 34, 9, 'bundesliga', \
                                       'D1', 'germany')]

    ###############################################################################################
    global CURRENT_SEASON
    global SEASONS_BACK
    global SEASONS

    CURRENT_SEASON = 2018 # Curremt is 2018-2019 (so 2018)
    SEASONS_BACK = 3 #3
    SEASONS = list(range(CURRENT_SEASON-SEASONS_BACK, CURRENT_SEASON + 1))

    ###############################################################################################
    global SLEEP_LOW
    global SLEEP_HIGH
    global SLEEP_TIME

    SLEEP_LOW = 6
    SLEEP_HIGH = 8
    SLEEP_TIME = random.randint(SLEEP_LOW, SLEEP_HIGH)

    ###############################################################################################
    global WEB_PROTOCOL
    global FD_URL_ROOT
    global FD_URL_COUNTRY
    global WF_URL_ROOT
    global WF_URL_ROUND

    WEB_PROTOCOL = 'http://'
    WF_URL_ROOT = WEB_PROTOCOL + 'www.worldfootball.net'
    WF_URL_ROUND = WF_URL_ROOT + "/schedule/{0}-{1}-{2}-spieltag/{3}"
    FD_URL_ROOT = WEB_PROTOCOL + 'www.football-data.co.uk'
    FD_URL_COUNTRY = FD_URL_ROOT + '/{0}m.php'

    ###############################################################################################
    global RX_HTML_COMMENT
    global RX_HTML_TABLE
    global RX_HTML_TABLE_COLUMN
    global RX_HTML_TABLE_ROW
    global RX_HTML_MATCH_SCORES
    global RX_HTML_HYPERLINK
    global RX_HTML_HYPERLINK_TEAM
    global RX_WF_GOALS

    RX_HTML_COMMENT = re.compile(r'<!--.*?-->', re.DOTALL)
    RX_HTML_TABLE = re.compile(r'<table.*?</table>', re.DOTALL)
    RX_HTML_TABLE_COLUMN = re.compile(r'<td.*?>(.*?)</td>', re.DOTALL)
    RX_HTML_TABLE_ROW = re.compile(r'<tr>(.*?)</tr>', re.DOTALL)
    RX_HTML_MATCH_SCORES = re.compile(r'<.*?>(\d+):(\d+)\s+\((\d+):(\d+)\)\s+<.*?>')
    RX_HTML_HYPERLINK = re.compile(r'<a\s+href="(\/.*?)".*')
    RX_HTML_HYPERLINK_TEAM = re.compile(r"<a\s+href=\"\/teams\/(.*?)\/.*")
    RX_WF_GOALS = re.compile(r'(\d+):(\d+)')

    ###############################################################################################
    global FD_TO_WF_BUNDESLIGA_1
    FD_TO_WF_BUNDESLIGA_1 = {'Augsburg':'fc-augsburg',
                             'Bayern Munich':'bayern-muenchen',
                             "M'gladbach":'bor-moenchengladbach',
                             'Darmstadt':'sv-darmstadt-98',
                             'Dortmund':'borussia-dortmund',
                             'Ein Frankfurt':'eintracht-frankfurt',
                             'Fortuna Dusseldorf':'fortuna-duesseldorf',
                             'FC Koln':'1-fc-koeln',
                             'Freiburg':'sc-freiburg',
                             'Hamburg':'hamburger-sv',
                             'Hannover':'hannover-96',
                             'Hertha':'hertha-bsc',
                             'Hoffenheim':'1899-hoffenheim',
                             'Ingolstadt':'fc-ingolstadt-04',
                             'Leverkusen':'bayer-leverkusen',
                             'Mainz':'1-fsv-mainz-05',
                             'Nurnberg':'1-fc-nuernberg',
                             'RB Leipzig':'rb-leipzig',
                             'Schalke':'fc-schalke-04',
                             'Stuttgart':'vfb-stuttgart',
                             'Werder Bremen':'werder-bremen',
                             'Wolfsburg':'vfl-wolfsburg'}

    ###############################################################################################
    global FD_COLUMNS
    FD_COLUMNS = ['HS', 'AS', 'HST', 'AST', \
                  'HF', 'AF', 'HC', 'AC', \
                  'HY', 'AY', 'HR', 'AR', \
                  'B365H', 'B365D', 'B365A']
