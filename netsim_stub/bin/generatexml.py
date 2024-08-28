import sys
import os
import csv
import xml.etree.ElementTree as ET
  

def generate_xml_file(filename):
    if os.path.isfile(filename):
        xmlFile = filename[:-4] + '.xml'
        csvData = csv.reader(open(filename))
        xmlData = open(xmlFile, 'w')
        xmlData.write('<?xml version="1.0"?>' + "\n")
        # there must be only one top-level tag
        xmlData.write('<SimulationData>' + "\n")
        rowNum = 0
        for row in csvData:
            if rowNum == 0:
                tags = row
                for i in range(len(tags)):
                    tags[i] = tags[i].replace(' ', '_')
            else: 
                xmlData.write('<Simulation name=\"' + row[0] +'\">' + "\n")
                for i in range(len(tags)):
                    if i == 0:
                        continue 
                    xmlData.write('    ' + '<' + tags[i] + '>' + row[i] + '</' + tags[i] + '>' + "\n")
                xmlData.write('</Simulation>' + "\n")                
            rowNum +=1
        xmlData.write('</SimulationData>' + "\n")
        xmlData.close()
        return xmlFile


	
def main(argv):
    if len(argv) != 1:
        print "Enter filename with fullpath as argument"
        os._exit(1)
    filename = argv[0] # get folder as a command line argument
    xmlFile = generate_xml_file(filename)
    


    
if __name__ == '__main__':
    main(sys.argv[1:])