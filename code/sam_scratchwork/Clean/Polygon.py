class Polygon:
    ''' A Polygon is a list of Boxes, presumed pairwise non-overlapping.
        The whole Polygon may be labeled with a `label` in ('text', 'title', etc.).
        Polygon also supports image-weighted areas: if `weight_image`, a member
        of the class on whole, is set to a NewsImage object, then Polygons'
        area-calculations will be weighted by that object's blackness values.
    '''
    weight_image = None
    def __init__(self, boxes=[], label='text', string=None):
        self.label=label
        if string is not None: self.from_str(string)
        else: self.boxes = boxes
    def check_valid(self):
        '''ensures no overlaps'''
        for i,b in enumerate(self.boxes):
            for j in range(i):
                assert(not self.boxes[i].overlap(b))
    def area(self): #TODO: memoize!
        return sum(b.area(weight_image) for b in self.boxes)
    def intersect(self, other):
        intersects = (bs.intersect(bo) for bs in self.boxes for bo in other.boxes)
        return Segment(i for i in intersects if i.area())
    def __str__(self):
        return self.label +'|'+ '|'.join(str(b) for b in self.boxes)
    def from_str(self, string):
        ss = string.split('|')
        self.label = ss[0]
        self.boxes = [Box(string=s) for s in ss[1:] if s]

    def create_jaccard(denom_func, docstring=None):
        '''returns a method to compute overlaps of form intersect/denominator'''
        def intersect_over(self, truth, denom_func):
            intersect = self.intersect(truth).area()
            return 0.0 if intersect==0.0 else \
                   intersect/denom_func(self, truth, intersect)
        intersect_over.__doc__ = docstring
        return intersect_over
    jaccard_precision = create_jaccard(lambda s,t,i: s.area(weight_image),
       docstring='''returns proportion of self's area also in truth's area''')
    jaccard_recall = create_jaccard(lambda s,t,i: t.area(weight_image),
       docstring='''returns proportion of truth's area also in self's area''')
    jaccard_similarity = create_jaccard(lambda s,t,i: s.area(weight_image)+t.area(weight_image)-i,
       docstring='''returns intersection area over union area''')
