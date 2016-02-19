""" driver.py """
""" python 2.7 """

import sys
import processXML as pXML


if __name__ == "__main__":

	image_file 	= sys.argv[1]
	xml_file 	= sys.argv[2]
	
	proc = pXML.ProcessXML(xml_file)
	proc.writeStSpData('test2.txt')
	proc.writeTBData('tb.txt')