#!/usr/bin/python
import sys
import ConfigParser
import xml.etree.ElementTree as ET
import re


arg1 = sys.argv[1]

BASE_DIR = "/netsim/"
BIN_DIR = BASE_DIR + "bin/"
ETC_DIR = BASE_DIR + "etc/"
LIB_DIR = BASE_DIR + "lib/"
INST_DIR = BASE_DIR + "inst/"

NETYPES = ETC_DIR + "netypes.txt"
ENVIRONMENT = ETC_DIR + "environment" 
USER_INPUT_XML = ETC_DIR + "user_input.xml"

PM_MIBS = {"MSRBS-V2":["17-Q4-RUI-V3", "MSRBS-V2_71-Q4_V3UPGMib.xml"], "PRBS":["61A-UPGIND-LTE-ECIM-MSRBS-V1", "PRBS_61A_UPGIND_V1Mib.xml"]}

with open(USER_INPUT_XML, "r") as user_input_file:
	user_input_string = user_input_file.read()
user_input = ET.fromstring(user_input_string)

def ConfigSectionMap(section):
	Config = ConfigParser.ConfigParser()
	Config.read(ENVIRONMENT)
	env_dict = {}
	options = Config.options(section)
	for option in options:
		try:
			env_dict[option] = Config.get(section, option)
			if env_dict[option] == -1:
				DebugPrint("skip: %s" % option)
		except:
			print("exception on %s!" % option)
			env_dict[option] = None
	return env_dict

def get_simulation_data(SimulationName):
	print("NE Name                  Type                 Server         In Address       Default dest.")
	try:
		node_name = user_input.findall(".//*[@name='%s']/node_name" % SimulationName)[0].text
		node_type = user_input.findall(".//*[@name='%s']/node_type" % SimulationName)[0].text
		sim_mim_ver = user_input.findall(".//*[@name='%s']/sim_mim_ver" % SimulationName)[0].text
		sim_mim_ver = re.sub('[_]','',sim_mim_ver)
        	network = user_input.findall(".//*[@name='%s']/network" % SimulationName)[0].text
		get_output(node_name, node_type, sim_mim_ver, network)
	except IndexError:
		print("in except")
		pass

def get_output(node_name, node_type, sim_mim_ver, network):
	print(node_name + "\t\t " + network + " " + node_type + " " + sim_mim_ver + " netsim")
	

def get_started():
	node_name = user_input.findall(".//*/nodes_ON")
	node_List = [node.text for node in node_name]
	sim_name = user_input.findall(".//*/sim_name")
	sim_List = [sim.text for sim in sim_name]
	dict = {}
	if len(sim_List) == len(node_List):
		for i in range(0, len(sim_List)):
			dict[sim_List[i]] = node_List[i]
	for key in dict:
		if dict[key] == "NULL":
			continue
		mim_ver = key.split(":")[2]
		mim_ver = re.sub('[_]','',mim_ver)	
		print("\n")
		print("'server_" + key.replace(":", "-") + "@netsim' for " + key.split(":")[0] + " " + key.split(":")[1] + " " + mim_ver)
		print("=================================================================")
		print("    NE                          Simulation/Commands")
		for node in dict[key].split(":"):
			print("    " + node + "\t\t/netsim/netsimdir/" + key.replace(":", "-"))



def netype_full(node_type, mim_ver):
	for netype in PM_MIBS:
		if netype == node_type:
			if mim_ver == PM_MIBS[netype][0]:
				print ("pm_mib :  \"" + PM_MIBS[netype][1] + "\"")


def main():
	SimulationName = ConfigSectionMap('Open')['sim_name']
	if arg1 == "simnes":
		print(">> .show " + arg1)
		get_simulation_data(SimulationName)
		print("OK")
	elif arg1 == "started":
		print(">> .show " + arg1)
		get_started()
		print("OK")
	elif ' '.join(sys.argv[1:]).startswith("netype full"):
		print(">> .show " + ' '.join(sys.argv[1:]))
		netype_full(sys.argv[3], sys.argv[4])
		print("OK")
	elif arg1 == "netypes":
		with open(NETYPES, 'r') as netypes:
			print netypes.read()
	else:
		print(sys.argv[1:])
		print("function not defined yet")



if __name__ == '__main__': main()
