'''@author Samuel Tenka
'''
class VerticalDominance:
    def __init__(self):
        pass
    def decide_geometry(self, truth, guess, newspage):
        for seg in (truth,guess):
            seg.attach_to(newspage)
    def precision(self, truth, guess, newspage=None):
        self.decide_geometry(truth,guess,newspage)
        return sum(max(ga.jaccard_precision(ta) for ga in guess.article_regions()) for ta in truth.article_regions()) / len(truth.articles)
    def recall(self, truth, guess, newspage=None):
        self.decide_geometry(truth,guess,newspage)
        return sum(max(ga.jaccard_recall(ta) for ga in guess.article_regions()) for ta in truth.article_regions()) / len(guess.articles)
    def fscore(self, newspage, truth, guess, beta=1.1):
        P = self.precision(newspage, truth, guess)
        R = self.recall(newspage, truth, guess)
        return (1+beta**2) * (P*R)/(beta**2*P + R)
