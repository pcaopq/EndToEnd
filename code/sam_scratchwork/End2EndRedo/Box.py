'''@author Samuel Tenka
'''
from functools import reduce

class Box:
    def __init__(self, *args):
       '''A Box is a axis-aligned rectangle.
          Its coordinates are in units of .jp2 pixels.
       '''
       if len(args)==1:
           self.coors = args[0]
       else:
           miny, minx, maxy, maxx = args
           self.coors = [[miny, minx], [maxy, maxx]]
       #ensure maxcoor>=mincoor on both axes:
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
        '''smallest common container'''
        return Box([[m(box.coors[i][j] for box in (self,other)) for j in range(2)] for i,m in enumerate((min,max))])
    def meet(self, other):
        '''largest common containee, i.e. the intersection
           Note: the case of null intersection will return an area-0 box.
        '''
        return Box([[m(box.coors[i][j] for box in (self,other)) for j in range(2)] for i,m in enumerate((max,min))])
    def overlaps(self, other):
        '''determines whether there is significant (i.e. nonzero) overlap'''
        return self.meet(other).area() != 0.0
    def __eq__(self, other):
        '''checks equality'''
        return self.coors == other.coors
