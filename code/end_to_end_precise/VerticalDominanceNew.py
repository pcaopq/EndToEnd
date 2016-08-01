'''@author Samuel Tenka

VerticalDominance.py segments newspages by
   0. Reading textlines from XML
   1. Classifying textlines as Title or Text, based on fontsize
   2. Assigning Textlines to Titlelines
   3. Merging, for each Titleline, the set of all associated Textlines.
'''

import json
import VD
from memory_profiler import profile
import sys, ReadTextLines0
import timeit
import time
import pdb
assert(len(sys.argv)==5)
fp = open('VerticalDominanceNew.log', 'w+')
@profile(stream = fp)
def main():
  outfolder, imagename, xmlname,outname = sys.argv[1:5]
  outname = outname.split('/')[-1]
  outname = outfolder + '/' + outname.split('/')[-1]
  scrapedname = xmlname+'.scraped.txt'
  titlesname = xmlname+'.titles.txt'
  textsname = xmlname+'.texts.txt'
  '''
  *** Step 0: Fetch Strips from XML ***'''
  start = timeit.default_timer()
  ReadTextLines0.readxml(xmlname,imagename, scrapedname)
  vdclass = VD.VerticalDominance()
  vdclass.parse(scrapedname)  #contents,coordinates,heights = 
  vdclass.getstrips() #titlestrips,textstrips = 
  '''
  *** Step 1: Classify some blocks as Titles *** '''
  vdclass.gettitleblocks() #titleblocks = 
  '''
  *** Step 2: Compute assignments of Textblocks to Titles *** '''
  vdclass.assign_textblocks() #assignments = 
  '''
  *** Step 3: Merge articleblocks based on title *** '''
  vdclass.group_textblocks()#articleblocks = 
  '''
  *** Step 4: Write to JSON: *** '''
  anns = []

  for j,(y,x,h,w) in enumerate(vdclass.titlecoors):
     anns.append({"class": "title",
                  "height": h-y,
                  "id": j,
                  "type": "rect",
                  "width": w-x,
                  "x": x,
                  "y": y})
  for j,ab in enumerate(vdclass.articleblocks):
     for (y,x,h,w) in ab:
        anns.append({"class": "article",
                     "height": h-y,
                     "id": str(j),
                     "type": "rect",
                     "width": w-x,
                     "x": x,
                     "y": y})

  seg = [{
          "annotations": anns,
        }]

  with open(outname,'w') as f:
     json.dump(seg, f, indent=4)
  f.close()
  with open('../../output/segment'+'/'+'VDnewtime', 'a+') as f:
     f.write("%f"%(timeit.default_timer() - start,))   
     f.write(' ')  
  f.close()
if __name__ == "__main__":
    main()