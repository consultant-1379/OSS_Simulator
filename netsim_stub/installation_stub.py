#!/usr/bin/python
import os
import crypt
import subprocess
import xml.etree.ElementTree as ET
from distutils.dir_util import copy_tree
from datetime import datetime
import shutil
import logging
import pwd
import zipfile

WORKING_DIR = "/netsim_users/netsim_stub"
ROOT_DIR = "/netsim"
BIN_DIR = ROOT_DIR + "/bin/"
ETC_DIR = ROOT_DIR + "/etc/"
INST_DIR = ROOT_DIR + "/inst/"
SIM_DIR = ROOT_DIR + "/netsimdir/"
DB_DIR = ROOT_DIR + "/netsim_dbdir/simdir/netsim/netsimdir/"
GENERATE_XML = BIN_DIR + "generatexml.py"
GENERATE_EUTRANDATA = BIN_DIR + "generateEutranDataFile.py"
BASE_DIRECTORIES = [ "/netsim/genstats/logs/rollout_console/" , "/netsim/netsimdir/" , "/netsim/netsim_dbdir/simdir/netsim/netsimdir/" , "/netsim/genstats/tmp/" , "/netsim/inst/zzzuserinstallation/mim_files/" , "/netsim/inst/zzzuserinstallation/ecim_pm_mibs/" , "/netsim/bin/" , "/netsim/etc/" , "/netsim/inst/platf_indep_java/linux64/jre/bin/"]
TMPFS_DIR = "/pms_tmpfs/"
JAVA_LINK = "/netsim/inst/platf_indep_java/linux64/jre/bin/java"
USER_NAME = "netsim"
logging.basicConfig(filename="/var/tmp/installation.log", level=logging.INFO)

#condition for file override from job
USER_INPUT_XML = "/tmp/NodeMOMs/user_input_1.8K.xml"


def create_directories(directories, root):
	getCurrentLog("Creating directories for OSS_Simulator" ,'INFO')
	for create_dir in directories:
		os.makedirs(create_dir)
	for Simulation in root.findall('Simulation'):
		cmd = "mkdir -p " + SIM_DIR + Simulation.get('name')
		subprocess.Popen(cmd.split())
		cmd = "touch " + SIM_DIR + Simulation.get('name') + "/simulation.netsimdb"
		subprocess.Popen(cmd.split())
		nodes_ON = Simulation.find('nodes_ON').text
		node_list = nodes_ON.split(":")
		stats_dir = Simulation.find('stats_dir').text
		for node in node_list:
			cmd = "mkdir -p " + DB_DIR + Simulation.get('name') + "/" + node + "/fs/" + stats_dir
			subprocess.Popen(cmd.split())
		

def add_user():
	getCurrentLog("Adding" + USER_NAME + "as a user" ,'INFO')
	password = "netsim"
	encPass = crypt.crypt(password,"22")
	os.system("useradd -d /netsim -p " + encPass + " netsim")

def pre_execution():
	if os.path.exists(ROOT_DIR):
		getCurrentLog("Deleting the older directories" ,'INFO')
		shutil.rmtree(ROOT_DIR)
	if os.path.exists(TMPFS_DIR):
		getCurrentLog("Deleting the existing output directories" ,'INFO')
		shutil.rmtree(TMPFS_DIR)
	os.system("bash " + WORKING_DIR + "/bin/pre_rollout.sh")

def extract_mom():
	getCurrentLog("Extracting MOM Files" ,'INFO')
	os.chdir(INST_DIR + "zzzuserinstallation/")
	zip = zipfile.ZipFile('/tmp/NodeMOMs/mim_files.zip')
	zip.extractall()
	os.chdir(INST_DIR + "zzzuserinstallation/")
	zip = zipfile.ZipFile('/tmp/NodeMOMs/ecim_pm_mibs.zip')
	zip.extractall()
	
def output_directory(root):
	for Simulation in root.findall('Simulation'):
		nodes_ON = Simulation.find('nodes_ON').text
		node_list = nodes_ON.split(":")
		stats_dir = Simulation.find('stats_dir').text
		sim_name = Simulation.get('name')
		for node in node_list:
			if 'LTE' in sim_name: 
				if 'RadioNode' in sim_name:
					cmd = "mkdir -p " + TMPFS_DIR + sim_name + "/" + node + stats_dir
					p = subprocess.Popen(cmd.split())
				else:
					cmd = "mkdir -p " + TMPFS_DIR + sim_name.split("-")[-1] + "/" + node + stats_dir
					p = subprocess.Popen(cmd.split())
			else:
				cmd = "mkdir -p " + TMPFS_DIR + sim_name + "/" + node + stats_dir
				p = subprocess.Popen(cmd.split())

				
def copy_scripts():
	getCurrentLog ("Copying files into required directories" ,'INFO')
	copy_tree(WORKING_DIR + "/bin/", BIN_DIR)
	copy_tree(WORKING_DIR + "/commands/" , BIN_DIR)
	copy_tree(WORKING_DIR + "/etc/" , ETC_DIR)
	copy_tree(WORKING_DIR + "/shell/" , INST_DIR)
	shutil.copy2(USER_INPUT_XML , ETC_DIR)
	os.rename(USER_INPUT_XML , ETC_DIR + "user_input.xml")

def changing_permissions():
	getCurrentLog ("Changing permissions of from root to netsim" ,'INFO')
	subprocess.call(["chown" , "-R" , "netsim:netsim" , ROOT_DIR , TMPFS_DIR])
	subprocess.call(["chmod" , "-R" , "755" , ROOT_DIR , TMPFS_DIR])
	
def cleanup():
	getCurrentLog("Cleaning up the Directories" , "INFO")
	os.remove('/tmp/NodeMOMs.zip')
	shutil.rmtree('/tmp/NodeMOMs')
	
def getCurrentLog(message,type):
	curDateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	if type == 'INFO':
		logging.info(curDateTime + message)
		print 'INFO: ' + curDateTime + message
	elif type == 'WARN':
		logging.warning(curDateTime + message)
		print 'WARNING: ' + curDateTime + message
	
def main():
	if USER_NAME in [entry.pw_name for entry in pwd.getpwall()]:
		getCurrentLog(" User " + USER_NAME + " already exists",'INFO')
	else:
		add_user()
	os.chdir('/tmp')
	zip = zipfile.ZipFile('/tmp/NodeMOMs.zip')
	zip.extractall()
	pre_execution()
	user_input = ET.parse(USER_INPUT_XML)
	root = user_input.getroot()
	create_directories(BASE_DIRECTORIES, root)
	copy_scripts()	
	output_directory(root)
	changing_permissions() 
	subprocess.call(["ln" , "-s" , "/usr/bin/java" , JAVA_LINK])
	for Simulation in root.findall('Simulation'):
		Simulation = Simulation.get('name')
		if 'LTE' in Simulation:
			getCurrentLog("Generating EutranData for LTE Nodes" , 'INFO')
			os.system("su - netsim -c \"python " + GENERATE_EUTRANDATA + "\"")
		else:
			print Simulation
			getCurrentLog("No need of EutranData" , 'INFO')
	cleanup()
if __name__ == "__main__":
	main()
		
		
		
