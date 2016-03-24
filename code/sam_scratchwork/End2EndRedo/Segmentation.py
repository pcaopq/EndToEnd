'''@author Samuel Tenka
'''

class Segmentation:
    '''A `Segmentation`'''
    def __init__(self):
        self.articles = []
    def shrink(self):
        '''Ensures disjointness of component polygons
           (by removing all inter-polygon intersections).
        '''
        polygons = [p for a in self.articles for p in a.polygons_by_type.values()]
        intersections = {i:[] for i in range(len(polygons))}
        for i,p in enumerate(polygons):
            for j,pp in enumerate(polygons[:i]):
                if not p.overlaps(pp):
                    continue
                I = p.intersect(pp)
                intersections[i].append(I)
                intersections[j].append(I)
        for i,p in enumerate(polygons):
            


    def read_from(self, json):
        pass
    def write_to(self, json):
        pass
