#!/usr/bin/python

import os
from subprocess import Popen
import xml.etree.ElementTree as ET

USER_INPUT_XML = "/netsim/etc/user_input.xml"
SIM_DIR="/netsim/netsimdir/"
DB_DIR = "/netsim/netsim_dbdir/simdir/netsim/netsimdir/"
EUtranCellDataFile = "EUtranCellData.txt"

def generateEUtranCellData():
	user_input = ET.parse(USER_INPUT_XML)
	root = user_input.getroot()
	for Simulation in root.findall('Simulation'):
		simulationName = Simulation.get('name')
		if 'RadioNode' in simulationName:
			continue
		eutranCellFilePath = SIM_DIR + simulationName + "/SimNetRevision/"
		if not os.path.exists(eutranCellFilePath):
			cmd = "mkdir -p " + eutranCellFilePath
			p = Popen(cmd.split())
		node_type = Simulation.find('node_type').text
		nodes_ON = Simulation.find('nodes_ON').text	
		node_List = nodes_ON.split(":")
		nb_iot_cell = Simulation.find('nb_iot_cell').text
		with open(eutranCellFilePath + EUtranCellDataFile, "w+") as f:
			node_List.sort()
			i = 1
			for node_name in node_List:	
				no_of_cells = Simulation.find('no_of_cells').text
				for j in range(1,int(no_of_cells)+1):
					if i == 1 and nb_iot_cell == "Yes" and node_type == "MSRBS-V2":
						eutranCellData = 'SubNetwork=SUBNW-1,MeContext=' + node_name + ',ManagedElement=' + node_name + ',ENodeBFunction=1,NbIotCell=' + node_name + "-" + str(j)
					else:
						if node_type == "ERBS" or node_type == "PRBS":
							eutranCellData = 'SubNetwork=SubNetwork=ONRM_ROOT_MO,SubNetwork=SUBNW-1,MeContext=' + node_name + ',ManagedElement=' + node_name + ',ENodeBFunction=1,EUtranCellFDD=' + node_name + "-" + str(j)
						if node_type == "MSRBS-V2":
							eutranCellData = 'SubNetwork=SUBNW-1,MeContext=' + node_name + ',ManagedElement=' + node_name + ',ENodeBFunction=1,EUtranCellFDD=' + node_name + "-" + str(j)		
					f.write(eutranCellData + "\n")
					i = i + 1
		

def main():
	generateEUtranCellData()

if __name__ == '__main__': main()
