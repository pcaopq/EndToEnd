'''@author Samuel Tenka
'''

from collections import defaultdict

from Box import Box
from Polygon import Polygon
from Article import Article
from GeometrySettings import GeometrySettings

class Segmentation:
    '''A `Segmentation`'''
    def __init__(self, json_name=None):
        self.geometry_settings = GeometrySettings()
        self.articles = []
        if json_name is not None:
            self.read_from(json_name)
    def shrink(self):
        '''Ensures disjointness of component polygons
           (by removing all inter-polygon intersections).
           Called by some metrics.
        '''
        polygons = [p for a in self.articles for p in a.polygons_by_type.values()]
        intersections = {i:[] for i in range(len(polygons))}
        for i,p in enumerate(polygons):
            for j,pp in enumerate(polygons[:i]):
                if not p.overlaps(pp): continue
                I = p.intersect(pp)
                intersections[i].append(I)
                intersections[j].append(I)
        print(intersections)
        for i,p in enumerate(polygons):
            for ii in intersections[i]:
               p.remove(ii)
    def read_from(self, json_name):
        with open(json_name) as f:
            json = eval(f.read())
        boxlists_by_idclass = defaultdict(lambda: defaultdict(list)) #unknown key will map to empty list
        for d in json[0]['annotations']:
            boxlists_by_idclass[d['id']][d['class']].append(Box(d,geometry_settings=self.geometry_settings))
        self.articles = [Article({c:Polygon(bl) for c,bl in cbl.items()}) for i,cbl in boxlists_by_idclass.items()]
    def write_to(self, json_name, image_name):
        json = [{'annotations': [b.to_dict(article_id=i, content_class=c)
                                 for i,a in enumerate(self.articles)
                                 for c,p in a.polygons_by_type.items()
                                 for b in p.boxes],
                 'class':'image',
                 'filename': image_name
                }] #perhaps have an filename_class?
        with open(json_name,'w') as f:
            f.write(str(json).replace("'",'"')
                             .replace(', ', ',\n\t')
                             .replace('{', '{\n\t')
                             .replace('}', '\n}')
                             .replace('[', '[\n')
                             .replace(']', '\n]'))
