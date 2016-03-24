'''@author Samuel Tenka
'''

class Article:
    '''An `Article` is a pair of Polygons, often with one element empty,
       one representing a `title` region, another, a `text` region.
    '''
    def __init__(self, *args):
        '''Initialize from `title_polygon,text_polygon` (title comes earlier)
           or from a dictionary.'''
        if len(args)==2:
            title_polygons, text_polygons = args
            self.polygons_by_type = {'title':title_polygon, 'text':text_polygon}
        else:
            self.polygons_by_type = args
