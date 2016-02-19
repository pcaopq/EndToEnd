''' Geometry of axis-aligned rectangles.
'''
from sys import stdout
from random import random

point_metric = lambda c0,c1: max(abs(c1[0]-c0[0]),abs(c1[1]-c0[1]))
class Box:
    def __init__(self, coor0=None, coor1=None):
        '''0th coor is (miny,minx); 1th coor is (maxy,maxx)'''
        if coor1 is None: self.from_point([None]*2 if coor0 is None else coor0)
        else: self.coors = [coor0,coor1]
    def draw_on(self, canvas, cbbcs, pbbcs, color='black', fill=''):
        '''cbbcs=canvas bounding box coors; pbbcs=page bounding box coors'''
        to_canvas = lambda coor: [cbbcs[1][i] * (coor[i]-pbbcs[0][i])/(pbbcs[1][i]-pbbcs[0][i]) for i in range(2)]
        y,x = to_canvas(self.coors[0])
        Y,X = to_canvas(self.coors[1])
        canvas.create_rectangle(x,y,X,Y, outline=color, fill=fill, stipple='gray12')
    def center(self):
        return [sum(self.coors[i][j] for i in range(2))/2 for j in range(2)]
    def disconnect_distance(self, other):
        return min(-other.coors[1][0] + self.coors[0][0],
                   other.coors[1][0] - self.coors[1][0],
                   -other.coors[1][1] + self.coors[0][1],
                   other.coors[1][1] - self.coors[1][1])
    def overlaps(self, other): #TODO: check correctness!
        return disconnect_distance(self, other) < 0.0
    def dist_to(self, other):
        return point_metric(self.center(),other.center()) +\
               max(0, self.disconnect_distance(other))
    def join_with(self, other):
        self.coors = [[(min,max)[i](box.coors[i][j] for box in (self,other))
                       for j in range(2)] for i in range(2)]
    def from_point(self, coor):
        self.coors = [coor[:]]*2
    def closest_cent(self, centers):
        return min((self.dist_to(centers[i]), i) for i in range(len(centers)))[1]
    def random_pt_within(self):
       return Box([random()*(self.coors[1][i]-self.coors[0][i])+self.coors[0][i] for i in range(2)])
