'''implements kmeans clustering
   see Page.py : Page class
'''
from sys import stdout
from random import random

lvls = '00 CC 44 FF 88'.split() #not in order, for better color-contrast
colors = ['#'+R+G+B for B in lvls for G in lvls for R in lvls] #5**3==125 colors total
class KMeans:
    def __init__(self, K, page):
        print('initializing kmeans clusterer...'); stdout.flush()
        self.K=K
        self.page=page
        self.N=len(self.page.words)
        self.centers = [self.page.bb.random_pt_within() for k in range(K)]
        self.Estep() #initializes self.assignments, self.lens
    def Estep(self):
        self.assignments = [coor.closest_cent(self.centers) for coor in self.page.words]
        self.lens = [0]*self.N
        for i in range(self.N):
            self.lens[self.assignments[i]] += 1
    def Mstep(self):
        for i in range(self.K):
            c = self.centers[i]
            c.from_point(c.center())
        for i in range(self.N):
            #if random() < 50.0/(1+self.lens[i]): ##RANDOM!
            if random() < 3.0/10.0: ##RANDOM!
               self.centers[self.assignments[i]].join_with(self.page.words[i])
        for center in self.centers:
            if center.coors[0][0]==center.coors[1][0] or \
               center.coors[0][1]==center.coors[1][1]:
               center.from_point(self.page.bb.random_pt_within().coors[0])
    def draw_on(self, canvas, cbbcs):
        pbbcs = self.page.bb.coors
        for center,color in zip(self.centers, colors):
            center.draw_on(canvas, cbbcs, pbbcs, color, fill=color)
        for word,i in zip(self.page.words, range(len(self.page.words))):
            word.draw_on(canvas, cbbcs, pbbcs, colors[self.assignments[i]])
