""" python 2.7 """

# author: stefan larson

# TODO: combine getTBData & writeTBData (have latter call former)

"""
the hierarchy is like this:
page
	textblock
			textline
					string
					space
"""

from xml.dom import minidom
from memory_profiler import profile
import timeit

# from memory_profiler import profile


class  ProcessXML:
	''' class for processing .xml files to get ocr information
	'''

	def __init__(self, fname):
		self.filename = fname	# .xml file
		self.textblocks = None 	# list of textblocks
		self.xmldoc = minidom.parse(self.filename)
	def getTIFdimensions(self):
		''' returns (height, width) of the .tif data in the xml file. we will use this
		data to change scales to the .jp2 image size
		'''
		# self.xmldoc = minidom.parse(self.filename)
		alto = self.xmldoc.getElementsByTagName('alto')[0]
		layout = alto.getElementsByTagName('Layout')[0]
		page = layout.getElementsByTagName('Page')[0]
		h = page.getAttribute('HEIGHT')
		w = page.getAttribute('WIDTH')
		return (h,w)

	def getTextblocks(self):
		""" create list of textblocks """
		# self.xmldoc = minidom.parse(self.filename)
		alto = self.xmldoc.getElementsByTagName('alto')[0]
		layout = alto.getElementsByTagName('Layout')[0]
		page = layout.getElementsByTagName('Page')[0]
		printspace = page.getElementsByTagName('PrintSpace')[0]
		self.textblocks = printspace.getElementsByTagName('TextBlock')

	def getTextLines(self, textblock):
		""" loop thru textlines in a textblock """
		if textblock.getElementsByTagName('TextLine'):
			textlines = textblock.getElementsByTagName('TextLine')
			return textlines
		else:
			return False

	def getStrings(self, textline):
		""" return list of strings from a textline """
		strings = textline.getElementsByTagName('String')
		return strings

	def getSpaces(self, textline):
		""" return a list of spaces from a textline """
		spaces = textline.getElementsByTagName('SP')
		return spaces

	def writeStSpData(self, wname):
		""" write the coordinate data of strings and spaces to wname file """
		if self.textblocks == None:
			self.getTextblocks()
		with open(wname, 'w') as f:
			for tb in self.textblocks:
				textlines = self.getTextLines(tb)
				if not textlines:
					continue
				for tl in textlines:
					strings = self.getStrings(tl)
					for s in strings:
						hpos 	= float(s.getAttribute('HPOS'))
						vpos 	= float(s.getAttribute('VPOS'))
						width 	= float(s.getAttribute('WIDTH'))
						height 	= float(s.getAttribute('HEIGHT'))
						f.write("%f %f %f %f\n" % (hpos,vpos,width,height))
					spaces = self.getSpaces(tl)
					for sp in spaces:
						hpos 	= float(sp.getAttribute('HPOS'))
						vpos 	= float(sp.getAttribute('VPOS'))
						width 	= float(sp.getAttribute('WIDTH'))
						f.write("%s %s %s\n" % (hpos,vpos,width))
		f.close()
		return

	def writeTBData(self, wname):
		""" write the coordinate data of textblocks to wname file """
		if self.textblocks == None:
			self.getTextblocks()
		with open(wname, 'w') as f:
			for tb in self.textblocks:
				if tb.getAttribute('HPOS'):
					hpos 	= float(tb.getAttribute('HPOS'))
					vpos 	= float(tb.getAttribute('VPOS'))
					width 	= float(tb.getAttribute('WIDTH'))
					height 	= float(tb.getAttribute('HEIGHT'))
					f.write("%f %f %f %f\n" % (hpos,vpos,width,height))
		f.close()
		return

	def getTBData(self):
		''' returns a list of (hpos,vpos,width,height) info for each textblock
		'''
		if self.textblocks == None:
			self.getTextblocks()
		tbList = []
		for tb in self.textblocks:
			if tb.getAttribute('HPOS'):
				hpos	= float(tb.getAttribute('HPOS'))
				vpos 	= float(tb.getAttribute('VPOS'))
				width 	= float(tb.getAttribute('WIDTH'))
				height 	= float(tb.getAttribute('HEIGHT'))
				tbList.append( (hpos,vpos,width,height) )
		return tbList
# fp = open('minidom.log','w+')        
# @profile(stream = fp)   
def main():
	start = timeit.default_timer()
	xml = ProcessXML("0003.xml")
	# print(xml.getTBData())
	xml.writeTBData("0003stsp")	
	print timeit.default_timer() - start
if __name__ == '__main__':
	main()	
