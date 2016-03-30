''' python 2.7 '''

# author: stefan larson

'''
This is a baseline segmentation algorithm. It gets the textblock information from the
xml files and calls each textblock an article.

usage:
	python textblocksBS.py <image> <xml> <output>

	where
		<image> is a jp2 or jpg
		<xml> is xml file associated with the image
		<output> is a .json, to which we write the segmentation results

'''

import processXML
import sys
import json
from PIL import Image as PILI
def size_of_image(imname):
	im=PILI.open(imname	)
	return im.size[::-1] #[height,width]


if __name__ == "__main__":

	f_out_folder = sys.argv[1]
	f_image = sys.argv[2]
	f_xml = sys.argv[3]
	f_out = sys.argv[4].split('/')[-1]

	# read xml data
	pxml = processXML.ProcessXML(f_xml)
	tbList = pxml.getTBData() # list of (hpos,vpos,width,height) info per t.b.
	(h,w) = pxml.getTIFdimensions(); h,w=float(h),float(w)
	(hj,wj) = size_of_image(f_image)
	hs,ws = float(hj)/h, float(wj)/w
	tbList = [(hpos*ws,vpos*hs,width*ws,height*hs) for (hpos,vpos,width,height) in tbList]

	# prepare to write to json by putting  data into dicts
	seg = {"annotations":[]}
	id = 0
	for (hpos,vpos,width,height) in tbList:
		tbInfo = {}
		tbInfo["class"] = "article"
		tbInfo["height"] = height
		tbInfo["width"] = width
		tbInfo["x"] = hpos
		tbInfo["y"] = vpos
		tbInfo["type"] = "rect"
		tbInfo["id"] = id
		seg["annotations"].append(tbInfo)
		id += 1

	# write to json
	with open( f_out_folder+'/'+f_out, 'w' ) as f:
		json.dump(seg, f, indent=4)
	f.close()
