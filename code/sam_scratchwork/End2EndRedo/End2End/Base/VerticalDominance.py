'''@author Samuel Tenka
VerticalDominance.py segments newspages by
   0. Reading textlines from XML
   1. Classifying textlines as Title or Text, based on fontsize
   2. Assigning Textlines to Titlelines
   3. Merging, for each Titleline, the set of all associated Textlines.
'''
from Segmentation import Segmentation
from NewsPage import NewsPage

class VerticalDominance:
    def __init__(self):
        pass
    def segment(self, newspage):
        textlines = self.read_textlines_from_metadata(newspage)
        titles,articles = self.identify_titles(textlines)
        self.merge_horizontally_neighboring_titles()
        self.assign_articles_to_titles()
        articles = self.merge_articlelines_into_columns(len(titles), assigments)
        title_assignments = self.merge_vertically_neighboring_titles()
    def read_textlines_from_metadata(self,newspage):
        return [TL for TB in newspage.xml.getTextblocks()
                   for TL in newspage.xml.getTextLines(TB)]
    def findtitleheight(self,heights,bins=20):
        m,M = min(heights),max(heights)         # Compute range
        r = M-m; step=r/bins                    # and scale for histogram.
        freqs = {i:0 for i in range(bins+1)}    # Stores our histogram, with counts initialized to 0.
        for h in heights:                       # Fill the histogram
            freqs[int(float(h-m)/step)] += 1    # with heights.
        h,i = max((freqs[i],i) for i in range(bins+1)) # Find peak of histogram
        while i<bins and freqs[i]>freqs[i+1]:          # then move right
            i += 1                                     #     until we stop decreasing;
        return m+i*step                                #...that's what we return.
    def merge_horizontally_neighboring_titles(titles):
        '''Merges titlestrips horizontally, into long, thin strips.'''
        def adjoins(a,b):
            centerb = (b[0][0]+b[1][0])/2.0
            ayy = lambda yy: a[0][0]<yy<a[1][0]
            centera = (a[0][0]+a[1][0])/2.0
            byy = lambda yy: b[0][0]<yy<b[1][0]
            return 0<a[0][1]-b[1][1]<500 and (ayy(centerb) and ayy(centera))
        def join_hori2(coors):
            if not coors: return ((0,0),(0,0))
            l = len(coors)
            z = [[[c[i][j] for c in coors] for j in range(2)] for i in range(2)]
            return ((sum(z[0][0])/l, min(z[0][1])), (sum(z[1][0])/l, max(z[1][1])))
        done=False
        while not done: #while we haven't checked every pair of titlestrips
            done=True
            for i,t in enumerate(titlecoors): #loop through titlestrips
                for tt in titlecoors[i:]: #loop through potential partners
                    if not (adjoins(tt,t) or adjoins(t,tt)): continue
                    #if they can be merged:
                    if t in titles: titles.remove(t)   # then merge
                    if tt in titles: titles.remove(tt) # them, removing
                    titles.append(join_hori2([t,tt]))  # the originals
                    done=False                         # from our pool of titlecoors, and appending their merged form.
                    break
                if not done:
                    break
        return titles
    def assign_articles_to_titles(self):
        def dominates(a,b):
            centerb0 = (1*b[0][1]+3*b[1][1])/4.0
            centerb1 = (3*b[0][1]+1*b[1][1])/4.0
            axx = lambda xx: a[0][1]<xx<a[1][1]
            return a[0][0]<b[1][0] and (axx(centerb0) or axx(centerb1))
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
    def merge_articlelines_into_columns(self,N,assignments):
        '''assignments will have _keys_ of TITLE_IDs (here, iterator variable `j`),
        and _values_ of LISTS OF TEXTSTRIPS (here, iterator variable `words`,
        each of whose elements will be a rectangle)'''
        def supports(a,b):
            centerb0 = (1*b[0][1]+3*b[1][1])/4.0
            centerb1 = (3*b[0][1]+1*b[1][1])/4.0
            axx = lambda xx: a[0][1]<xx<a[1][1]
            return a[1][0]>=b[0][0] and (axx(centerb0) or axx(centerb1))
        def join_verti(coors):
            if not coors: return ((0,0),(0,0))
            z = [[[c[i][j] for c in coors] for j in range(2)] for i in range(2)]
            return ((min(z[0][0]), min(z[0][1])), (max(z[1][0]), max(z[1][1])))
        articles=[[] for j in range(N)]
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
                articles[j].append(join_verti(ws)) # remember our column
                for w in ws: #remove all words in our column from future candidates for future columns
                    words.remove(w)
        return articles
    def merge_vertically_neighboring_titles(self,titles):
        '''vertically merge titleblocks'''
        def sitson(a,b):
            centerxx = lambda ab: (1*ab[0][1]+1*ab[1][1])/2.0
            xx = lambda ab: lambda xx: ab[0][1]<xx<ab[1][1]
            return a[1][0]>=b[0][0] and (xx(a)(centerxx(b)) and xx(b)(centerxx(a)))
        title_assignments = list(range(len(titles)))
        for j,tb in enumerate(titles):
            if assignments[j]: continue
            try:
                jj = min((title[1][0],jj) for jj,title in enumerate(titles) if j!=jj and sitson(title,tb))[1]
                title_assignments[j] = jj
            except ValueError: #from trying to take `min` of an empty iterator
                print('no dominating title supports title [%s]'%str(tb))
        for i in range(len(titles)): #super inefficient LOL
            for j in range(len(titles)):
                title_assignments[j] = title_assignments[title_assignments[j]]
        return title_assignments

V = VerticalDominance()
X = NewsPage('0003')
V.segment(X)
