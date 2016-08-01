''' python 2.7 '''

# author: stefan larson

'''
	This script reads in a json file of this format.
	data["annotations"] returns a list of dicts, where each dict is a segmentation item
	of this format:
		{
            "id": 0, (non-negative integer)
            "height": 1448.0, 
            "width": 1536.0, 
            "y": 1328.0, 
            "x": 1288.0, 
            "type": "rect", 
            "class": "article" ("title", "other")
        }
'''

import json
from pprint import pprint
from Box import Box
from Polygon import Polygon
from Segmentation import Segmentation
import pdb

def rect_from_json(fname):
	with open(fname) as data_file:    
	    data = json.load(data_file)
	return data[0]["annotations"]

def seg_from_json(fname):
	with open(fname) as data_file:    
	    data = json.load(data_file)
	#print "data:         ", data
	annotations = data[0]["annotations"]
	#print "annotationssssssssss:     ",annotations

	# TODO: make sure to address the box type (article/image/title) assignment problem (i.e.
	# at box or polygon level)

	polygon_dict = {}
	# polygon_dict has key = id, value = list of boxes
	for segment in annotations:
		if segment['id'] not in polygon_dict:
			polygon_dict[segment['id']] = []
		coord0 = [ segment['y'], segment['x']]
		coord1 = [ coord0[0]+segment['height'] , coord0[1]+segment['width'] ]
		polygon_dict[segment['id']].append( Box(coor0=coord0,coor1=coord1) )

	# convert polygons dict to Segmentation object
	#seg = Segmentation()

	polygons = [Polygon(boxes=boxList) for boxList in polygon_dict.values()]
	return Segmentation(segments=polygons)
	# print seg.segs












	