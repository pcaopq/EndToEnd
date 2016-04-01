'''@author Samuel Tenka
'''
class Jaccard:
    def __init__(self):
        pass
    def poly_precision(self, true_poly, true_poly):
        '''amount of self area also in truth's area'''
        intersect_area = self.intersect(truth).area()
        return 0 if not intersect_area else intersect_area/self.area()
    def precision(self, newspage, truth, guess):
        return sum(max(ga.jaccard_recall(ta) for ga in guess.articles()) for ta in truth.articles()) / len(truth.articles)
    def recall(self, newspage, truth, guess):
        return sum(max(ga.jaccard_recall(ta) for ga in guess.articles()) for ta in truth.articles()) / len(self.articles)
    def fscore(self, newspage, truth, guess, beta=1.0):
        P = self.precision(newspage, truth, guess)
        R = self.recall(newspage, truth, guess)
        return (1+beta**2) * (P*R)/(beta**2*P + R)
