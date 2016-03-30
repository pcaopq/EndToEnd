'''@author Samuel Tenka
'''

import unittest
from JP2 import JP2

class TestJP2(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.rectangle = JP2('testjp2_rectangle.jpg')
        self.diamond = JP2('testjp2_diamond.jpg')
    def assert_weights_close(self, weight, target, area, thresh=0.05):
        error = (weight-target)/float(area)
        print(error)
        self.assertTrue(abs(error) < thresh)
    def test_weights(self):
        w_black_rect = self.rectangle.weight_on(60,60,120,120)
        self.assert_weights_close(w_black_rect, 60*60, 60*60)
        w_white_rect = self.rectangle.weight_on(120,120,180,180)
        self.assert_weights_close(w_white_rect, 0, 60*60)
        w_diamond = self.diamond.weight_on(0,0,256,256)
        self.assert_weights_close(w_diamond, (256*256)/2 - 128*128, 256*256)

if __name__=='__main__':
    unittest.main()
