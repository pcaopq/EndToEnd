import sys, os

from Segmentation import Segmentation

class EvalOneToMany:
    def __init__(self, gt_path, seg_path, img_path=None, xml_path=None):
        assert False
        print('123')
        self.ground_truth = Segmentation(fname=gt_path)
        self.seg_to_eval = Segmentation(fname=seg_path)

def main():
    gt_path, seg_path, img_path, xml_path = sys.argv[1:5]
    print gt_path, seg_path, img_path, xml_path
    evaluator = EvalOneToMany(gt_path, seg_path, img_path, xml_path)

if __name__ == '__main__':
	main()
