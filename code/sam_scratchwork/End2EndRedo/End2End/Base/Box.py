'''@author Samuel Tenka
'''
from functools import reduce
from GeometrySettings import GeometrySettings

default_geometry_setting = GeometrySettings()

class Box:
    def __init__(self, *args, geometry_settings=default_geometry_setting):
        '''A `Box` is a axis-aligned rectangle, initialized
           either from *(miny, minx, maxy, maxx)
           or from [[miny, minx], [maxy,maxx]].
           The latter form is also used for its internal representation.
           Its coordinates are in units of .jp2 pixels.
           Optional argument `newspage` is of type NewsPage;
           if this option is specified, area becomes weighted by black pixels.
        '''
        if len(args)==4:
            miny, minx, maxy, maxx = args
            self.coors = [[miny, minx], [maxy, maxx]]
        else:
            assert(len(args)==1); arg=args[0]
            assert(type(arg) in (type([]),type({})))
            if type(arg) is type({}): self.from_dict(arg)
            else: self.coors = arg
        self.geometry_settings = geometry_settings
        self.ensure_maxcoor_exceeds_mincoor_on_both_axes() #Notable documentation technique.
    def ensure_maxcoor_exceeds_mincoor_on_both_axes(self):
        self.coors[1] = [max(self.coors[i][j] for i in range(2)) for j in range(2)]
    def __repr__(self):
        '''String representation for debugging purposes.'''
        return str(self.coors)
    def area(self):
        '''Counts interior pixels, potentially weighted by pixel values.'''
        if self.geometry_settings.compute_areas_by_pixel_value:
            (miny, minx), (maxy, maxx) = self.coors
            return self.geometry_settings.newspage.weight_on(miny, minx, maxy, maxx)
        return reduce(lambda y,x:y*x, (self.coors[1][i]-self.coors[0][i] for i in range(2)))
    def join(self, other):
        '''Smallest common container.
           Geometry settings are inherited from leftmost operand.
        '''
        return Box([[m(box.coors[i][j] for box in (self,other)) for j in range(2)]
                   for i,m in enumerate((min,max))], geometry_settings=self.geometry_settings)
    def meet(self, other):
        '''Largest common containee, i.e. the intersection.
           Note: the case of null intersection will return an area-0 box.
           Geometry settings are inherited from leftmost operand.
        ''' #TODO: change null intersection case to return *None*
        return Box([[m(box.coors[i][j] for box in (self,other)) for j in range(2)]
                   for i,m in enumerate((max,min))], geometry_settings=self.geometry_settings)
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
        inf = float('inf')
        D0 = [[maxy,-inf],[inf,maxx]]
        D1 = [[-inf,-inf],[maxy,minx]]
        D2 = [[-inf,minx],[miny,inf]]
        D3 = [[miny,maxx],[inf,inf]]
        return tuple(Box(D, geometry_settings=self.geometry_settings) for D in (D0,D1,D2,D3)) #TODO: can we express above more elegantly?
    def minus(self, other):
        '''Returns a partition of the points in `self` but not in `other`
           as a list (empty if self in other) of disjoint boxes.'''
        return list(filter(None,(self.meet(D) for D in other.windmill())))
    def refine(self, other):
        '''Returns a partition of the points in `self.join(other)`
           as a list of disjoint boxes, each:
           (in or disjoint from `self`) and (in or disjoint from `other`).
           This is useful for `flattening away` overlaps:
           see `Polygon.remove_internal_overlaps`
        '''
        if other in self: return [self]
        return [other] + self.minus(other)

    def from_dict(self,json):
        y,x,h,w = (json[key] for key in ('y','x','height','width'))
        self.coors = [[y,x],[y+h,x+w]]
    def to_dict(self, article_id, content_class): #TODO: better name for `content_class` is `label`?
        '''content_class is `title` or `article`'''
        return {
            'id': str(article_id),
            'class': content_class,
            'y': self.coors[0][0],
            'x': self.coors[0][1],
            'height': self.coors[1][0]-self.coors[0][0],
            'width': self.coors[1][1]-self.coors[0][1],
            'type': 'rect'
        }
