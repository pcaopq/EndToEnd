# testso.py
# pcre2: /usr/local/Cellar/pcre2/10.21
# pcre: /usr/local/Cellar/pcre/8.38
# swig -c++ -python example.i
# g++ -O2 -fPIC -c tinyxml2.cpp (-std = c++11) (-std = c++0x)
# g++ -O2 -fPIC -c tinyxml2_wrap.cxx -I/usr/include/python2.6
# g++ -lpython -dynamiclib tinyxml2.o tinyxml2_wrap.o -o _tinyxml2.so
# >>> import example
# >>> c = example.new_intp()     # Create an "int" for storing result
# >>> example.add(3,4,c)         # Call function
# >>> example.intp_value(c)      # Dereference
# 7
# >>> example.delete_intp(c)     # Delete
import tinyxml2
# import ctypes

def main():
	# tinyxml2lib = ctypes.cdll.LoadLibrary("tinyxml2.so")
	# doc = tinyxml2lib.tinyxml2.XMLDocument
	# doc = tinyxml2.XMLDocument()
	doc = tinyxml2.XMLDocument()
	doc.LoadFile("0003.xml")
	pRoot = doc.FirstChildElement("alto")
	pElement = pRoot.FirstChildElement("Layout").FirstChildElement("Page").FirstChildElement("PrintSpace").FirstChildElement("TextBlock")
	# INTP = ctypes.POINTER(ctypes.c_int)
	# num = ctypes.c_int(0)
	# addr = ctypes.addressof(num)
	# ptr = ctypes.cast(addr, INTP)
	a = tinyxml2.new_intp()
	# pElement.QueryIntAttribute("HPOS", a)
	# print(tinyxml2.intp_value(a))
	# tinyxml2.delete_intp(a)
	while(pElement != None):
		pElement.QueryIntAttribute("HPOS", a)
		print(tinyxml2.intp_value(a))
		pElement = pElement.NextSiblingElement("TextBlock");
	tinyxml2.delete_intp(a)
	# print(a.QueryIntValue())
if __name__ == '__main__':
	main()