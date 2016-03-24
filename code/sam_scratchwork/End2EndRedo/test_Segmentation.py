'''@author Samuel Tenka
'''

import unittest
from Segmentation import Segmentation

class TestBox(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        s = Segmentation('test.json')
    def test_init(self):
        pass
if __name__=='__main__':
    unittest.main()
