'''@author Samuel Tenka
'''

import unittest
from Segmentation import Segmentation

class TestSegmentation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        s = Segmentation('test.json')
        s.write_to('test_out.json','test.jp2')
    def test_init(self):
        pass
if __name__=='__main__':
    unittest.main()
