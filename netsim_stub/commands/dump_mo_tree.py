#!/usr/bin/python
import sys
import os
import ConfigParser
import xml.etree.ElementTree as ET

config = ConfigParser.RawConfigParser()

cmd = sys.argv[1:]
site_cmd = "dumpmotree:moid=\"1\",printattrs, scope=0, includeattrs=\"site\";"

BASE_DIR = "/netsim/"
BIN_DIR = BASE_DIR + "bin/"
ETC_DIR = BASE_DIR + "etc/"
LIB_DIR = BASE_DIR + "lib/"
INST_DIR = BASE_DIR + "inst/"
NETSIM_DIR = BASE_DIR + "netsimdir/"

ENVIRONMENT = ETC_DIR + "environment"
USER_INPUT_XML = ETC_DIR + "user_input.xml"
with open(USER_INPUT_XML, "r") as user_input_file:
        user_input_string = user_input_file.read()

CPP_NE_TYPES = ["M-MGW", "ERBS", "RBS", "RNC"]

config.read(ENVIRONMENT)
sim_name = config.get('Open', 'sim_name')

user_input = ET.fromstring(user_input_string)
node_type = user_input.findall(".//*[@name='%s']/node_type" % sim_name)[0].text
stats_dir = user_input.findall(".//*[@name='%s']/stats_dir" % sim_name)[0].text
trace_dir = user_input.findall(".//*[@name='%s']/trace_dir" % sim_name)[0].text
site_loc = user_input.findall(".//*[@name='%s']/site_loc" % sim_name)[0].text

list1 = ["PmEventM=", "FilePullCapabilities"]
data_dir = "fileLocation"
if ' '.join(cmd) == site_cmd:
	print("site_loc : " + site_loc)
else:
	if cmd.__contains__(list1[0]) and cmd.__contains__(list1[1]):
		data_dir = "outputDirectory"
	elif node_type in CPP_NE_TYPES:
		data_dir = "performanceDataPath"
	else:
		data_dir = "fileLocation"

	if  data_dir == "performanceDataPath" or data_dir == "fileLocation":
		print(data_dir + "=" + stats_dir)
	else:
		print(data_dir + "=" + trace_dir)


