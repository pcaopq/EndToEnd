'''@author Samuel Tenka
'''
class Jaccard:
    def __init__(self):
        pass
    def precision(self, truth, guess, newspage=None):
        return sum(max(ga.jaccard_recall(ta) for ga in guess.article_regions()) for ta in truth.article_regions()) / len(truth.articles)
    def recall(self, truth, guess, newspage=None):
        return sum(max(ga.jaccard_recall(ta) for ga in guess.article_regions()) for ta in truth.article_regions()) / len(self.articles)
    def fscore(self, newspage, truth, guess, beta=1.0):
        P = self.precision(newspage, truth, guess)
        R = self.recall(newspage, truth, guess)
        return (1+beta**2) * (P*R)/(beta**2*P + R)
