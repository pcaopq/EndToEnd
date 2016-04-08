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

'''Design Question:
      (0) should we pass newspages down, or
      (1) should each box,polygon,article,and segmentation store (a ptr) to its newspage?
   (0) has the advantage that we can compute area *with or without*
   respect to the ground image.
   On the other hand,
   (1) has the advantage that we don't have to pass a newspage everytime
   we want to compute overlap etc.
   Does (1) have any competing advantages?
'''
#TODO: resolve above?
