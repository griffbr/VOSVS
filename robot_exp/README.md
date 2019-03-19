# Robot Experiments

## Overview
OSVOS_trainer is being provided to enable users to quickly annotate their own training data and train new OSVOS models for video object segmentation.
Original YCB annotation data used for our paper is included in ``./data/rawData/``.

Please cite our paper if you find it useful for your research.
```
@inproceedings{GrFlCoWACV19,
  author = {Griffin, Brent and Florence, Victoria and Corso, Jason J.},
  title = {Tukey-Inspired Video Object Segmentation},
  journal = {CoRR},
  year = {2019}
}
```

### Setup
Add trained OSVOS segmentation models to ``./data/models``.
obj config

Vs config





### Execution Process
Run ``./train_osvos_models.py`` [native Python, requires TensorFlow]
Model files generated in ``./data/models/`` can be deleted to save disk space or used in robot experiments.

Processing logged data.

## Included External Files

S. Caelles*, K.K. Maninis*, J. Pont-Tuset, L. Leal-Taixé, D. Cremers, and L. Van Gool
One-Shot Video Object Segmentation, Computer Vision and Pattern Recognition (CVPR), 2017.
	Video Object Segmentation
	https://github.com/scaelles/OSVOS-TensorFlow