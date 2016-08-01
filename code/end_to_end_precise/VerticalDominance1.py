'''@author Samuel Tenka
VerticalDominance.py segments newspages by
   0. Reading textlines from XML
   1. Classifying textlines as Title or Text, based on fontsize
   2. Assigning Textlines to Titlelines
   3. Merging, for each Titleline, the set of all associated Textlines.
'''

import json
import processXML
from memory_profiler import profile
import pdb

''' *** Geometry Code: How to Merge Rectangles *** '''
def tocorners(y,x,h,w):
    y,x,h,w = (float(v) for v in (y,x,h,w))
    return (y,x,y+h,x+w)
def join_hori(coors):
    z = list(zip(*coors)); l=len(coors)
    return ((sum(z[0])/l, min(z[1])), (sum(z[2])/l, max(z[3])))
def join_hori2(coors):
    if not coors: return ((0,0),(0,0))
    l = len(coors)
    z = [[[c[i][j] for c in coors] for j in range(2)] for i in range(2)]
    return ((sum(z[0][0])/l, min(z[0][1])), (sum(z[1][0])/l, max(z[1][1])))
def join_verti(coors):
    if not coors: return ((0,0),(0,0))
    z = [[[c[i][j] for c in coors] for j in range(2)] for i in range(2)]
    return ((min(z[0][0]), min(z[0][1])), (max(z[1][0]), max(z[1][1])))

''' *** used in `parse` to extract coordinates and textstrings from a piece of text
   representing --- in our inhouse format (developed by Panfeng and Sam, needs to be improved) ---
   a textblock (containing multiple lines)
   *** '''
def consume_block(lines):
    chunk = []
    for line in lines:
        words = line.split()
        if len(words)==5:
            chunk.append(words)
        elif chunk:
           text = ' '.join(ws[0] for ws in chunk)
           coor = join_hori([tocorners(*ws[1:]) for ws in chunk])
           yield text,coor
           chunk=[]

''' *** Histogram Code: How to Determine Title/Text Height-Threshold *** '''
def findtitleheight(heights,bins=20):
    m,M =min(heights),max(heights)          # compute range
    r = M-m; step=r/bins                    #              and scale for histogram

    freqs = {i:0 for i in range(bins+1)}    # This is our histogram: counts init'd to 0
    for h in heights:                       # fill the histogram
        freqs[int(float(h-m)/step)] += 1    # with heights

    h,i = max((freqs[i],i) for i in range(bins+1)) #find peak of histogram
    while i<bins and freqs[i]>freqs[i+1]:          #then move right
        i += 1                                     #     until we stop decreasing
    return m+i*step                                #...that's what we return.

''' *** Given a filename for ReadTextLines.py's readxml's output,
        extracts and returns `contents` (i.e.actual textstrings),
        `coordinates` (the good stuff on which this code operates: title/textstrips)
        and `heights` (computed from `coordinates`)
        TODO: replace with call's to Stefan's elegant XML reader!! :ODOT
    *** '''
def parse(scrapedname):
   contents=[]; coordinates=[];
   with open(scrapedname) as f:
       for block in f.read().split('-'*70):
           for t,c in consume_block(block.split('\n')):
               contents.append(t)
               coordinates.append(c)
               #print(t,c)
   xs = [[c[j][i] for c in coordinates for j in range(2)] for i in range(2)]
   miny, maxy, minx, maxx = min(xs[0]), max(xs[0]), min(xs[1]), max(xs[1])
   print('vpos ranges in [%d,%d]; hpos ranges in [%d,%d]' % (miny, maxy, minx, maxx))
   heights = [c[1][0]-c[0][0] for c in coordinates]
   return contents,coordinates,heights

''' *** Used in `gettitleblocks` for detecting whether to merge two titlestrips,
        by checking whether the titlestrips are at same vertical level, and are
        (nearly) flush with each other horizontally. *** '''
def adjoins(a,b):
   centerb = (b[0][0]+b[1][0])/2.0
   ayy = lambda yy: a[0][0]<yy<a[1][0]
   centera = (a[0][0]+a[1][0])/2.0
   byy = lambda yy: b[0][0]<yy<b[1][0]
   return 0<a[0][1]-b[1][1]<500 and (ayy(centerb) and ayy(centera))
''' *** Classifies title v text strips (Calls our histogram code to do this) *** '''
def getstrips(contents,coordinates,heights):
   TH = findtitleheight(heights)
   print('titleheights=',TH)
   titlecoors=[]; textcoors=[]
   for i,(con,coor) in enumerate(zip(contents,coordinates)):
       h = coor[1][0]-coor[0][0]
       (textcoors if h<TH else titlecoors).append(coor)
   return titlecoors,textcoors
''' *** Merges titlestrips horizontally, into long, thin strips *** '''
def gettitleblocks(titlecoors):
   f=True
   while f: #while we haven't checked every pair of titlestrips
      f=False
      for i,t in enumerate(titlecoors): #loop through titlestrips
         for tt in titlecoors[i:]: #loop through potential partners
            if adjoins(tt,t) or adjoins(t,tt): #if they can be merged:
               if t in titlecoors: titlecoors.remove(t)   # then merge
               if tt in titlecoors: titlecoors.remove(tt) # them, removing
               titlecoors.append(join_hori2([t,tt]))      # the originals
               f=True                                     # from our pool of titlecoors, and appending their merged form.
               break
         if f:
            break
   return titlecoors

''' *** Used in `assign_textblocks` for Determining whether a title `a`
        `vertically dominates` a given textstrip `b`. Vertical domination
        means `a` lies directly above `b`; for details see coefficient in code. *** '''
def dominates(a,b):
   centerb0 = (1*b[0][1]+3*b[1][1])/4.0
   centerb1 = (3*b[0][1]+1*b[1][1])/4.0
   axx = lambda xx: a[0][1]<xx<a[1][1]
   return a[0][0]<b[1][0] and (axx(centerb0) or axx(centerb1))

''' *** Used in `group_textblocks` for Determining whether to vertically merge
        two textstrips known to belong to the same title. Returns whether
        or not (a is _below_ b   and   a and b are sufficiently aligned) *** '''
def supports(a,b):
   centerb0 = (1*b[0][1]+3*b[1][1])/4.0
   centerb1 = (3*b[0][1]+1*b[1][1])/4.0
   axx = lambda xx: a[0][1]<xx<a[1][1]
   return a[1][0]>=b[0][0] and (axx(centerb0) or axx(centerb1))

''' *** Assign Textstrips to Textblocks*** '''
def assign_textblocks(titlecoors, textcoors):
    #assignments[titleid] WILL BE [all words that are dominated by that title]
    assignments = {j:[] for j in range(len(titlecoors))}
    for word in textcoors:
        try:
            #find the lowest (i.e. maximum [1][0], i.e. item of upper boundary _farthest_ from upper edge of image)
            #     the lowest title that dominates given word
            j = max((title[1][0],j) for j,title in enumerate(titlecoors) if dominates(title,word))[1]
            assignments[j].append(word)
        except ValueError: #from trying to take `max` of an empty iterator
            print('no title dominates [%s]'%str(word))
    return assignments

''' *** Merge Textstrips based on their assignments to TitleBlocks *** '''
def group_textblocks(N,assignments):
   '''assignments will have _keys_ of TITLE_IDs (here, iterator variable `j`),
      and _values_ of LISTS OF TEXTSTRIPS (here, iterator variable `words`,
      each of whose elements will be a rectangle)'''
   articleblocks=[[] for j in range(N)]
   for j,words in assignments.items(): #for each group of title/associated textstrips:
      if not words: continue #(don't bother if there are _no_ associated textstrips)

      #In what follows, our pattern will be to keep merging textstrips vertically,
      #into columns; in each loop, we find such a column, then remove from `words`
      #the members of that column, so that `words` is empty exactly when we've
      #finally assigned each textstrip to some column.
      while words:
         maxword = words[0]
         for w in words[1:]: # find lowest word in same column as words[0]
            if supports(w, maxword):
               maxword=w
         ws = [w for w in words if supports(maxword, w)] # this is our column
         articleblocks[j].append(join_verti(ws)) # remember our column
         for w in ws: #remove all words in our column from future candidates for future columns
            words.remove(w)
   return articleblocks

''' *** Used in `group_titleblocks` for Determining whether to identify
        two titlestrips. extremely weak (i.e. very easy to satisfy; usually true)
        True if `b` sits on a`.*** '''
def sitson(a,b):
    centerxx = lambda ab: (1*ab[0][1]+1*ab[1][1])/2.0
    xx = lambda ab: lambda xx: ab[0][1]<xx<ab[1][1]
    return a[1][0]>=b[0][0] and (xx(a)(centerxx(b)) and xx(b)(centerxx(a)))
def group_titleblocks(titleblocks,assignments):
   '''vertically merge titleblocks'''
   title_assignments = list(range(len(titleblocks)))
   for j,tb in enumerate(titleblocks):
       if assignments[j]: 
        continue
       try:
           #find the highest (i.e. minimum [1][1], i.e. item of lower boundary _nearest_ to upper edge of image)
           #     the highest title that dominates some word and supports `tb`
           jj = min((title[1][0],jj) for jj,title in enumerate(titleblocks) if j!=jj and sitson(title,tb))[1]
           title_assignments[j] = jj
       except ValueError: #from trying to take `min` of an empty iterator
           print('no dominating title supports title [%s]'%str(tb))
   for i in range(len(titleblocks)): #super inefficient LOL
       for j in range(len(titleblocks)):
           title_assignments[j] = title_assignments[title_assignments[j]]
   print(title_assignments)
   return title_assignments

''' *** Putting it all together... ***
'''
'''
*** Step -1: Parse command-line arguments: *** '''
import sys, ReadTextLines
import timeit
assert(len(sys.argv)==5)
fp = open('VerticalDominance1.log', 'w+')
@profile(stream=fp)
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
  ReadTextLines.readxml(xmlname,imagename, scrapedname)
  contents,coordinates,heights = parse(scrapedname)
  titlestrips,textstrips = getstrips(contents,coordinates,heights)
  '''
  *** Step 1: Classify some blocks as Titles *** '''
  titleblocks = gettitleblocks(titlestrips)
  '''
  *** Step 2: Compute assignments of Textblocks to Titles *** '''
  assignments = assign_textblocks(titleblocks,textstrips)
  '''
  *** Step 3: Merge articleblocks based on title *** '''
  title_assignments = group_titleblocks(titleblocks,assignments)
  articleblocks = group_textblocks(len(titleblocks),assignments)
  '''
  *** Step 4: Write to JSON: *** '''
  anns = []
  for j,((y,x),(h,w)) in enumerate(titleblocks):
     anns.append({"class": "title",
                  "height": h-y,
                  "id": str(title_assignments[j]),
                  "type": "rect",
                  "width": w-x,
                  "x": x,
                  "y": y})
  for j,ab in enumerate(articleblocks):
     for ((y,x),(h,w)) in ab:
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
  with open('../../output/segment'+'/'+'VD1oldtime', 'a+') as f:
    f.write("%f"%(timeit.default_timer() - start,))   
    f.write(' ')
  f.close()
if __name__=='__main__':
  main()
