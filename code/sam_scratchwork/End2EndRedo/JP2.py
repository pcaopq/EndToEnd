'''@author Samuel Tenka
'''

import numpy as np
import matplotlib.image as mpimg

class JP2:
    gamma_default = lambda x: (1.0-x/(3*256.0))**2 #whitens greys; white-->epsilon>0
    def __init__(self, image_name, gamma=gamma_default):
        self.image_name = image_name
        self.gamma = gamma
        self.compute_weights()
    def compute_weights(self):
        '''presumes .jpg to be grayscale; precomputes area blacknesses
           for more efficient evaluation
        '''
        print('Computing image [%s] weights...' % self.image_name)
        self.weight = mpimg.imread(self.image_name)
        self.weight = self.gamma(np.sum(self.weight, axis=2)) # convert to grayscale
        self.weight = np.cumsum(self.weight, axis=0)
        self.weight = np.cumsum(self.weight, axis=1)
    def weight_on(self, miny, minx, maxy, maxx):
        maxx-=1; maxy-=1;
        return self.weight[maxy][maxx] - self.weight[miny][maxx] \
                                       - self.weight[maxy][minx] + self.weight[miny][minx]
