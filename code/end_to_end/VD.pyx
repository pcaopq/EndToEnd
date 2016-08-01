# def primes(int kmax):
#     cdef int n, k, i
#     cdef int p[1000]
#     result = []
#     if kmax > 1000:
#         kmax = 1000
#     k = 0
#     n = 2
#     while k < kmax:
#         i = 0
#         while i < k and n % p[i] != 0:
#             i = i + 1
#         if i == k:
#             p[k] = n
#             k = k + 1
#             result.append(n)
#         n = n + 1
#     return result
/*
vector<string> &split(const std::string &s, char delim, std::vector<std::string> &elems) {
    stringstream ss(s);
    string item;
    while (getline(ss, item, delim)) {
        elems.push_back(item);
    }
    return elems;
}

vector<string> split(const string &s, char delim) {
    vector<string> elems;
    split(s, delim, elems);
    return elems;
}
*/
from libc.math cimport *
cdef float[] tocorners(int y, int x, int h, int w):
    cdef float tmp1 = float(y) + float(h)
    cdef float tmp2 = float(x) + float(w)
    cdef float tmp3 = float(y)
    cdef float tmp4 = float(x)
    cdef float tmp[4] = {tmp3, tmp4, tmp1, tmp2}
    return tmp

def join_hori(coors):
    z = zip(*coors)
    cdef int l
    l = len(coors)
    return ((sum(z[0])/l, min(z[1])), (sum(z[2])/l, max(z[3])))

def join_hori2(coors):
    if not coors: 
        return ((0,0),(0,0))
    cdef:
        int i
        int j
        int l
    l = len(coors)
    z = [[[c[i][j] for c in coors] for j in range(2)] for i in range(2)]
    return ((sum(z[0][0])/l, min(z[0][1])), (sum(z[1][0])/l, max(z[1][1])))

def join_verti(coors):
    if not coors: 
        return ((0,0),(0,0))
    cdef:
        int i
        int j
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

 def findtitleheight(heights, bins = 20):
    cdef:
         int m = min(heights)         # compute range
         int M = max(heights) 
         int r = M-m
         float step = float(r)/bins                    #              and scale for histogram
         int i
         int h

    freqs = {i:0 for i in range(bins+1)}    # This is our histogram: counts init'd to 0
    for h in heights:                       # fill the histogram
        freqs[int(float(h-m)/step)] += 1    # with heights

    h,i = max((freqs[i],i) for i in range(bins+1)) #find peak of histogram
    while i<bins and freqs[i]>freqs[i+1]:          #then move right
        i += 1                                     #     until we stop decreasing
    return m+i*step                                #...that's what we return.

 def parse(scrapedname):
    contents=[]
    coordinates=[];
    cdef:
        int i
        int j
        int miny
        int minx
        int maxx
        int maxy

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
    cdef float centerb
    cdef float centera
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
    assignments = {j:[] for j in range(len(textcoors))}
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

''' *** Putting it all together... ***
'''
'''
*** Step -1: Parse command-line arguments: *** '''
import sys, ReadTextLines
assert(len(sys.argv)==5)
outfolder, imagename, xmlname,outname = sys.argv[1:5]
outname = outfolder + '/' + outname.split('/')[-1]
scrapedname = xmlname+'.scraped.txt'
titlesname = xmlname+'.titles.txt'
textsname = xmlname+'.texts.txt'
'''
*** Step 0: Fetch Strips from XML ***'''
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
articleblocks = group_textblocks(len(titleblocks),assignments)
'''
*** Step 4: Write to JSON: *** '''
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
      anns.append({"class": "article",
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















