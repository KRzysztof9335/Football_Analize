"""
This module is responsible for any kind of web pages interactions
"""
# Standard modules
import random
import sys
import time
import urllib.request

# User defined modules
import modules.configuration as CFG

def verify_url_is_alive(url):
    """
    In - string - url to download
    Out - bolean - representing if given url is alive
    Function True if url is alive, False otherwise
    """
    conn_handler = urllib.request.Request(url)
    conn_handler.get_method = lambda: 'HEAD'
    try:
        urllib.request.urlopen(conn_handler)
        CFG.LOGGER.debug("Web page: %s is alive", url)
        return True
    except urllib.error.URLError:
        CFG.LOGGER.critical("Web page: %s is not alive", url)
        return False

def download_webpage_content(url):
    """
    In - string - url to download
    Out - string - html file content
    Function sleeps random seconds (to not download content too fast) and downloads webpage content
    """
    time.sleep(random.randint(CFG.SLEEP_LOW, CFG.SLEEP_HIGH))
    return urllib.request.urlopen(url).read().decode('utf-8')

def download_file_and_save(url_file, path_excel):
    """
    In - string - url to file to download
       - string - path where file will be saved
    """
    urllib.request.urlretrieve(url_file, path_excel)

def get_webpage_content(url):
    """
    In - string - url to download
    Out - string - html file content
    Function returns html content as string.
    """
    url_webpage_is_alive = verify_url_is_alive(url)
    if not url_webpage_is_alive:
        sys.exit(1)
    url_webpage_content = download_webpage_content(url)
    CFG.LOGGER.debug("Downloaded content from: %s", url)
    return url_webpage_content
