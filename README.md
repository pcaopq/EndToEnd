# mdp-newspaper-segmentation
This repository will house our code for prototyping and production. In our weekly meetings, we will discuss appropriate documentation techniques, subdivide programming tasks, and assign issues accordingly. 

MDP 2016 Proquest News

## Usage

Under end_to_end/, running
```
python end2end.py test.config
```
will run the current segmentation algorithm,
then evaluate the output through our evaluation pipeline,
producing ``report.pdf''

Requires: PIL, pdflatex
