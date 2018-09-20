# Standard modules
import random
import sys
import time
import urllib.request

# User defined modules
import modules.configuration as CFG

def webhandler_verify_url_is_alive(url):
	conn_handler = urllib.request.Request(url)
	conn_handler.get_method = lambda: 'HEAD'
	try:
		urllib.request.urlopen(conn_handler)
		CFG.logger.debug("Web page: {0} is alive".format(url))
		return True
	except:
		CFG.logger.critical("Web page: {0} is not alive".format(url))
		return False

def webhandler_download_webpage_content(url_to_download):
	time.sleep(random.randint(CFG.SLEEP_LOW, CFG.SLEEP_HIGH))
	return urllib.request.urlopen(url_to_download).read().decode('utf-8')

def webhandler_get_webpage_content(url_to_download):
	url_webpage_is_alive = webhandler_verify_url_is_alive(url_to_download)
	if not url_webpage_is_alive: sys.exit(1)
	url_webpage_content = webhandler_download_webpage_content(url_to_download)
	CFG.logger.debug("Downloaded content from: {0}".format(url_to_download))
	return url_webpage_content

def webhandler_set_round_results_url(league, season, play_round):
	 return "https://{0}/{1}/{2}-{3}-{4}-spieltag/{5}".format(CFG.MATCHES_INFO_URL, 'schedule', league, season, season+1, play_round)

def webhandler_get_round_results(url):
	return webhandler_get_webpage_content(url)
	


#https://www.worldfootball.net/schedule/bundesliga-2017-2018-spieltag/13/
#https://www.worldfootball.net/schedule/fra-ligue-1-2018-2019-spieltag/2/
