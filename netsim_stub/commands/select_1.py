#!/usr/bin/python
import sys
import os
import ConfigParser
config = ConfigParser.RawConfigParser() 

BASE_DIR = "/netsim/"
BIN_DIR = BASE_DIR + "bin/"
ETC_DIR = BASE_DIR + "etc/"
LIB_DIR = BASE_DIR + "lib/"
INST_DIR = BASE_DIR + "inst/"
NETSIM_DIR = BASE_DIR + "netsimdir/"

ENVIRONMENT = ETC_DIR + "environment"
USER_INPUT_XML = ETC_DIR + "user_input.xml"

Selection = sys.argv[1]
netsimdir_sims = os.listdir(NETSIM_DIR)

def ValidateSelection():
	if Selection in netsimdir_sims:
		return True
	else:
		return False	


def ImportSelection(Selection):
	config.read(ENVIRONMENT)
	config.set('Select', 'SELECT_ARG', Selection)
	with open(ENVIRONMENT, 'wb') as env:
		config.write(env)

def main():
	print(">> .select " + Selection) 
	ImportSelection(Selection)
	print("OK")

if __name__ == '__main__': main()
