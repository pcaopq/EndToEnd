''' python 2.7 '''

# author: stefan larson

"""
This is a baseline segmentation algorithm. It gets the textblock information from the
xml files and calls each textblock an article.

usage:
	python textblocksBS.py <image> <xml> <output>

	where
		<image> is a jp2 or jpg
		<xml> is xml file associated with the image
		<output> is a .json, to which we write the segmentation results

"""

import csv
import sys
import json


if __name__ == "__main__":
	
	f_image = sys.argv[1]
	f_xml = sys.argv[2]
	f_out = sys.argv[3]

	f = f_image.split('/')[1].split('.')[0]
	f_csv = 'images/' + f + '.csv'
	
	boxes = []
	f = open(f_csv, 'r')
	for line in f:
		dat = line.strip('\n')
		dat = line.split(',')
		boxes.append( [ float(elt) for elt in dat] )
	f.close()
	
	# each list in boxes is of form [c,r,w,h]
	

	# prepare to write to json by putting  data into dicts
	seg = {"annotations":[]}
	id = 0
	for [hpos,vpos,width,height] in boxes:
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
	with open( f_out, 'w' ) as f:
		json.dump(seg, f, indent=4)
	f.close()


