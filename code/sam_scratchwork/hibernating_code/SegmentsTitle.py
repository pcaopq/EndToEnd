''' Article Labeling
'''

#def onetime(func):
#    '''memoization decorator, e.g. for geometry calculations'''
#    computed=False; val=None
#    def onetime(*args, **kwargs):
#        if not computed:
#            val=func(*args, **kwargs); computed=True
#        return val
#    return onetime

class Segment:
    def __init__(self, boxes=[], title=None):
        self.boxes = boxes
        self.title = None
    def label(self): return (self.title, id(self))
    def area(self): return sum(b.area() for b in self.boxes)
    def intersect(self, other):
        return Segment(bs.intersect(bo) for bs in self.boxes for bo in other.boxes)
    def __str__(self): return '|'.join(str(b) for b in self.boxes)
    def from_str(self, string): self.boxes = [Box(s) for s in string.split('|')]

class Segmentation:
    def __init__(self, segments=[]):
        self.segments = {s.title:s for s in segments}
    def __str__(self): return '\n'.join(str(s) for s in self.segments)
    def from_str(self, string): self.boxes = [Box(s) for s in string.split('|')]

    def distance_IU2(self, truth):
        '''sum(intersect*2) / sum(true segments*2)'''
        return sum(ss.intersect(st).area()**2 for ss in self.segments.values()
                                              for st in truth.segments.values()) /
               sum(ts.area()**2 for ts in truth.segments.values())
    def distance_labels(self, truth):
        def distance(tt,ts):
            if tt not in self.segments: return 1.0
            return 0.0 if  else 0.9
        return sum(self.segments[tt].distance(ts) for tt,ts in truth.segments.items())/len(truth.segments)
