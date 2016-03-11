import os

class EndToEnd:
   '''assumes segmentation algo.s take command line arguments as follows:
         python dilate_segmenter.py <imagename> <xmlname> <outname>
      e.g.
         python dilate_segmenter.py 0005.jp2 0005.xml 0005_seg.json
   '''
   def __init__(self, config_filename='config.txt'):
      with open(config_filename) as f:
         mydict = eval(f.read())
         self.metrics = mydict['Metrics']
         self.implementations = mydict['Implementations']
         self.files = mydict['Files']
   def segment(self):
      for fname in self.files:
         for imp_name in self.implementations:
            os.system('python %s %s %s' % (imp_name,) +
                      tuple(fname+ext for ext in ('.jpg','.xml','.json')))
   def evaluate(self):
      for fname in self.files:
         for imp_name in self.implementations:
            os.system('python %s %s %s' % (imp_name,) +
                      tuple(fname+ext for ext in ('.py','.xml','.json')))
