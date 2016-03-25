'''@author Samuel Tenka
'''

import unittest
from Box import Box
from Polygon import Polygon

class TestPolygon(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.square = Polygon([Box([[0,0],[100,100]])])
        self.corner = Polygon([Box([[50,0],[100,50]])]) #upper left corner
        self.others = Polygon([Box([[0,0],[50,50]]),
                               Box([[50,50],[100,100]]),
                               Box([[0,50],[50,100]])])
    def test_minus(self):
        smc = self.square.minus(self.corner)
        self.assertFalse(smc == self.square)
        self.assertFalse(smc == self.corner)
        self.assertTrue(smc == self.others)
if __name__=='__main__':
    unittest.main()
