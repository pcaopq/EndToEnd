''' Geometry of axis-aligned rectangles.
    For us, coordinates are length-2 lists of form [y, x].
'''

#TODO: something funny's goin' on here!

class Box:

    # add attribute label
    def __init__(self, coor0=None, coor1=None, string=None, label=None):
        '''0th coor is (miny,minx); 1th coor is (maxy,maxx)'''
        if string is not None: self.from_str(string)
        elif coor1 is None: self.from_point([0.0]*2 if coor0 is None else coor0)
        else: self.from_corners(coor0,coor1)

        if label is not None:
            self.label = label
    def center(self):
        return [sum(self.coors[i][j] for i in range(2))/2 for j in range(2)]
    def disconnect_distance(self, other):
        return max(far.coors[0][i]-near.coors[1][i] for i in range(2) for (far,near) in [(self,other),(other,self)])
    def overlaps(self, other): #TODO: check correctness!
        return self.disconnect_distance(other) < 0.0
    def join(self, other):
        return Box(*[[(min,max)[i](box.coors[i][j] for box in (self,other))
                       for j in range(2)] for i in range(2)])
    def intersect(self, other):
        if not self.overlaps(other): return Box([0.0,0.0], [0.0,0.0])
        return Box(string=str([[(max,min)[i](box.coors[i][j] for box in (self,other))
                       for j in range(2)] for i in range(2)]))
    def area(self):
        return float((self.coors[1][1]-self.coors[0][1]) *\
                     (self.coors[1][0]-self.coors[0][0]))
    def from_point(self, coor):
        self.coors = [coor[:]]*2
    def from_corners(self, coorA, coorB):
        transpose = list(zip(coorA,coorB))
        self.coors = [[(min,max)[i](t) for t in transpose] for i in range(2)]
    def __str__(self): return str(self.coors)
    def from_str(self, string):
        self.coors = eval(string)

    def print_box(self):
        print self.label, self.coors[0], self.coors[1]
