'''@author Samuel Tenka
'''

from Newspage import Newspage
import imp

class Config:
    def __init__(self, config_name):
        with open(config_name) as f:
            self.config_dict = eval(f.read())

        self.algos = {algo_name: imp.load_source(algo_name.split('/')[-1], algo_name)
                      for algo_name in self.config_dict['Algorithms']}
        self.metrics = {metric_name: imp.load_source(metric_name.split('/')[-1], metric_name)
                      for metric_name in self.config_dict['Metrics']}
    def get_algos(self):
        return self.algos
    def get_metrics(self):
        return self.metrics
    def get_newspages(self):
        for newspage_name in self.config_dict['Newspages']:
            yield Newspage(newspage_name)
