'''@author Samuel Tenka
'''

class Article:
    '''An `Article` is a pair of Polygons, often with one element empty,
       one representing a `title` region, another, a `text` region.
    '''
    def __init__(self, text_polygons, title_polygons):
        self.polygons_by_type = {'text':text_polygon, 'title':title_polygon}
