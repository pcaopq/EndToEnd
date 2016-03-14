## @author: Samuel Tenka
 #
import json

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

def findtitleheight(heights,bins=20):
    #heights = [math.log(h) for h in heights]
    m,M =min(heights),max(heights)
    r = M-m; step=r/bins
    freqs = {i:0 for i in range(bins+1)}
    for h in heights:
        freqs[int(float(h-m)/step)] += 1
    h,i = max((freqs[i],i) for i in range(bins+1))
    while i<bins and freqs[i]>freqs[i+1]:
        i += 1
    #return math.exp(m+i*step)
    return m+i*step
    
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

def adjoins(a,b):
   centerb = (b[0][0]+b[1][0])/2.0
   ayy = lambda yy: a[0][0]<yy<a[1][0]
   centera = (a[0][0]+a[1][0])/2.0
   byy = lambda yy: b[0][0]<yy<b[1][0]
   return 0<a[0][1]-b[1][1]<500 and (ayy(centerb) and ayy(centera))
   
def getstrips(contents,coordinates,heights):
   TH = findtitleheight(heights)
   print('titleheights=',TH)
   titlecoors=[]; textcoors=[]
   for i,(con,coor) in enumerate(zip(contents,coordinates)):
       h = coor[1][0]-coor[0][0]
       (textcoors if h<TH else titlecoors).append(coor)
   return titlecoors,textcoors
def gettitleblocks(titlecoors):
   f=True
   while f:
      f=False
      for i,t in enumerate(titlecoors):
         for tt in titlecoors[i:]:
            if adjoins(tt,t) or adjoins(t,tt):
               if t in titlecoors: titlecoors.remove(t)
               if tt in titlecoors: titlecoors.remove(tt)
               titlecoors.append(join_hori2([t,tt]))
               f=True
               break
         if f:
            break
   return titlecoors
   
   
def dominates(a,b):
   centerb0 = (1*b[0][1]+3*b[1][1])/4.0
   centerb1 = (3*b[0][1]+1*b[1][1])/4.0
   axx = lambda xx: a[0][1]<xx<a[1][1]
   return a[0][0]<b[1][0] and (axx(centerb0) or axx(centerb1))
def supports(a,b):
   centerb0 = (1*b[0][1]+3*b[1][1])/4.0
   centerb1 = (3*b[0][1]+1*b[1][1])/4.0
   axx = lambda xx: a[0][1]<xx<a[1][1]
   return a[1][0]>=b[0][0] and (axx(centerb0) or axx(centerb1))
   
def assign_textblocks(titlecoors, textcoors):
   assignments = {j:[] for j in range(len(textcoors))}
   for word in textcoors:
      try:
         j = max((title[1][0],j) for j,title in enumerate(titlecoors) if dominates(title,word))[1]
         assignments[j].append(word)
      except ValueError:
         print('no title dominates [%s]'%str(word))
   return assignments
def group_textblocks(N,assignments):
   articleblocks=[[] for j in range(N)]
   for j,words in assignments.items():
      if not words: continue
      while words:
         maxword = words[0]
         for w in words[1:]:
            if supports(w, maxword):
               maxword=w
         ws = [w for w in words if supports(maxword, w)]
         articleblocks[j].append(join_verti(ws))
         for w in ws:
            words.remove(w)
      #order info is useful!
   return articleblocks
   
import sys, test
assert(len(sys.argv)==5)
outfolder, imagename, xmlname,outname = sys.argv[1:5]
outname = outfolder + '/' + outname.split('/')[-1]
scrapedname = xmlname+'.scraped.txt'
titlesname = xmlname+'.titles.txt'
textsname = xmlname+'.texts.txt'
test.readxml(xmlname,scrapedname)
contents,coordinates,heights = parse(scrapedname)
titlestrips,textstrips = getstrips(contents,coordinates,heights)
titleblocks = gettitleblocks(titlestrips)
assignments = assign_textblocks(titleblocks,textstrips)
articleblocks = group_textblocks(len(titleblocks),assignments)

#with open(titlesname,'w') as f:
#    for coor in titleblocks:
#        f.write('%f %f %f %f\n' % tuple(coor[i][j] for i in range(2) for j in range(2)))
#with open(textsname,'w') as f:
#    for coor in articleblocks:
#        f.write('%f %f %f %f\n' % tuple(coor[i][j] for i in range(2) for j in range(2)))

anns = []
for j,((y,x),(h,w)) in enumerate(titleblocks):
   anns.append({"class": "title", 
                "height": h-y,
                "id": j, 
                "type": "rect", 
                "width": w-x, 
                "x": x, 
                "y": y})
for j,ab in enumerate(articleblocks):
   for ((y,x),(h,w)) in ab:
      anns.append({"class": "text", 
                   "height": h-y,
                   "id": str(j), 
                   "type": "rect", 
                   "width": w-x, 
                   "x": x, 
                   "y": y})
                
seg = {
        "annotations": anns,
      }

with open(outname,'w') as f:
   json.dump(seg, f, indent=4)