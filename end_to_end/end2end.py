import os, sys
import Image
import matplotlib.pyplot as plt

sys.path.insert(0, './latex_generator')
from report_generator import *

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
            self.eval_results = {}

    def segment(self):
        for fname in self.files:
            print(fname)
            for imp_name in self.implementations:
                if not os.path.isfile(imp_name):
                    print 'invalid implementation file name'
                    continue
                command = 'python %s %s %s %s' % ((imp_name,) +
                      tuple(fname+ext for ext in ('','.xml','.json')))
<<<<<<< HEAD
                print command
=======
                #print('QWERTYUYTREWERTYUYTREWERTY',command)
>>>>>>> e7e622362568ee59c927e08269f5015387e28e96
                os.system(command)
    def evaluate(self):
        '''assumes format groundtruth - ....gt.json'''
        for fname in self.files:
            for metric_name in self.metrics:
                if not os.path.isfile(metric_name):
                    print 'invalid implementation file name'
                    continue
                command = 'python %s %s %s %s %s' % ((metric_name,) +
                      tuple(fname+ext for ext in ('.gt.json', '.json', '', '.xml')))
                print command
                os.system(command)

    def collect_data(self):
        for i, imp_name in enumerate(self.implementations):
            alg_result = {} # a dictionary contains precision, recall, score, history
            imp_pre, imp_rec, imp_score = 0.0, 0.0, 0.0
            eval_history = [] # precision, recall, score average for each image
            for fname in self.files:
                history_path = fname + '.evalout'
                if not os.path.isfile(history_path):
                    print 'no evaluation history', history_path
                    return

                img_pre, img_rec, img_score = 0.0, 0.0, 0.0
                with open(history_path) as f:
                    lines = f.read().rstrip().split('\n')
                    for line in lines:
                        numbers = line.split(' ')
                        img_pre += float(numbers[0])
                        img_rec += float(numbers[1])
                        img_score += float(numbers[2])
                    eval_history.append((img_pre / len(lines), img_rec / len(lines), \
                        img_score / len(lines)))
            
            # calculate the precision, recall, score average for each algorithm
            for r in eval_history:
                imp_pre += r[0]
                imp_rec += r[1]
                imp_score += r[2]
            imp_pre /= len(self.files)
            imp_rec /= len(self.files)
            imp_score /= len(self.files)

            eval_history = sorted(eval_history, key=lambda tup: tup[2])

            alg_result['precision'] = imp_pre
            alg_result['recall'] = imp_rec
            alg_result['score'] = imp_score
            alg_result['history'] = eval_history
            self.eval_results[imp_name] = alg_result
        print self.eval_results

    def plot_performance_curve(self):

        line_colors = ['r', 'g', 'b']
        plt.hold(True)
        for i, imp_name in enumerate(self.implementations):

            eval_history = self.eval_results[imp_name]['history']
            count = 0
            x = []
            y = []
            last_record = eval_history[0][2]
            for record in eval_history[1:]:
                count += 1
                if record[2] > last_record:
                    y.append(last_record)
                    last_record = record[2]
                    x.append(count)
            y.append(last_record)
            x.append(len(eval_history))

            for j in range(len(x)):
                x[j] /= float(len(eval_history))

            plt.plot(x,y)
            plt.xlabel('percentage of data')
            plt.ylabel('accuracy')
            plt.line = plt.plot(x, y, line_colors[i % len(line_colors)], label='performance curve')
            plt.legend(loc='upper left')
        plt.hold(False)
        plt.savefig('./performance.png')


    # generate the file in latex form to plot the graphs
    def generate_report(self):
        r = Report_generator('./latex_generator/template.tex', './latex_generator/report.tex')
        r.generate_report(self.implementations, self.eval_results)
        os.system('pdflatex ./latex_generator/report.tex')
        os.system('open ./report.pdf')

def main():
   config_filename = sys.argv[1]
   end_to_end = EndToEnd(config_filename)
   end_to_end.segment()
   end_to_end.evaluate()
   end_to_end.collect_data()
   end_to_end.plot_performance_curve()
   end_to_end.generate_report()

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
