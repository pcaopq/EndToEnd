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

4. A path to the location of the predicted segmentations (i.e. output path), and a path to evaluation output. This is the “Outpath” field. This should be a list of two paths: one for the segmentation output, a second for the evaluation output.

An example configuration file is displayed below. Let it be named "test.config". The configuration file must have the following format:

```
{
	“Metrics”: [“EvalOneToMany.py”],
	“Implementations”: [“textblocksBS.py”],
	“Data”: [“/path/to/data_and_groundtruth/”],
	“Outpath”: [“/path/to/segmentation_output”, "/path/to/evaluation_output"]
}
```

### 2. Running the End-to-End system
Navigate to the code/ directory and in the terminal do:
```
python end2end.py test.config
```
Output will be sent to the output path detailed in test.config.

### 3. Output
The configuration file's "Outpath" field lists two paths: one path to a location for the segmentation output, a second path to the evaluation output. 

1. Segmentation Output: The end-to-end system places the .json files produced by the segmentation algorithms in this path. The segmentation algorithms are those detailed in the configuration file's "Implementations" field.
2. Evaluation Output: The end-to-end system places a .pdf report of the evaluation into this path. This .pdf file is for human digestion, as it nicely summarizes the results of each segmentation algorithm. Additionally, a text file containing the results is placed into this path.
