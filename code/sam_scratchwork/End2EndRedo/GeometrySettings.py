'''@author Samuel Tenka
'''

#TODO:
# perhaps place this as a global
# variable in Box.py?
#
class GeometrySettings:
    '''A single switch with which
       we can alter the behavior
       of a whole set of regions.
    '''
    def __init__(self):
        self.compute_areas_by_pixel_value = False
        self.newspage = None
