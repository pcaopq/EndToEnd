import sys, os
sys.path.insert(0, './latex_generator')

from Box import Box
import re
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from report_generator import *

NUM_CLASS = 3 # the number of classes, including title, text and other
ONETOONE_THRESHOLD = 0.85 # a specific manually decided threshold to classify each segmentation
ONETOMANY_THRESHOLD  = 0.1 # a specific manually decided threshold to classify each segmentation
LABELS = ['text', 'title', 'other']

class EvalOneToMany:
	
	# path
	image_path = './images/0005.jpg'
	segmentation_path = './images/0005.jpg.demo_full.txt'
	ground_truth_path = './images/0005.jpg.demo_full.txt'

	seg_blocks = []
	gt_blocks = []

	image = None

	# record the accuracy data
	eval_history = []

	# initialize the model. load the image
	def __init__(self, img_path=None, gt_path=None):
		if img_path is not None:
			self.image_folder = img_path
			self.image = mpimg.imread(img_path)
		else:
			self.image = mpimg.imread(self.image_path)

		if gt_path is not None:
			self.ground_truth_folder = gt_path
			self.gt_blocks = self.read_segmentation(gt_path)
		else:
			self.gt_blocks = self.read_segmentation(self.ground_truth_path)

	# read the segmentation coordinates and label from files
	def read_segmentation(self, f_path):
		blocks = []
		with open(f_path) as f:
			lines = f.readlines()
			for line in lines:
				label_and_block = line.split('|')
				label = label_and_block[0]

				for i in range(1, len(label_and_block)):
					coords = re.sub(r'[\[\],]', '', label_and_block[i]).rstrip().split(' ')
					coord0 = [float(coords[0]), float(coords[1])] #coordinates 1
					coord1 = [float(coords[2]), float(coords[3])] #coordinates 2
					box = Box(coord0, coord1, None, label)
					blocks.append(box)
		return blocks

	def evaluate(self, seg_blocks=None, seg_path=None, use_black_pixel=False):
		# user can provide either the segmentation blocks or the segmentation file path
		if seg_blocks is None:
			if seg_path is None:
				return 0
			seg_blocks = self.read_segmentation(seg_path)
		N = [0.0] * NUM_CLASS # number of blocks for each class in ground truth
		M = [0.0] * NUM_CLASS # number of blocks for each class in guess
		one2one = [0.0] * NUM_CLASS # number of blocks which has a score larger than 0.85
		g_one2many = [0.0] * NUM_CLASS # number of ground truth segmentation that matches to more than one detection segmentation
		g_many2one = [0.0] * NUM_CLASS # number of ground truth segmentation that more than one matches to the same one detections
		d_one2many = [0.0] * NUM_CLASS # number of detection segmentation that matches to more than one ground truth segmentation
		d_many2one = [0.0] * NUM_CLASS # number of detection segmentation that more than one matches to the same one segmentation
		det = [0.0] * NUM_CLASS # detection rate (recall)
		rec = [0.0] * NUM_CLASS # recognition accuracy (precision)

		score = [None] * len(self.gt_blocks)
		for i in range(len(score)):
			score[i] = [0.0] * len(seg_blocks)

		# compute number of segments for each class in ground truth
		for i in range(len(self.gt_blocks)):
			if self.gt_blocks[i].label == 'text':
				N[0] += 1
			elif self.gt_blocks[i].label == 'title':
				N[1] += 1
			else:
				N[2] += 1

		# compute number of segments for each class in guess
		for i in range(len(seg_blocks)):
			if seg_blocks[i].label == 'text':
				M[0] += 1
			elif seg_blocks[i].label == 'title':
				M[1] += 1
			else:
				M[2] += 1

		# computing score table
		for j in range(len(self.gt_blocks)):
			for k in range(len(seg_blocks)):
				score[j][k] = self.MatchScore(self.gt_blocks[j], seg_blocks[k], use_black_pixel)

		for c in range(NUM_CLASS):
			# computing one2one
			for j in range(len(self.gt_blocks)):
				for k in range(len(seg_blocks)):
					if self.gt_blocks[j].label != LABELS[c] or seg_blocks[k].label != LABELS[c]:
						continue
					if score[j][k] >=  ONETOONE_THRESHOLD:
						one2one[c] += 1

			# computing g_one2many and d_many2one
			for j in range(len(self.gt_blocks)):
				m_count = 0
				for k in range(len(seg_blocks)):
					if self.gt_blocks[j].label != LABELS[c] or seg_blocks[k].label != LABELS[c]:
						continue
					if score[j][k] >= ONETOMANY_THRESHOLD and score[j][k] < ONETOONE_THRESHOLD:
						m_count += 1

				if m_count >= 1:
					g_one2many[c] += 1
					d_many2one[c] += m_count

			# computing d_one2many and g_many2one
			for j in range(len(seg_blocks)):
				m_count = 0
				for k in range(len(self.gt_blocks)):
					if seg_blocks[j].label != LABELS[c] or self.gt_blocks[k].label != LABELS[c]:
						continue
					if score[k][j] >= ONETOMANY_THRESHOLD and score[k][j] < ONETOONE_THRESHOLD:
						m_count += 1

				if m_count >= 1:
					d_one2many[c] += 1
					g_many2one[c] += m_count

			# computing det(recall) and rec(precision)
			if N[c] == 0:
				det[c] = 0
			else:
				det[c] = one2one[c] / N[c] + g_one2many[c] / (4 * N[c]) + g_many2one[c] / (4 * N[c])

			if M[c] == 0:
				rec[c] = 0
			else:
				rec[c] = one2one[c] / M[c] + d_one2many[c] / (4 * M[c]) + d_many2one[c] / (4 * M[c])
		
		# compute final score
		num_class = 0
		for c in range(NUM_CLASS):
			if N[c] > 0:
				num_class += 1
		DET = 0 # recall
		REC = 0 # precision
		for i in range(num_class):
			DET += det[i] * N[i] / sum(N)
			REC += rec[i] * M[i] / sum(M)
		NSM = 0
		if num_class * (sum(det) + sum(rec)) != 0:
			NSM = 2 * (sum(det) * sum(rec)) / (num_class * (sum(det) + sum(rec)));
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
	eval = EvalOneToMany()
	eval.evaluate(None, './images/0006.jpg.demo_full.txt', False)
	eval.evaluate(None, './images/0006.jpg.demo_full.txt', False)
	eval.evaluate(None, './images/0005.jpg.demo_full.txt', False)
	eval.evaluate(None, './images/0005.jpg.guess.txt', False)
	eval.evaluate(None, './images/0005.jpg.guess2.txt', False)
	eval.plot_performance_curve()
	eval.generate_report()

if __name__ == '__main__':
	main()
