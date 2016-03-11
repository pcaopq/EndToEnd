class Segmentation:
    ''' A Segmentation is a list of Polygons, presumed pairwise non-overlapping.
    '''
    def __init__(self, segments=[], string=None):
        if string is not None: self.from_str(string)
        else: self.segs = segs[:]
    def __str__(self):
        return '\n'.join(str(s) for s in self.segs)
    def from_str(self, string):
        self.segs = [Polygon(string=s) for s in string.split('\n')]

    #TODO: make robust to overlaps...
    def pair_recall(self, truth):
        '''Returns probability that two random points from truth's segments
           will be classified the same way by truth and self (as belonging
           either to the same or to different articles)'''
        matrix = {(i,j):s.intersect(t).area() for i,s in enumerate(self.segs) \
                                                for j,t in enumerate(truth.segs)}

        both_same = sum(v**2 for v in intersects.values())
        both_different = 2*sum(matrix[(i,j)]*matrix[(i_,j_)]
                                    for i,_ in enumerate(self.segs)
                                    for i_ in range(i)
                                    for j,__ in enumerate(truth.segs)
                                    for j_,___ in enumerate(truth.segs) if j!=j_)
        total = sum(ts.area() for ts in truth.segs)**2
        return 0.0 if total==0.0 else (both_same + both_different)/total
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
