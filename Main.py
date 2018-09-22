"""
Module Main - responsible for high level control
"""
#!/usr/bin/python3

# Standard modules
import os
import sys
sys.path.insert(0, '{0}/modules'.format(os.environ['REPO_ROOT']))

# User defined modules
import modules.configuration as CFG
import modules.infobank as IB

def main():
    """
    Top level function - controls what will be executed
    """
    CFG.logger.info("Main started")
    CFG.init()
    CFG.logger.info("Creating infobank: started")
    IB.create()
    CFG.logger.info("Creating infobank: success")
    CFG.logger.info("Main finished")

    
if __name__ == "__main__":
    main()
