from xml.dom import minidom

def readxml(xmlname, scrapedname):
    xmldoc = minidom.parse(xmlname)
    alto = xmldoc.getElementsByTagName('alto')[0]
    layout = alto.getElementsByTagName('Layout')[0]
    page = layout.getElementsByTagName('Page')[0]
    printspace = page.getElementsByTagName('PrintSpace')[0]
    textblocks = printspace.getElementsByTagName('TextBlock')
    with open(scrapedname, 'w') as f:
    	for textblock in textblocks:
            f.write('-'*70+'\n')
            if textblock.getElementsByTagName('TextLine'):
                textlines = textblock.getElementsByTagName('TextLine')
                for textline in textlines:
                    strings = textline.getElementsByTagName('String')
                    sps = textline.getElementsByTagName('SP')
                    for string in strings:
                        L = lambda label:float(string.getAttribute(label))
                        S = lambda label:(string.getAttribute(label))
                        f.write("%s %f %f %f %f\n" % (S('CONTENT'), L('VPOS'), L('HPOS'), L('HEIGHT'),L('WIDTH')))
                    for sp in sps:
                        f.write("%s %s %s\n" % (sp.getAttribute('VPOS'), sp.getAttribute('HPOS'), sp.getAttribute('WIDTH')))
            # if textblock.getAttribute('HPOS'):
            # 	f.write("%f %f %f %f\n" % (float(textblock.getAttribute('HPOS')), float(textblock.getAttribute('VPOS')), float(textblock.getAttribute('WIDTH')), float(textblock.getAttribute('HEIGHT'))))

#import sys
#readxml(sys.argv[1]) #e.g. 0005.xml
