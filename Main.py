#!/usr/bin/python3

# Standard modules
import sys
sys.path.insert(0, './modules')

# User defined modules
import configuration as CFG
import infobank as IB

def main():
	CFG.logger.info("Main started")
	CFG.init()
	CFG.logger.info("Creating infobank: started")
	IB.infobank_create()
#	check_for_updates(CONFIG_SUPPORTED_LEAGUES)
	CFG.logger.info("Creating infobank: success")
	CFG.logger.info("Main finished")


if __name__ == "__main__":
    main()
