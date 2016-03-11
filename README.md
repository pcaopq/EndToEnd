# mdp-newspaper-segmentation
This repository will house our code for prototyping and production. In our weekly meetings, we will discuss appropriate documentation techniques, subdivide programming tasks, and assign issues accordingly. 

MDP 2016 Proquest News

# End-to-End System
The End-to-End system is what we use to evaluate segmentation algorithms. On one end, the system uses a segmentation algorithm to produce a predicted segmentation of a newspaper image. The output of the segmentation algorithm is passed to the other end of the system, which evaluates the predicted segmentation against a ground-truth segmentation. 

## Required Software
General: python, a LaTeX generator (such as pdflatex)
Python packages: numpy, matplotlib, PIL

## Usage
### 1. Set up configuration file
The configuration file serves as the input to the end-to-end evaluation system. The configuration file details the following:

1. A list of segmentation algorithms to test. This is the “Metrics” field. This field should be a list of .py files. These files are the evaluation metrics.

2. A list of evaluation metrics with which to evaluate the segmentation algorithms.  This is the “Implementations” field. The “Implementations” field should be a list of .py files. These files are the segmentation algorithms. More than one segmentation algorithm can be used; each will be evaluated individually. Each segmentation algorithm produces a .json file. 

3. A path to the newspaper and ground-truth data, with which we will produce and evaluate segmentations. This is the “Data” field. The path should be to a directory (or a .jp2 if only evaluating one image). 

4. A path to the location of the predicted segmentations (i.e. output path). This is the “Outpath” field. This should be a path to a directory.

The configuration file must have the following format:

```
{
	“Metrics”: [“EvalOneToMany.py”],
	“Implementations”: [“textblocksBS.py”],
	“Data”: [“/path/to/data_and_groundtruth/”],
	“Outpath”: [“/path/to/output_location”]
}
```

### 2. Running the End-to-End system
hit play
