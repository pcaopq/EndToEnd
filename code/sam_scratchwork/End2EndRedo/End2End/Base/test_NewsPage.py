'''@author Samuel Tenka
'''

import unittest
from NewsPage import NewsPage

class TestNewsPage(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        newspage = NewsPage('0003')
    def test_init(self):
        pass
if __name__=='__main__':
    unittest.main()
