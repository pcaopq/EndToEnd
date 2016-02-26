import numpy as np
import matplotlib.image as mpimg

class NewsImage:
    '''Processes image .jpgs and .xmls for evaluation pipeline.
       For example, pre-computes area blacknesses for more efficient
       evaluation.
    '''
    gamma_default = lambda x:1.0-(x/255.0)**2
    def __init__(self, root, gamma=gamma_default):
        '''The argument 'root' could be, for example, root='../Data/0005',
           on which we append '.jpg' and '.xml'.

           member functions:
           0. 'gamma' transforms a grayscale value into a blackness measure.
        '''
        self.filenames = {suffix:root+suffix for suffix in ('.jpg','.xml')}
        self.gamma = gamma
    def read_blackness(self):
        '''presumes .jpg to be grayscale; precomputes area blacknesses
           for more efficient evaluation
        '''
        self.blacknesses = self.gamma(mpimg.imread(self.filenames['.jpg']))
        self.blacknesses = np.cumsum(self.blacknesses, axis=0)
        self.blacknesses = np.cumsum(self.blacknesses, axis=1)
        print(self.blacknesses.shape)
    def get_total_blackness(self,y0,x0,y1,x1):
        # TODO: fix (should be four terms)
        return self.blacknesses[y1][x1]-self.blacknesses[y0][x0]
