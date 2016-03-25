'''@author Samuel Tenka
'''

import numpy as np
import matplotlib.image as mpimg

class JP2:
    gamma_default = lambda x: 1.0-(x/255.0)**2
    def __init__(self, image_name, gamma=gamma_default):
        self.image_name = image_name
        self.gamma = gamma
        self.compute_weights()
    def compute_weights(self):
        '''presumes .jpg to be grayscale; precomputes area blacknesses
           for more efficient evaluation
        '''
        self.weight = self.gamma(mpimg.imread(self.image_name))
        self.weight = np.cumsum(self.weight, axis=0)
        self.weight = np.cumsum(self.weight, axis=1)
    def weight_on(self, miny, minx, maxy, maxx):
        return weight[maxy][maxx] - weight[miny][maxx] \
                                  - weight[maxy][minx] + weight[miny][minx]
J = JP2('0003.jpg')
