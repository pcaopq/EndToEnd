'''@author Samuel Tenka
'''

from collections import defaultdict

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
            for ii in intersections(p):
               p.remove(ii)
    def read_from(self, json_name):
        with open(json_name) as f:
            json = eval(f.read())
        boxlists_by_idclass = defaultdict(list) #unknown key will map to empty list
        for d in json['annotations']:
            boxlists_by_idclass[(d['id'],d['class'])].append(Box(d))
    def write_to(self, json_name, image_name):
        json = [{'annotations': [b.to_dict(article_id=i, content_class=c)
                                 for i,a in enumerate(self.articles)
                                 for c,p in a.polygons_by_type.keys()
                                 for b in p.boxes]
                 'class':'image'
                 'filename': image_name
                }] #perhaps have an filename_class?
        with open(json_name,'w') as f:
            f.write(str(json))
