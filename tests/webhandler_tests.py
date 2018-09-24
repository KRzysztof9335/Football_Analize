#!/usr/bin/python3

# Standard modules
import os
import sys
import unittest

# User defined modules
sys.path.insert(0, '{0}'.format(os.environ['REPO_ROOT']))

import modules.configuration as CFG
import modules.webhandler as WH

class function_verify_url_is_alive(unittest.TestCase):

	def test_existng_webpages(self):
		self.assertEqual(WH.verify_url_is_alive('https://www.google.com/'), True)
		self.assertEqual(WH.verify_url_is_alive('http://www.google.com/'), True)
		self.assertEqual(WH.verify_url_is_alive('http://www.google.com'), True)

	def test_non_existing_webpages(self):
		self.assertEqual(WH.verify_url_is_alive('http://www.nonexistingwebpage111'), False)

if __name__ == '__main__':
	CFG.init()
	CFG.LOGGER.setLevel(CFG.logging.CRITICAL)
	unittest.main()
