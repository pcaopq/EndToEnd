from Box import Box
from Page import Page
from myFFT import FFT, periodicity
#from KMeans import KMeans

def histogram_of(filename, axis=1, oversample=1, num_bins=1024):
    '''num_bins must be power of 2'''
    mypage = Page(filename)
    get_xs = lambda mybox: tuple(mybox.coors[i][axis] for i in range(2))

    histogram = [0 for i in range(oversample*num_bins)]
    xstart, xend = get_xs(mypage.bb)
    to_bin = lambda x: int(num_bins*float(x-xstart)/(xend-xstart))
    for w in mypage.words:
        xmin, xmax = get_xs(w)
        for i in range(to_bin(xmin), to_bin(xmax)): #off-by-1?
            histogram[i] += 1

    histogram = [sum(histogram[i*oversample:(i+1)*oversample]) for i in range(num_bins)]
    s = sum(histogram)
    if s==0: return None #return -1 #article has no text
    return [float(h)/s for h in histogram]

def FFT_columnation_of(histogram):
    return periodicity(histogram)
def var_columnation_of(histogram):
    return 1.0/sum((h-1.0/len(histogram))**2 for h in histogram)

import os, sys
from matplotlib import pyplot as plt
path = "C:\\Users\\Samuel\\Desktop\\Batch 1\\Batch 1\\sn85042289\\15032502570\\1961110101\\"
files = [] #(columnation score, filename, histogram) tuples
for f in (f for f in os.listdir(path) if len(f)==len('0000.xml') and f.endswith(".xml")):
   print('processing %s...' %f); sys.stdout.flush()
   hs = [histogram_of(path+f,axis) for axis in range(2)]
   if hs[0] is None or hs[1] is None: continue
   vcs = [var_columnation_of(h) for h in hs]
   score = vcs[1]#+vcs[0]
   files.append((score,vcs,f,hs))

files.sort()
for (s,cs,f,hs),i in zip(files,range(len(files))):
   print('writing %s...' %f); sys.stdout.flush()
   plt.plot(hs[1]) #plt.plot(FFT(h))
   #plt.hist(hs[0],bins=64,orientation='horizontal') #plt.plot(FFT(h))
   plt.title('%s: columnation=%f, row uniformity=%f'%(f,cs[0],cs[1]))
   plt.savefig('%d_plot_%s.png' % (i,f))
   plt.clf()
