#!/usr/bin/python3

# Standard modules
import os
import sys
import unittest
from unittest.mock import patch

# User defined modules
sys.path.insert(0, '{0}'.format(os.environ['REPO_ROOT']))
sys.path.insert(0, '{0}/modules'.format(os.environ['REPO_ROOT']))

from Main import *



class function_main(unittest.TestCase):

	def mocked_infobank_create():
		pass
	
	# patch will not affect next testcase :) If we want to mock we need to do it again
	@patch('infobank.create', side_effect=mocked_infobank_create)
	def test_create_infobank_called(self, info_create):
		main()
		self.assertEqual(info_create.call_count, 1)


if __name__ == '__main__':
	CFG.init()
	CFG.LOGGER.setLevel(CFG.logging.CRITICAL)
	unittest.main()