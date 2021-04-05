# Custom Image Annotation Tool and OSVOS Training

## Overview
OSVOS_train is being provided to enable users to quickly annotate their own training data and then train new OSVOS models for video object segmentation.
We include YCB annotation data used for our paper in ``./data/rawData``.

Please cite our paper if you find it useful for your research.
```
@inproceedings{GrFlCoWACV20,
  author = {Griffin, Brent and Florence, Victoria and Corso, Jason J.},
  booktitle = {IEEE Winter Conference on Applications of Computer Vision (WACV)},
  title = {Video Object Segmentation-based Visual Servo Control and Object Depth Estimation on a Mobile Robot},
  year = {2020}
}
```

### Demo
Just run ``./train_osvos_models.py`` with TensorFlow sourced.
This will train all of the OSVOS segmentation models used in the paper.
Results will be dated and added to the ``./results`` folder.

__YCB Objects Included as Annotated Training Examples.__
![alt text](https://github.com/griffbr/VOSVS/blob/master/figure/objects.jpg "YCB Objects Included as Training Examples")
<br />

### Setup
Add new data to ``./data/rawData/`` folder following the examples already provided.
Each folder in rawData will be used to train a separate segmentation model using the corresponding annotated training data.
Remove folders from rawData if you do not need to train a new model for them.

Each unique folder contains source images in the ``src`` folder and at _least_ one annotation mask in the ``usrAnnotate`` folder.
The mask should have the same name as its corresponding source image (e.g., 00054.png).

To generate new annotation data, simply run ``./annotate_images.py`` and follow instructions in terminal.

Currently, the segmentation network will train for 10,000 iterations.
To change this, edit line 38 (``iters=10000``) in  ``./train_osvos_models.py``.
Less iterations will run faster, but may not train as well.
More iterations will take longer, probably work better, but may also overfit to the training examples.

### Execution Process
Run ``./train_osvos_models.py`` [native Python, requires TensorFlow].<br />
Model files generated in ``./data/models`` can be deleted to save disk space or used in robot experiments.

## Included External Files

S. Caelles*, K.K. Maninis*, J. Pont-Tuset, L. Leal-Taixé, D. Cremers, and L. Van Gool
One-Shot Video Object Segmentation, Computer Vision and Pattern Recognition (CVPR), 2017.<br />
Video Object Segmentation. <br />
https://github.com/scaelles/OSVOS-TensorFlow

## Use

This code is available for non-commercial research purposes only.
