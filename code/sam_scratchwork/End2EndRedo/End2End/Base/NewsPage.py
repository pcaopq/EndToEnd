'''@author Samuel Tenka
'''

from JP2 import JP2
from XML import XML

class NewsPage:
    def __init__(self, root):
        self.jp2 = JP2(root+'.jpg')
        self.xml = XML(root+'.xml')
    def weight_on(self, *args):
        return self.jp2.weight_on(*args)
