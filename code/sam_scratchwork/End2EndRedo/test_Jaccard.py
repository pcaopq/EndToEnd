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
        self.assertEqual(1.00, self.jaccard.precision(self.truth, self.truth))
        self.assertEqual(1.00, self.jaccard.precision(self.guess, self.guess))
        self.assertEqual(0.75, self.jaccard.precision(self.truth, self.guess))
    def test_recall(self):
        self.assertEqual(1.00, self.jaccard.recall(self.truth, self.truth))
        self.assertEqual(1.00, self.jaccard.recall(self.guess, self.guess))
        self.assertEqual(0.75, self.jaccard.recall(self.truth, self.guess))

if __name__=='__main__':
    unittest.main()
