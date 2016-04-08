'''@author Samuel Tenka
'''

import unittest
from Metrics.Jaccard import Jaccard
from Segmentation import Segmentation
from NewsPage import NewsPage

class TestJaccard(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
    @classmethod
    def setUpClass(cls):
        cls.truth = Segmentation('metric_test_truth.json')
        cls.guess = Segmentation('metric_test_guess.json')
        cls.jaccard = Jaccard()
        print('##')
        cls.blank = NewsPage('blank_small')
        cls.black = NewsPage('black_small')
        cls.block_top = NewsPage('block_top_small')
        cls.block_bottom = NewsPage('block_bottom_small')
        print('##!')
    @classmethod
    def tearDownClass(cls):
        del cls.blank
    def assert_close(self, a, b, thresh=0.05):
        self.assertTrue(abs((a-b)/b) < thresh)
    def test_reflexivity(self):
        for metric in (self.jaccard.precision, self.jaccard.recall):
            for seg in (self.truth, self.guess):
                self.assertEqual(1.00, metric(seg, seg))
    def test_precision(self):
        self.assert_close(0.75, self.jaccard.precision(self.truth, self.guess))
        self.assert_close(0.75,self.jaccard.precision(self.truth, self.guess, self.blank))
        self.assert_close(0.75,self.jaccard.precision(self.truth, self.guess, self.black))
        self.assert_close(1.00,self.jaccard.precision(self.truth, self.guess, self.block_top)) #imprecision masked away
        self.assert_close(0.75,self.jaccard.precision(self.truth, self.guess, self.block_bottom))
    def test_recall(self):
        self.assert_close(0.75, self.jaccard.recall(self.truth, self.guess))
        self.assert_close(0.75,self.jaccard.recall(self.truth, self.guess, self.blank))
        self.assert_close(0.75,self.jaccard.recall(self.truth, self.guess, self.black))
        self.assert_close(0.75,self.jaccard.recall(self.truth, self.guess, self.block_top))
        self.assert_close(1.00,self.jaccard.recall(self.truth, self.guess, self.block_bottom)) #imperfect recall masked away
if __name__=='__main__':
    unittest.main()
