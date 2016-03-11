import operator as op
import functools as fn
import itertools as it

'''
1 is a 'coordinate'
[1,2] is a point
[[1,2],[3,4]] is a box
'''

class Box:
    ''' A box is an axis-aligned rectangle, represented by [mincoors, maxcoors]
        For us, coordinates are length-2 lists of form [y, x], in units of
        pixels of the original image.
    '''
    zerobox = Box([0.0,0.0], [0.0,0.0])
    def __init__(self, coor0=None, coor1=None, string=None):
        '''The 0th coor is [miny,minx]; 1st coor is [maxy,maxx];
           we may also initialize from a string, e.g. '[[1.0,0.0],[2.0,3.0]]'.
           If only coor0 is specified, then a point [coor0,coor0] is created.

           Member variables:
           0. coors represents coordinates, e.g. [[1.0,0.0],[2.0,3.0]].
        '''
        if string is not None: self.from_str(string)
        elif coor1 is None: self.from_point([0.0]*2 if coor0 is None else coor0)
        else: self.from_corners(coor0,coor1)

    def from_point(self, coor):
        '''initializes box as breadthless, lengthless, and
           centered at the inputted coordinate
        '''
        self.points = [coor[:]]*2
    def from_corners(self, coorA, coorB):
        '''Constructs the box from any two nonadjacent corners, in any order.
           Canonicalizes the coordinates into [mincoors,maxcoors] form.
        '''
        self.points = [[(min,max)[i](t) for axis_vals in list(zip(coorA,coorB))]
                      for i in range(2)]
    def flatten(self):
        '''converts internal [[miny,minx],[maxy,maxx]] into [miny,minx,maxy,maxx]
        '''
        return [coordinate for point in self.points for coordinate in points]
    def __str__(self):
        '''string representation of box is simply that of its coordinates,
           e.g. '[[1.0,0.0],[2.0,3.0]]'
        '''
        return str(self.points)
    def from_str(self, string): #TODO: allow easy corrections for height/width / scale tranformations
        self.points = eval(string)

    def area(self, image=None):
       '''returns image area, weighted by image-values if an image is given'''
       if image is not None:
           return image.get_total_blackness(*itertools.chain(*self.points))
       return fn.reduce(op.mul,(axis_vals[1]-axis_vals[0]
                                for axis_vals in zip(self.points)), 1.0)
    def center(self):
        '''returns [centery,centerx]'''
        return [sum(axis_vals)/2 for axis_vals in zip(self.points)]

    def disconnect_distance(self, other):
        '''returns the largest possible rectangle --- infinite in one of
           the vertical or horizontal directions --- that separates the
           two boxes. if the boxes overlap, this margin will be negative.
        '''
        return max(far.coors[0][i]-near.coors[1][i] for i in range(2)
                   for (far,near) in [(self,other),(other,self)])
    def overlaps(self, other): #TODO: check correctness!
        '''Returns whether do the boxes share geometric area strictly greater than 0?
           We don't consider image-values here.
        '''
        return self.disconnect_distance(other) < 0.0

    def join(self, other):
        '''returns the smallest box containing both inputs'''
        return Box(*[[(min,max)[i](box.points[i][j] for box in (self,other))
                      for j in range(2)] for i in range(2)])
    def intersect(self, other):
        '''returns the largest box contained in both inputs,
           or else the [[0,0],[0,0]] box if there's no shared area'''
        if not self.overlaps(other): return zerobox
        return Box(*[[(max,min)[i](box.points[i][j] for box in (self,other))
                      for j in range(2)] for i in range(2)]))
