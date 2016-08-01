'''@author Samuel Tenka
VerticalDominance.py segments newspages by
   0. Reading textlines from XML
   1. Classifying textlines as Title or Text, based on fontsize
   2. Assigning Textlines to Titlelines
   3. Merging, for each Titleline, the set of all associated Textlines.
'''

import json
import processXML
import matplotlib.pyplot as plt
from memory_profiler import profile 
import sys, ReadTextLines0
import timeit
import VD2
assert(len(sys.argv)==5)
def main():
  outfolder, imagename, xmlname,outname = sys.argv[1:5]
  outname = outfolder + '/' + outname.split('/')[-1]
  scrapedname = xmlname+'.scraped.txt'
  titlesname = xmlname+'.titles.txt'
  textsname = xmlname+'.texts.txt'
  '''
  *** Step 0: Fetch Strips from XML ***'''
  start = timeit.default_timer()
  ReadTextLines0.readxml(xmlname,imagename, scrapedname)
  vdclass = VD2.VerticalDominance()
  vdclass.parse(scrapedname)  #contents,coordinates,heights = 
  vdclass.getstrips() #titlestrips,textstrips = 
  # titlestrips,textstrips = getstrips(contents,coordinates,heights)
  DONT_MERGE_JUST_SHOW=False
  if DONT_MERGE_JUST_SHOW:
      titleblocks, articleblocks = vdclass.titlecoors, [[ts] for ts in vdclass.newtextcoors];
      title_assignments = list(range(len(titleblocks)))
      # print(title_assignments)
  else:
      '''
      *** Step 1: Classify some blocks as Titles *** '''
      vdclass.gettitleblocks()
      '''
      *** Step 2: Compute assignments of Textblocks to Titles *** '''
      vdclass.assign_textblocks()
      '''
      *** Step 3: Merge articleblocks based on title *** '''
      vdclass.group_titleblocks()
      # print(title_assignments)
      vdclass.group_textblocks()
  '''
  *** Step 4: Write to JSON: *** '''
  anns = []
  for j,(y,x,h,w) in enumerate(vdclass.titlecoors):
     anns.append({"class": "title",
                  "height": h-y,
                  "id": str(int(vdclass.title_assignments[j])),
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
  with open('../../output/segment'+'/'+'VD2newtime', 'a+') as f:
    f.write("%f"%(timeit.default_timer() - start,))   
    f.write(' ')
  f.close()
if __name__=='__main__':
  main()