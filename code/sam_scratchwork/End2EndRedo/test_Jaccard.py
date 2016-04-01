'''@author Samuel Tenka
'''

import unittest
from Metrics.Jaccard import Jaccard
from Segmentation import Segmentation
#from NewsPage import NewsPage

class TestJaccard(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.truth = Segmentation('metric_test_truth.json')
        self.guess = Segmentation('metric_test_guess.json')
        self.jaccard = Jaccard()
        self.newspage = None #Newspage(root)
    def test_precision(self):
        print(self.jaccard.precision(self.truth, self.truth))
        print(self.jaccard.precision(self.guess, self.guess))
        print(self.jaccard.precision(self.truth, self.guess))

        #self.assertEqual(self.zero, self.badzero)
        #self.assertEqual(self.zero, self.fancyzero)
        #self.assertEqual(self.zero, self.fancybadzero)

if __name__=='__main__':
    unittest.main()
