'''parses xml file of ocr'd string-location data:
      <String ID="TB.0005.2_0_0" STYLEREFS="TS_10.0" HEIGHT="156.0" WIDTH="448.0" HPOS="540.0" VPOS="1908.0" CONTENT="121st" WC="1.0"/>
'''
from sys import stdout

import re
from Box import Box

p = re.compile('<String ID="(?P<stringid>[^"]*)" ' +
               'STYLEREFS="(?P<stylerefs>[^"]*)" ' +
               'HEIGHT="(?P<height>[^"]*)" ' +
               'WIDTH="(?P<width>[^"]*)" ' +
               'HPOS="(?P<hpos>[^"]*)" ' +
               'VPOS="(?P<vpos>[^"]*)" ' +
               'CONTENT="(?P<content>[^"]*)" ' +
               'WC="(?P<wc>[^"]*)"/>')

class Page:
    def __init__(self, filename):
        self.bb = Box((0,0),(0,0))
        self.words = []
        self.read_from(filename)
    def add_word(self, wordbox):
        self.words.append(wordbox)
        self.bb.join_with(wordbox)
    def read_from(self, filename):
        #print('reading [%s]...' % filename); stdout.flush()
        with open(filename) as f:
            getnum = lambda match, label: float(match.group(label))
            data = [(getnum(m,'vpos'),getnum(m,'hpos'),
                     getnum(m,'height'),getnum(m,'width')) for m in p.finditer(f.read())]
            for y,x,h,w in data:
               self.add_word(Box([y,x],[y+h,x+w]))
        #print('found %d ocr points...' % len(self.words)); stdout.flush()
        #print('y ranges in [%d,%d]; x ranges in [%d,%d].' %
        #      tuple(self.bb.coors[i][j] for j in range(2) for i in range(2))); stdout.flush()
