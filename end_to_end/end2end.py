import os, sys
import Image
import matplotlib.pyplot as plt

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
                command = 'python %s %s %s %s' % ((imp_name,) +
                      tuple(fname+ext for ext in ('','.xml','.json')))
                os.system(command)
    def evaluate(self):
        '''assumes format groundtruth - ....gt.json'''
        for fname in self.files:
            for metric_name in self.metrics:
                os.system('python %s %s %s %s %s' % ((metric_name,) +
                      tuple(fname+ext for ext in ('.gt.json', '.json', '', '.xml'))))

    # def plot_performance_curve(self):

    #     for fname in self.files:
    #         history_path = fname + '.evalout'
    #         if not os.path.isfile(history_path):
    #             print 'no evaluation history', history_path
    #             return

    #         with open(history_path) as f:
    #             pre, rec, 
    #             for line in f.read().rstrip().split('\n'):
    #                 numbers = line.split(' ')
    #                 self.eval_history.append((float(numbers[0]), float(numbers[1]), float(numbers[2])))
    #         self.eval_history = sorted(self.eval_history, key=lambda tup: tup[2])
    #         count = 0
    #         x = []
    #         y = []
    #         last_record = self.eval_history[0][2]
    #         for record in self.eval_history[1:]:
    #             count += 1
    #             if record[2] > last_record:
    #                 y.append(last_record)
    #                 last_record = record[2]
    #                 x.append(count)
    #         y.append(last_record)
    #         x.append(len(self.eval_history))

    #         for i in range(len(x)):
    #             x[i] /= float(len(self.eval_history))

    #         plt.plot(x,y)
    #         plt.xlabel('percentage of data')
    #         plt.ylabel('accuracy')
    #         plt.line = plt.plot(x,y, label='performance curve')
    #         plt.legend(loc='upper left')
    #         plt.savefig('./performance.png')

def main():
   config_filename = sys.argv[1]
   end_to_end = EndToEnd(config_filename)
   end_to_end.segment()
   end_to_end.evaluate()

if __name__ == '__main__':
   main()



'''
A_0, A_1, ...

A_1 := A_1 minus A_0
A_2 := (A_2 minus A_1) minus A_0
.
.
.


'''