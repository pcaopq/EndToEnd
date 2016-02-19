""" driver.py """
""" python 2.7 """

import sys
import processXML as pXML

def do_segment(xml_file, outfile):
	proc = pXML.ProcessXML(xml_file)
	#proc.writeStSpData('test2.txt')
	proc.writeTBData(outfile)

import Latex
if __name__ == '__main__':
    Latex.gen_latex('Eval Results', 'EV.tex')
    Latex.gen_pdf('EV.tex', 'EV.pdf')
