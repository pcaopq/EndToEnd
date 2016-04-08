'''@author Stefan Larson
adapted by Samuel Tenka
'''
from xml.dom import minidom


class XML:#TODO: rename class to `Metadata` or something like that
    def __init__(self, xml_name):
        self.xml_name = xml_name # .xml file
        self.getTextblocks() #initializes self.textblocks

    def getTIFdimensions(self):
        ''' returns (height, width) of the .tif data in the xml file. we will use this
        data to change scales to the .jp2 image size
        '''
        xmldoc = minidom.parse(self.xml_name)
        page = get0('alto','Layout','Page')(xmldoc)
        h = page.getAttribute('HEIGHT')
        w = page.getAttribute('WIDTH')
        return (h,w)

    def getTextblocks(self):
        """ create list of textblocks """
        xmldoc = minidom.parse(self.xml_name)
        alto = xmldoc.getElementsByTagName('alto')[0]
        layout = alto.getElementsByTagName('Layout')[0]
        page = layout.getElementsByTagName('Page')[0]
        printspace = page.getElementsByTagName('PrintSpace')[0]
        self.textblocks = printspace.getElementsByTagName('TextBlock')
        return self.textblocks
    def getTBData(self):
        """ returns a list of (hpos,vpos,width,height) info for each textblock """
        tbList = []
        for tb in self.textblocks:
            if tb.getAttribute('HPOS'):
                attributes = tuple(s.getAttribute(attr) for attr in ('HPOS','VPOS','WIDTH','HEIGHT'))
                tbList.append( attributes )
        return tbList
    def writeTextblocks(self, wname):
        """ write the coordinate data of textblocks to wname file """
        with open(wname, 'w') as f:
            for attributes in self.getTBData():
                f.write("%s\n" % ' '.join(attributes))
    def writeStringSpaceData(self, wname):
        """ write the coordinate data of strings and spaces to wname file """
        with open(wname, 'w') as f:
            for tb in self.textblocks:
                textlines = self.getTextLines(tb)
                for tl in textlines:
                    strings = self.getStrings(tl)
                    for s in strings:
                        attributes = tuple(s.getAttribute(tag) for tag in ('HPOS','VPOS','WIDTH','HEIGHT'))
                        f.write("%s\n" % ' '.join(attributes))
                    spaces = self.getSpaces(tl)
                    for sp in spaces:
                        attributes = tuple(s.getAttribute(tag) for tag in ('HPOS','VPOS','WIDTH'))
                        f.write("%s\n" % ' '.join(attributes))

    @classmethod
    def getTextLines(self, textblock):
        ##TODO: SCALE THESE COORDINATES!!
        """ loop thru textlines in a textblock """
        textlines = textblock.getElementsByTagName('TextLine')
        textlines = [tuple(float(TL.getAttribute(tag)) for tag in ('VPOS','HPOS','HEIGHT','WIDTH')) for TL in textlines]
        textlines = [((y,x),(y+h,x+w)) for y,x,h,w in textlines]
        return textlines
    @classmethod
    def getStrings(self, textline):
        """ return list of strings from a textline """
        return textline.getElementsByTagName('String')
    @classmethod
    def getSpaces(self, textline):
        """ return a list of spaces from a textline """
        return textline.getElementsByTagName('SP')
