from Box import Box
from Segments import Segment, Segmentation
import os

def get_evalpairs(path):
    ''''''
    files = list(os.listdir(path))
    getroot = lambda fname: '.'.join(fname.split('.')[:-2])
    return [getroot(fname) for fname in files if \
            fname.endswith('.demo.txt') and \
            getroot(fname)+'.demo_seg.txt' in files]

def analyzepair(path, root):
    with open(path+root+'.demo.txt') as f:
        GT = Segmentation(string=f.read())
    with open(path+root+'.demo_seg.txt') as f:
        S = Segmentation(string=f.read())
    print(root)
    pfs,pp,pr = S.pair_fscore(GT),S.pair_precision(GT),S.pair_recall(GT)
    print('   Pair FScore=%.3f'%pfs)
    print('      Pair Precision=%.3f'%pp)
    print('      Pair Recall=   %.3f'%pr)
    jfs,jp,jr = S.jaccard_fscore(GT, gamma=2.0),S.jaccard_precision(GT, gamma=2.0),S.jaccard_recall(GT, gamma=2.0)
    print('   Jacc FScore=%.3f'%jfs)
    print('      Jacc Precision=%.3f'%jp)
    print('      Jacc Recall=   %.3f'%jr)
    return (pfs,(pp,pr),jfs,(jp,jr))

def analyze_batch(path):
    pair_fscores = []
    pair_precision_v_recall = []
    jacc_fscores = []
    jacc_precision_v_recall = []
    for root in get_evalpairs(path):
        pfs,(pp,pr),jfs,(jp,jr) = analyzepair(path,root)
        pair_fscores.append(pfs); pair_precision_v_recall.append((pp,pr))
        jacc_fscores.append(jfs); jacc_precision_v_recall.append((jp,jr))
    return (pair_fscores, pair_precision_v_recall), (jacc_fscores, jacc_precision_v_recall)
    #print(pair_fscores, pair_precision_v_recall)
    #print(jacc_fscores, jacc_precision_v_recall)

path = 'C:\\Users\\Samuel\\Desktop\\ProquestNews2016\\Data\\'
(pair_fscores, pair_precision_v_recall), (jacc_fscores, jacc_precision_v_recall) = analyze_batch(path)

pair_fscores.sort()
jacc_fscores.sort()

from matplotlib import pyplot as plt
plt.scatter(x=[p for p,r in pair_precision_v_recall], y=[r for p,r in pair_precision_v_recall], c='blue')
plt.scatter(x=[p for p,r in jacc_precision_v_recall], y=[r for p,r in jacc_precision_v_recall], c='green')
plt.xlabel('precision')
plt.ylabel('recall')
plt.title('Precision and Recall Scores (blue=pair, green=jacc)')
plt.savefig('TEST.png')
plt.clf()
plt.plot([sum(pair_fscores[:i])/i for i in range(1,len(pair_fscores))], c='blue')
plt.plot([sum(jacc_fscores[:i])/i for i in range(1,len(jacc_fscores))], c='green')
plt.xlabel('avg fscore')
plt.ylabel('number elements')
plt.title('Avg FScore of worst n datapoints (blue=pair, green=jacc)')
plt.savefig('TEST2.png')
plt.clf()
