# Standard modules
import os
import re
import sys

# User defined modules
sys.path.insert(0, '{0}/modules'.format(os.environ['REPO_ROOT']))

def common_get_file_content(file_to_get):
	file_handler = open(file_to_get, 'r')
	file_content = file_handler.read()
	file_handler.close()
	return file_content

def common_write_to_file(file_to_write, content_to_write):
	file_handler = open(file_to_write, 'w+')
	file_handler.write(content_to_write)
	file_handler.close()
