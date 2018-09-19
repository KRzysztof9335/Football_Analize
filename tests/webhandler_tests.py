#!/usr/bin/python3

# Standard modules
import os
import sys
import unittest

# User defined modules
sys.path.insert(0, '{0}/modules'.format(os.environ['REPO_ROOT']))

from webhandler import *
import configuration as CFG

class function_webhandler_verify_url_is_alive(unittest.TestCase):

	def test_existng_webpages(self):
		self.assertEqual(webhandler_verify_url_is_alive('https://www.google.com/'), True)
		self.assertEqual(webhandler_verify_url_is_alive('http://www.google.com/'), True)
		self.assertEqual(webhandler_verify_url_is_alive('http://www.google.com'), True)

	def test_non_existing_webpages(self):
		self.assertEqual(webhandler_verify_url_is_alive('http://www.nonexistingwebpage111'), False)

if __name__ == '__main__':
	CFG.init()
	CFG.logger.setLevel(CFG.logging.CRITICAL)
	unittest.main()
