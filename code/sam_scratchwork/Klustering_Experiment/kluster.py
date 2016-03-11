'''
parses xml file of ocr'd string-location data:
   <String ID="TB.0005.2_0_0" STYLEREFS="TS_10.0" HEIGHT="156.0" WIDTH="448.0" HPOS="540.0" VPOS="1908.0" CONTENT="121st" WC="1.0"/>
and clusters
'''
import re
from math import sqrt
from random import random
from sys import stdout

from tkinter import *
master = Tk()

print('defining lambdas...')
p = re.compile('<String ID="(?P<stringid>[^"]*)" ' +
               'STYLEREFS="(?P<stylerefs>[^"]*)" ' +
               'HEIGHT="(?P<height>[^"]*)" ' +
               'WIDTH="(?P<width>[^"]*)" ' +
               'HPOS="(?P<hpos>[^"]*)" ' +
               'VPOS="(?P<vpos>[^"]*)" ' +
               'CONTENT="(?P<content>[^"]*)" ' +
               'WC="(?P<wc>[^"]*)"/>')

print('defining lambdas...')
with open('0005.xml') as f:
    text = f.read()
    getnum = lambda match, label: float(match.group(label))
    coordinates = [(getnum(m,'vpos')+0.5*getnum(m,'height'),
                    getnum(m,'hpos')+0.5*getnum(m,'width')) for m in p.finditer(text)]
    print('xml has %d characters, %d ocr points.' % (len(text), len(coordinates)))
xs = [[c[i] for c in coordinates] for i in range(2)]
miny, maxy, minx, maxx = min(xs[0]), max(xs[0]), min(xs[1]), max(xs[1])
print('vpos ranges in [%d,%d]; hpos ranges in [%d,%d]' % (miny, maxy, minx, maxx))

cnvs_h, cnvs_w = 480, 320
w = Canvas(master, height=cnvs_h, width=cnvs_w)
to_canvas = lambda coor: (cnvs_h * (coor[0]-miny)/(maxy-miny), cnvs_w * (coor[1]-minx)/(maxx-minx))
w.pack()

#kmeans klustering:
K = 60; N = len(coordinates); numsteps=40;
print('defining lambdas...')
randcoor = lambda : (random()*(maxy-miny)+miny, random()*(maxx-minx)+minx)
def dist(c0,c1):
    #print(c0, c1)
    return max(abs(c1[0]-c0[0]),abs(c1[1]-c0[1]))
#dist = lambda c0, c1: max(abs(c1[0]-c0[0]),abs(c1[1]-c0[1])) #sqrt((c1[0]-c0[0])**2+(c1[1]-c0[1])**2)
closest_cent = lambda centers, coor: min((dist(centers[i],coor), i) for i in range(K))[1]
def accumulate(c0, c1):
    c0[0] += c1[0]
    c0[1] += c1[1]
def acc_max(c0, c1):
    if c0 is None:
        c0 = c1[:]
        return
    c0[0] = max(c0[0], c1[0])
    c0[1] = max(c0[1], c1[1])
def acc_min(c0, c1):
    if c0 is None:
        c0 = c1[:]
        return
    c0[0] = min(c0[0], c1[0])
    c0[1] = min(c0[1], c1[1])
def scale(c, scale):
    return (c[0]*scale, c[1]*scale)

centers = [randcoor() for k in range(K)]
assignments = [closest_cent(centers, coor) for coor in coordinates] #not DRY!

STEP=0
def render():
   global centers,assignments, STEP
   w.delete('all')

   for j in range(5):
       print('step %d...' % STEP); stdout.flush(); STEP+=1
       kluster_sums = [[0.0,0.0] for i in range(K)]
       kluster_mins = [list(centers[i]) for i in range(K)]
       kluster_maxs = [list(centers[i]) for i in range(K)]
       counts = [0 for i in range(K)]
       for i in range(N):
           if random() < 9.0/10.0:
              accumulate(kluster_sums[assignments[i]], coordinates[i])
              acc_min(kluster_mins[assignments[i]], coordinates[i])
              acc_max(kluster_maxs[assignments[i]], coordinates[i])
              counts[assignments[i]] += 1
       #kluster_avgs = [((c0[0]+c1[0])/2,(c0[1]+c1[1])/2) for c0,c1 in zip(kluster_mins, kluster_maxs)]
       for i in range(K):
           centers[i] = randcoor() if counts[i]==0 else scale(kluster_sums[i], 1.0/counts[i])
           #centers[i] = randcoor() if counts[i]==0 else kluster_avgs[i]
       assignments = [closest_cent(centers, coor) for coor in coordinates]

   lvls = '00 CC 44 FF 88'.split()
   colors = ['#'+R+G+B for R in lvls for G in lvls for B in lvls]
   for i in range(K):
       y,x = to_canvas(centers[i])
       y0,x0 = to_canvas(kluster_mins[i])
       y1,x1 = to_canvas(kluster_maxs[i])
       w.create_rectangle(x0,y0,x1,y1, outline=colors[i], fill=colors[i], stipple='gray12')
   for i in range(N):
       y,x = to_canvas(coordinates[i])
       w.create_rectangle(x, y, x+1, y+1, outline=colors[assignments[i]])

   if STEP<100:
      w.after(100, render) #render 10 times a second

render()
mainloop()

#for i in range(numsteps):
