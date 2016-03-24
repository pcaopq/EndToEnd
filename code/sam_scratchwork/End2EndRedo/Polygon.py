'''@author Samuel Tenka
'''
class Polygon:
    def __init__(self,boxes):
        self.boxes=filter(boxes)
        self.remove_internal_overlaps()
    def remove_internal_overlaps(self):
        '''ensures disjointness of component boxes while preserving their union.'''
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
        '''returns set of points in at least one input region, as a Polygon'''
        return Polygon(self.boxes+other.boxes)
    def intersect(self, other):
        '''returns set of points in both input regions, as a Polygon'''
        return Polygon([bs.meet(bo) for bs in self.boxes for bo in other.boxes])
    def area(self, newspage=None):
        '''Counts interior pixels, potentially weighted by pixel values.
           Optional argument `newspage` is of type NewsPage.
        '''
        return sum(b.area(newspage) for b in self.boxes)
