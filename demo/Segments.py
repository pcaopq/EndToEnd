''' Article Labeling

Precision: do you tell no lies?
Recall:    do you tell the whole truth?

todo: bias F1 (toward which?)
'''

from Box import Box

class Segment:
    def __init__(self, boxes=[], segtype='text', string=None):
        self.segtype=segtype
        if string is not None: self.from_str(string)
        else: self.boxes = boxes
    def label(self): return (self.title, id(self))
    def area(self): return sum(b.area() for b in self.boxes)
    def intersect(self, other):
        intersects = (bs.intersect(bo) for bs in self.boxes for bo in other.boxes)
        return Segment(i for i in intersects if i.area())
    def __str__(self): return self.segtype +'|'+ '|'.join(str(b) for b in self.boxes)
    def from_str(self, string):
        ss = string.split('|')
        self.segtype = ss[0]
        self.boxes = [Box(string=s) for s in ss[1:] if s]
    def jaccard_precision(self, truth):
        '''amount of self area also in truth's area'''
        intersect_area = self.intersect(truth).area()
        return 0 if not intersect_area else intersect_area/self.area()
    def jaccard_recall(self, truth):
        '''amount of truth's area also in self area'''
        intersect_area = self.intersect(truth).area()
        return 0 if not intersect_area else intersect_area/truth.area()
    def similarity_jaccard(self, truth):
        intersect_area = self.intersect(truth).area()
        sum_area = self.area() + truth.area()
        return 0 if not intersect_area else intersect_area/(sum_area - intersect_area)

class Segmentation:
    def __init__(self, segments=[], string=None):
        if string is not None: self.from_str(string)
        else: self.segments = segments[:]
    def __str__(self): return '\n'.join(str(s) for s in self.segments)
    def from_str(self, string): self.segments = [Segment(string=s) for s in string.split('\n')]
    def pair_recall(self, truth):
        '''probability that two random points from truth segments
           will be classified same way by truth and self (as either
           same or different articles)'''
        matrix = {(i,j):ss.intersect(st).area() for i,ss in enumerate(self.segments) \
                                                for j,st in enumerate(truth.segments)}
        num0 = sum(v**2 for v in matrix.values())
        num1 = 2*sum(matrix[(i,j)]*matrix[(i_,j_)] for i,_ in enumerate(self.segments)
                                                   for i_ in range(i)
                                                   for j,__ in enumerate(truth.segments)
                                                   for j_,___ in enumerate(truth.segments) if j!=j_)
        den = sum(ts.area() for ts in truth.segments)**2
        return 0 if den==0 else (num0+num1)/den
    def pair_precision(self, truth):
        return truth.pair_recall(self)
    def pair_fscore(self, truth):
        pairs = (self.pair_precision, self.pair_recall)
        js = [j(truth) for j in pairs]
        return 0 if min(js)==0.0 else len(pairs)/(sum(1.0/jj for jj in js)) #harmonic mean
    def jaccard_precision(self, truth, gamma=1.0):
        return sum(max(ss.jaccard_precision(st) for st in truth.segments)**gamma for ss in self.segments) / len(self.segments)
    def jaccard_recall(self, truth, gamma=1.0):
        return sum(max(ss.jaccard_recall(st) for ss in self.segments)**gamma for st in truth.segments) / len(truth.segments)
    def jaccard_fscore(self, truth, gamma=1.0):
        '''the higher the gamma, the more perfection is prized'''
        jaccs = (self.jaccard_precision, self.jaccard_recall)
        js = [j(truth,gamma) for j in jaccs]
        return 0 if min(js)==0.0 else len(jaccs)/(sum(1.0/jj for jj in js)) #harmonic mean
