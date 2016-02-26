import sys, os
sys.path.insert(0, './latex_generator')

from Segmentation import Segmentation
import re
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from report_generator import *
from readJSON import *

NUM_CLASS = 3 # the number of classes, including title, text and other
ONETOONE_THRESHOLD = 0.85 # a specific manually decided threshold to classify each segmentation
ONETOMANY_THRESHOLD  = 0.1 # a specific manually decided threshold to classify each segmentation
LABELS = ['text', 'title', 'other']

class EvalOneToMany:
	
	# path
	image_path = './images/0005.jpg'
	segmentation_path = './images/0005.jpg.demo_full.txt'
	ground_truth_path = './images/0005.jpg.demo_full.txt'

	image = None

	# record the accuracy data
	eval_history = []

	# initialize the model. load the image
	# ground_truth and seg_to_eval are both Segmentation class objects
	def __init__(self, gt_path, seg_path, img_path=None, xml_path=None):

		if img_path is not None:
			self.image_folder = img_path
			self.image = mpimg.imread(img_path)
		else:
			self.image = mpimg.imread(self.image_path)
		self.ground_truth = seg_from_json(gt_path)
		self.seg_to_eval = seg_from_json(seg_path)

	def evaluate(self):
		# user can provide either the segmentation blocks or the segmentation file path

		N = [0.0] * NUM_CLASS # number of blocks for each class in ground truth
		M = [0.0] * NUM_CLASS # number of blocks for each class in guess
		one2one = [0.0] * NUM_CLASS # number of blocks which has a score larger than 0.85
		g_one2many = [0.0] * NUM_CLASS # number of ground truth segmentation that matches to more than one detection segmentation
		g_many2one = [0.0] * NUM_CLASS # number of ground truth segmentation that more than one matches to the same one detections
		d_one2many = [0.0] * NUM_CLASS # number of detection segmentation that matches to more than one ground truth segmentation
		d_many2one = [0.0] * NUM_CLASS # number of detection segmentation that more than one matches to the same one segmentation
		det = [0.0] * NUM_CLASS # detection rate (recall)
		rec = [0.0] * NUM_CLASS # recognition accuracy (precision)


		score = [None] * len(self.ground_truth.segs)
		for i in range(len(score)):
			score[i] = [0.0] * len(self.seg_to_eval.segs)

		# computing score table
		for j, g in enumerate(self.ground_truth.segs):
			ok=0
			for k, s in enumerate(self.seg_to_eval.segs):
				score[j][k] = s.jaccard_similarity(g)
				if score[j][k]==1.0:
				    if j!=k:
					   NSM, REC, DET = 0,0,0
					   self.eval_history.append((REC, DET, NSM))
					   print NSM, REC, DET # final score, precision, recall
					   return
				    ok=1
			if not ok:
				NSM, REC, DET = 0,0,0
				self.eval_history.append((REC, DET, NSM))
				print NSM, REC, DET # final score, precision, recall
				return
		
		NSM,REC,DET=1,1,1
		print NSM, REC, DET # final score, precision, recall

		self.eval_history.append((REC, DET, NSM))

	def MatchScore(self, Box1, Box2, use_black_pixel=False):
		# compute the jaccard coefficient of two blocks

		if Box1.coors[1][0] <=  Box2.coors[0][0] or Box1.coors[1][1] <=  Box2.coors[0][1] \
			or Box1.coors[0][0] >=  Box2.coors[1][0] or Box1.coors[0][1] >=  Box2.coors[1][1] \
			or Box1.label != Box2.label:
			return 0

		if not use_black_pixel:
			width = min(Box1.coors[1][0], Box2.coors[1][0]) - max(Box1.coors[0][0], Box2.coors[0][0])
			height = min(Box1.coors[1][1], Box2.coors[1][1]) - max(Box1.coors[0][1], Box2.coors[0][1])
			overlap = width * height
			sr = (Box1.coors[1][0] - Box1.coors[0][0]) * (Box1.coors[1][1] - Box1.coors[0][1])
			sg = (Box2.coors[1][0] - Box2.coors[0][0]) * (Box2.coors[1][1] - Box2.coors[0][1])
			return overlap / (sr + sg - overlap)
		else:
			#implementation of black pixel
			overlap = 0.0 #area of intesection of two segments
			sr = 0.0 # area of detection segments
			sg = 0.0 # area of ground truth segments
			for i in range(int(max(Box1.coors[0][0], Box2.coors[0][0])), int(min(Box1.coors[1][0], Box2.coors[1][0]))):
				for j in range(int(max(Box1.coors[0][1], Box2.coors[0][1])), int(min(Box1.coors[1][1], Box2.coors[1][1])), ):
					if self.image[i][j] >= 127.5:
						overlap += 1
			for i in range(int(Box1.coors[0][0]), int(Box1.coors[1][0])):
				for j in range(int(Box1.coors[0][1]), int(Box1.coors[1][1])):
					if self.image[i][j] >= 127.5:
						sr += 1
			for i in range(int(Box2.coors[0][0]), int(Box2.coors[1][0])):
				for j in range(int(Box2.coors[0][1]), int(Box2.coors[1][1])):
					if self.image[i][j] >= 127.5:
						sg += 1
			return overlap / (sr + sg - overlap)

	def clear_history(self):
		self.eval_history = []

	def plot_performance_curve(self):

		# plot the performance curve, the x axis 
		if len(self.eval_history) == 0:
			print 'no evaluation history'
			return
		self.eval_history = sorted(self.eval_history, key=lambda tup: tup[2])
		count = 0
		x = []
		y = []
		last_record = self.eval_history[0][2]
		for record in self.eval_history[1:]:
			count += 1
			if record[2] > last_record:
				y.append(last_record)
				last_record = record[2]
				x.append(count)
		y.append(last_record)
		x.append(len(self.eval_history))

		for i in range(len(x)):
			x[i] /= float(len(self.eval_history))

		plt.plot(x,y)
		plt.xlabel('percentage of data')
		plt.ylabel('accuracy')
		plt.line = plt.plot(x,y, label='performance curve')
		plt.legend(loc='upper left')
		plt.savefig('./performance.png')

	def plot_result(self):
		plt.imshow(self.image, cmap = plt.get_cmap('gray'))
		plt.show()

	# generate the file in latex form to plot the graphs
	def generate_report(self):
		r = Report_generator('./latex_generator/template.tex', './latex_generator/report.tex')
		r.generate_report(self.eval_history)
		os.system('pdflatex ./latex_generator/report.tex')
		os.system('open ./report.pdf')

def main():
	gt_path, seg_path, img_path, xml_path = sys.argv[1:5]

	evaluator = EvalOneToMany(gt_path, seg_path, img_path, xml_path)
	evaluator.evaluate()
	# evaluator.plot_performance_curve()
	# eval.generate_report()

if __name__ == '__main__':
	main()
