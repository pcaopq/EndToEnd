'''@author Samuel Tenka
VerticalDominance.py segments newspages by
   0. Reading textlines from XML
   1. Classifying textlines as Title or Text, based on fontsize
   2. Assigning Textlines to Titlelines
   3. Merging, for each Titleline, the set of all associated Textlines.
'''

class VerticalDominance:
    def __init__(self):
        pass
    def segment(self, newspage):
        self.read_textlines_from_metadata(newspage)
        self.identify_titlelines()
        self.merge_neighboring_titlelines()
        self.assign_articlelines_to_titlelines()
        self.merge_columns_of_articlelines()
    def read_textlines_from_metadata(self,newspage):
        print(newspage.xml.getTextLines())
    def identify_titlelines(self):
        pass
    def merge_neighboring_titlelines(self):
        pass
    def assign_articlelines_to_titlelines(self):
        pass
    def merge_columns_of_articlelines(self):
        pass

V = VerticalDominance()
X = NewsPage('0003')
V.segment(X)
