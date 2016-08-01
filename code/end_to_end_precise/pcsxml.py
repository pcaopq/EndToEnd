'''python 2.7'''
import tinyxml2
import timeit
from memory_profiler import profile

class pcsxml:
	def __init__(self, name):
		self.filename = name
		self.xmldoc = tinyxml2.XMLDocument()
		self.xmldoc.LoadFile(name)
		self.page = self.xmldoc.FirstChildElement("alto").FirstChildElement("Layout").FirstChildElement("Page")
		self.textblks = self.page.FirstChildElement("PrintSpace").FirstChildElement("TextBlock")
	def getTIFdimensions(self):
		# h = tinyxml2.new_intp()
		# w = tinyxml2.new_intp()
		h = self.page.IntAttribute("HEIGHT")
		w = self.page.IntAttribute("WIDTH")
		# tinyxml2.delete_intp(h)
		# tinyxml2.delete_intp(w)
		return (h, w)
	def writeStSpData(self, wname):
		with open(wname, 'w+') as f:
			while(self.textblks != None):
				textlines = self.textblks.FirstChildElement("TextLine")
				hpos = tinyxml2.new_intp()
				vpos = tinyxml2.new_intp()
				width =  tinyxml2.new_intp()
				height = tinyxml2.new_intp()
				while(textlines != None):
					strings = textlines.FirstChildElement("String")
					while(strings != None):
						strings.QueryIntAttribute("HPOS", hpos)
						strings.QueryIntAttribute("VPOS", vpos)
						strings.QueryIntAttribute("WIDTH", width)
						strings.QueryIntAttribute("HEIGHT", height)
						f.write("%f %f %f %f\n"%(tinyxml2.intp_value(hpos),tinyxml2.intp_value(vpos),tinyxml2.intp_value(width),tinyxml2.intp_value(height)))
						strings = strings.NextSiblingElement("String")

					spaces = textlines.FirstChildElement("SP")
					while(spaces != None):
						spaces.QueryIntAttribute("HPOS", hpos)
						spaces.QueryIntAttribute("VPOS", vpos)
						spaces.QueryIntAttribute("WIDTH", width)
						spaces.QueryIntAttribute("HEIGHT", height)
						f.write("%f %f %f %f\n"%(tinyxml2.intp_value(hpos),tinyxml2.intp_value(vpos),tinyxml2.intp_value(width),tinyxml2.intp_value(height)))
						spaces = spaces.NextSiblingElement("SP")

				textlines = textlines.NextSiblingElement("TextLine")
			self.textblks = self.textblks.NextSiblingElement("TextBlock")
		f.close()
		tinyxml2.delete_intp(hpos)
		tinyxml2.delete_intp(vpos)
		tinyxml2.delete_intp(width)
		tinyxml2.delete_intp(height)
		return
	def writeTBData(self, wname):
		with open(wname, 'w+') as f:
			while(self.textblks != None):
				hpos = tinyxml2.new_intp()
				vpos = tinyxml2.new_intp()
				width =  tinyxml2.new_intp()
				height = tinyxml2.new_intp()
				self.textblks.QueryIntAttribute("HPOS", hpos)
				self.textblks.QueryIntAttribute("VPOS", vpos)
				self.textblks.QueryIntAttribute("WIDTH", width)
				self.textblks.QueryIntAttribute("HEIGHT", height)
				f.write("%f %f %f %f"%(tinyxml2.intp_value(hpos), tinyxml2.intp_value(vpos), tinyxml2.intp_value(width), tinyxml2.intp_value(height)))				
				self.textblks = self.textblks.NextSiblingElement("TextBlock")
		f.close()
		tinyxml2.delete_intp(hpos)
		tinyxml2.delete_intp(vpos)
		tinyxml2.delete_intp(width)
		tinyxml2.delete_intp(height)
		return
	def getTBData(self):
		tbList = []
		while(self.textblks != None):
			hpos = tinyxml2.new_intp()
			vpos = tinyxml2.new_intp()
			width =  tinyxml2.new_intp()
			height = tinyxml2.new_intp()
			self.textblks.QueryIntAttribute("HPOS", hpos)
			self.textblks.QueryIntAttribute("VPOS", vpos)
			self.textblks.QueryIntAttribute("WIDTH", width)
			self.textblks.QueryIntAttribute("HEIGHT", height)
			tbList.append((tinyxml2.intp_value(hpos), tinyxml2.intp_value(vpos), tinyxml2.intp_value(width), tinyxml2.intp_value(height)))								
			self.textblks = self.textblks.NextSiblingElement("TextBlock")
		tinyxml2.delete_intp(hpos)
		tinyxml2.delete_intp(vpos)
		tinyxml2.delete_intp(width)
		tinyxml2.delete_intp(height)			
		return tbList

# fp = open('tinyxml2.log','w+')        
# @profile(stream = fp)      
def main():
	start = timeit.default_timer()
	xml = pcsxml("0003.xml")
	# print(xml.getTBData())
	xml.writeTBData("0003stsp")
	print (timeit.default_timer() - start)
if __name__ == '__main__':
	main()























