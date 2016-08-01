# 0003time.py
from processXML import *
import time
start_time = time.time()
a = ProcessXML("0003.xml")
c = a.getTBData()
print(len(c))
for x in c:
	print(x)
print("\n")
print("--- %s seconds ---" % (time.time() - start_time))



