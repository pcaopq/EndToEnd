''' Article Labeling
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
        self.boxes = [Box(string=s) for s in ss[1:]]
    def similarity_jaccard(self, other):
        intersect_area = self.intersect(other).area()
        sum_area = self.area() + other.area()
        #print("sum=",sum_area, "int=",intersect_area)
        return 0 if not intersect_area else intersect_area/(sum_area - intersect_area)

class Segmentation:
    def __init__(self, segments=[], string=None):
        if string is not None: self.from_str(string)
        else: self.segments = segments[:]
    def __str__(self): return '\n'.join(str(s) for s in self.segments)
    def from_str(self, string): self.segments = [Segment(string=s) for s in string.split('\n')]
    def similarity_IU2(self, truth):
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
        #print("num0",num0,"num1",num1,"den",den)
        return (num0+num1)/den
    def similarity_jaccard(self, truth):
        '''todo: work on this!'''
        return sum(max(ss.similarity_jaccard(st) for st in truth.segments) for ss in self.segments) / len(self.segments)
