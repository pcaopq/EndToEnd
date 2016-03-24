'''@author Samuel Tenka
'''
from functools import reduce

class Box:
    def __init__(self, *args):
       '''A Box is a axis-aligned rectangle, initialized
          either from *(miny, minx, maxy, maxx)
          or from [[miny, minx], [maxy,maxx]].
          The latter form is also used for its internal representation.
          Its coordinates are in units of .jp2 pixels.
       '''
       if len(args)==4:
           miny, minx, maxy, maxx = args
           self.coors = [[miny, minx], [maxy, maxx]]
       else:
           assert(len(args)==1)
           self.coors = args[0]
       self.ensure_maxcoor_exceeds_mincoor_on_both_axes() #Notable documentation technique.
    def ensure_maxcoor_exceeds_mincoor_on_both_axes(self):
        self.coors[1] = [max(self.coors[i][j] for i in range(2)) for j in range(2)]
    def area(self, newspage=None):
        '''Counts interior pixels, potentially weighted by pixel values.
           Optional argument `newspage` is of type NewsPage.
        '''
        if newspage is not None:
            (miny, minx), (maxy, maxx) = self.coors
            return newspage.weight_on(miny, minx, maxy, maxx)
        return reduce(lambda y,x:y*x, (self.coors[1][i]-self.coors[0][i] for i in range(2)))
    def join(self, other):
        '''Smallest common container.'''
        return Box([[m(box.coors[i][j] for box in (self,other)) for j in range(2)] for i,m in enumerate((min,max))])
    def meet(self, other):
        '''Largest common containee, i.e. the intersection.
           Note: the case of null intersection will return an area-0 box.
        '''
        return Box([[m(box.coors[i][j] for box in (self,other)) for j in range(2)] for i,m in enumerate((max,min))])
    def __contains__(self, other):
        '''Checks whether `self` contains `other` as regions in the plane.'''
        return self == self.join(other)
    def __bool__(self):
        '''Positive-area boxes are True;
           infinitely-thin ones are False.
        '''
        return bool(self.area())
    def overlaps(self, other):
        '''Determines whether there is significant (i.e. nonzero) overlap.'''
        return bool(self.meet(other))
    def __eq__(self, other):
        '''Checks equality. Distinct points exist.'''
        return self.coors == other.coors

    def windmill(self):
        '''Returns a partition of the box's complement into 4 quarter-planes.
           This has applications to methods `minus` and (hence) `refine` below.'''
        (miny, minx), (maxy, maxx) = self.coors
        D0 = [[maxy,-inf],[inf,maxx]]
        D1 = [[-inf,-inf],[maxy,minx]]
        D2 = [[-inf,minx],[miny,inf]]
        D3 = [[miny,maxx],[inf,inf]]
        return (D0,D1,D2,D3) #TODO: can we express above more elegantly?
    def minus(self, other):
        '''Returns a partition of the points in `self` but not in `other`
           as a list (empty if self in other) of disjoint boxes.'''
        return filter(self.meet(D) for D in other.windmill())
    def refine(self, other):
        '''Returns a partition of the points in `self.join(other)`
           as a list of disjoint boxes, each:
           (in or disjoint from `self`) and (in or disjoint from `other`).
           This is useful for `flattening away` overlaps:
           see `Polygon.remove_internal_overlaps`
        '''
        if other in self: return [self]
        return [other] + self.minus(other)
