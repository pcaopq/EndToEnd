'''@author Samuel Tenka
'''

class Polygon:
    '''A `Polygon` is a region in the plane,
       represented as a disjoint union of Boxes.
    '''
    def __init__(self,boxes, is_disjoint=False):
        self.boxes=list(filter(None,boxes))
        if not is_disjoint: self.remove_internal_overlaps()
    def __repr__(self):
        '''String representation for debugging purposes.'''
        return 'P[%s]' % ', '.join(repr(b) for b in self.boxes)
    def remove_internal_overlaps(self):
        '''Ensures disjointness of component boxes while preserving their union,
           thus `flattening away` any overlaps among component boxes.
        '''
        newboxes = []
        while self.boxes:
            b, self.boxes = self.boxes[0], self.boxes[1:]
            for nb in newboxes:
                if not b.overlaps(nb): continue
                self.boxes += b.refine(nb)
                newboxes.remove(nb)
                break
            else:
                newboxes.append(b)
        self.boxes=newboxes
    def union(self, other, is_disjoint=False):
        '''Returns set of points in at least one input region, as a Polygon.'''
        return Polygon(self.boxes+other.boxes, is_disjoint)
    def intersect(self, other):
        '''Returns set of points in both input regions, as a Polygon.'''
        return Polygon([bs.meet(bo) for bs in self.boxes for bo in other.boxes], is_disjoint=True)
    def minus(self, other):
        '''Returns set of points in `self` but not in `other`, as a Polygon.
           Implemented recursively.
        '''
        oldboxes = self.boxes[:]
        newboxes = []
        while oldboxes:
            b, oldboxes = oldboxes[0], oldboxes[1:]
            for j,bo in enumerate(other.boxes):
                if not b.overlaps(bo): continue
                newboxes += Polygon(b.minus(bo)).minus(Polygon(other.boxes[j+1:])).boxes
                break
            else:
                newboxes.append(b)
        return Polygon(newboxes, is_disjoint=True)
    def remove(self, other):
        '''Shrinks `self` so as not to include any points in `other`.'''
        self.boxes = self.minus(other).boxes
    def area(self, newspage=None):
        '''Counts interior pixels, potentially weighted by pixel values.
           Optional argument `newspage` is of type NewsPage.
        '''
        return sum(b.area(newspage) for b in self.boxes)
    def __bool__(self):
        return bool(self.area())
    def overlaps(self, other):
        '''Checks whether a postive-area region of pixels lies in both polygons.
           Faster than `return bool(self.intersect(other))` when much overlap.
        '''
        for bs in self.boxes:
            for bo in other.boxes:
                if bs.overlaps(bo): return True
        return False
    def __eq__(self,other):
        return self.union(other).area()==self.intersect(other).area()
