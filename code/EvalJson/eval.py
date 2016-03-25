import sys, os

from Segmentation import Segmentation
import re

from readJSON import *

NUM_CLASS = 3 # the number of classes, including title, text and other
ONETOONE_THRESHOLD = 0.85 # a specific manually decided threshold to classify each segmentation
ONETOMANY_THRESHOLD  = 0.1 # a specific manually decided threshold to classify each segmentation
LABELS = ['article', 'title', 'graphics']

class EvalOneToMany:

	# record the accuracy data
	eval_history = []

	# initialize the model. load the image
	# ground_truth and seg_to_eval are both Segmentation class objects
	def __init__(self, gt_path, seg_path):

		self.seg_path = seg_path
		self.gt_path = gt_path

		self.ground_truth = seg_from_json(gt_path, True)
		self.seg_to_eval = seg_from_json(seg_path, True)

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

		# compute number of segments for each class in ground truth
		for i, p in enumerate(self.ground_truth.segs):
			if p.label == LABELS[0]:
				N[0] += 1
			elif p.label == LABELS[1]:
				N[1] += 1
			else:
				N[2] += 1

		# compute number of segments for each class in guess
		for i, p in enumerate(self.seg_to_eval.segs):
			if p.label == LABELS[0]:
				M[0] += 1
			elif p.label == LABELS[1]:
				M[1] += 1
			else:
				M[2] += 1

		# computing score table
		for j, g in enumerate(self.ground_truth.segs):
			for k, s in enumerate(self.seg_to_eval.segs):
				score[j][k] = s.jaccard_similarity(g) 

		for c in range(NUM_CLASS):
			# computing one2one
			for j, g in enumerate(self.ground_truth.segs):
				for k, s in enumerate(self.seg_to_eval.segs):
					if g.label != LABELS[c] or s.label != LABELS[c]:
						continue
					if score[j][k] >= ONETOONE_THRESHOLD:
						one2one[c] += 1

			# computing g_one2many and d_many2one
			for j, g in enumerate(self.ground_truth.segs):
				m_count = 0
				for k, s in enumerate(self.seg_to_eval.segs):
					if g.label != LABELS[c] or s.label != LABELS[c]:
						continue
					if score[j][k] >= ONETOMANY_THRESHOLD and score[j][k] < ONETOONE_THRESHOLD:
						m_count += 1

				if m_count >= 1:
					g_one2many[c] += 1
					d_many2one[c] += m_count

			# computing d_one2many and g_many2one
			for j, g in enumerate(self.seg_to_eval.segs):
				m_count = 0
				for k, s in enumerate(self.ground_truth.segs):
					if g.label != LABELS[c] or s.label != LABELS[c]:
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
		# print g_one2many, g_many2one
		# print score
		print REC, DET, NSM # final score, precision, recall

def main():
	gt_path, seg_path = sys.argv[1:3]

	evaluator = EvalOneToMany(gt_path, seg_path)
	evaluator.evaluate()

if __name__ == '__main__':
	main()
