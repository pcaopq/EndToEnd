'''@author Samuel Tenka
'''
class Jaccard:
    def __init__(self, newspage, ground_truth, segmentation):
        self.newspage = newspage
        self.ground_truth = ground_truth
        self.segmentation = segmentation
        '''Design Question:
              (0) should we pass newspages down, or
              (1) should each box,polygon,article,and segmentation store (a ptr) to its newspage?
           (0) has the advantage that we can compute area *with or without*
           respect to the ground image.
           Does (1) have any competing advantages?
        '''
        #TODO: resolve above?    
