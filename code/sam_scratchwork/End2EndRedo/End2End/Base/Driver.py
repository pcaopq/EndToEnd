'''@author Samuel Tenka
'''

assert(__name__=='__main__')

from Config import Config
from Newspage import Newspage
import sys,
C = Config(config_name=sys.argv[1])

for newspage in C.get_newspages():
    for algo in C.get_algos():
        seg = algo.RUN(newspage)
        for metric in C.get_metrics():
            evalout = metric.EVALUATE(seg, groundtruth)
