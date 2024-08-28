#!/usr/bin/python
import sys
import os
import ConfigParser
config = ConfigParser.ConfigParser() 

BASE_DIR = "/netsim/"
BIN_DIR = BASE_DIR + "bin/"
ETC_DIR = BASE_DIR + "etc/"
LIB_DIR = BASE_DIR + "lib/"
INST_DIR = BASE_DIR + "inst/"
NETSIM_DIR = BASE_DIR + "netsimdir/"

ENVIRONMENT = ETC_DIR + "environment"
USER_INPUT_XML = ETC_DIR + "user_input.xml"

SimulationName = sys.argv[1]
netsimdir_sims = os.listdir(NETSIM_DIR)

def ValidateSimulation():
	if SimulationName in netsimdir_sims:
		return True
	else:
		return False	


def ImportSimulationName():
	config.read(ENVIRONMENT)
	config.set('Open', 'SIM_NAME', SimulationName)
	with open(ENVIRONMENT, 'wb') as env:
		config.write(env)

def main():
	if ValidateSimulation():
		print(">> .open " + SimulationName) 
		ImportSimulationName()
		print("OK")
	else:
		print("Not a valid simulation")

if __name__ == '__main__': main()
