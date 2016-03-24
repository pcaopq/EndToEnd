'''@author Samuel Tenka
'''
class Polygon:
    '''A `Polygon` is a region in the plane,
       represented as a disjoint union of Boxes.
    '''
    def __init__(self,boxes, is_disjoint=False):
        self.boxes=filter(boxes)
        if not is_disjoint: self.remove_internal_overlaps()
    def remove_internal_overlaps(self):
        '''Ensures disjointness of component boxes while preserving their union,
           thus `flattening away` any overlaps among component boxes.
        '''
        newboxes = []
        while self.boxes:
            b, self.boxes = self.boxes[0], self.boxes[1:]
            for nb in newboxes:
                if b.overlaps(nb):
                    self.boxes += b.refine(nb)
                    break
            else:
                newboxes.append(b)
        self.boxes=newboxes
    def union(self, other):
        '''Returns set of points in at least one input region, as a Polygon.'''
        return Polygon(self.boxes+other.boxes)
    def intersect(self, other):
        '''Returns set of points in both input regions, as a Polygon.'''
        return Polygon([bs.meet(bo) for bs in self.boxes for bo in other.boxes], is_disjoint=True)
    def remove(self, other):
        '''Shrinks `self` so as not to include points in `other`.'''
        self.boxes.append(None) #sentinel
        while True:
            b, self.boxes = self.boxes[0], self.boxes[1:]
            if b is None: break
            for bo in other.boxes:
                if not b.overlaps(bo): continue
                self.boxes += b.minus(bo)
            else:
                self.boxes.append(b)
    def area(self, newspage=None):
        '''Counts interior pixels, potentially weighted by pixel values.
           Optional argument `newspage` is of type NewsPage.
        '''
        return sum(b.area(newspage) for b in self.boxes)
    def overlaps(self, other):
        for bs in self.boxes:
            for bo in other.boxes:
                if bs.overlaps(bo): return True
        return False
