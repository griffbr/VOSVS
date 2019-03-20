# Robot Experiments

## Overview
robot_exp contains the source code used for the experiments in our paper.
The necessary segmentation models are trained using ``../OSVOS_train/train_osvos_models.py``.
Code is setup for Toyota's Human Support Robot (HSR) using ROS messages, but should be reconfigurable for other robot platforms.

Please cite our paper if you find it useful for your research.
```
@inproceedings{GrFlCoWACV19,
  author = {Griffin, Brent and Florence, Victoria and Corso, Jason J.},
  title = {Tukey-Inspired Video Object Segmentation},
  journal = {CoRR},
  year = {2019}
}
```

__VOS-based Visual Servo Control, Active Depth Estimation, and Mobile Robot Grasping.__ After identifying the sugar box, HSR uses our video object segmentation-based framework to center the object with the optical axis of the grasp camera (columns 1-2). Next, HSR estimates the depth of the segmented object in real time as the gripper approaches on the optical axis (columns 2-4). Finally, HSR uses VOS-based grasping and error detection to pick up the sugar box (columns 5-6).
This framework only requires an RGB camera combined with robot actuation.
![alt text](https://github.com/griffbr/VOSVS/blob/master/figure/complete_exp.png "VOS-based Visual Servo Control, Active Depth Estimation, and Mobile Robot Grasping")
<br />

### Setup
Add trained OSVOS segmentation models to ``./data/models``.
New object models should be added to the existing dictionary in ``./object_conf.py``.

Add new visual servo configurations using ``./vs_conf.py``.
Learn parameters for new visual servo configurations using ``./learn_vs.py``.

### Execution Process
Run ``./paper_vs.py`` to replicate visual servo control experiments from the paper [native Python, requires TensorFlow].

Run ``./paper_vs_de.py`` to replicate combined visual servo and depth estimation experiments from the paper [native Python, requires TensorFlow].

Visual servo and depth estimation data is timestamped and logged automatically into the ``./log`` folder.
To process logged data and make plots, run ``./process_vs_log.py`` for visual servo data and ``./process_de_log.py`` for depth estimation data.
Processed data are saved in new folders in ``./log``.

## Included External Files

S. Caelles*, K.K. Maninis*, J. Pont-Tuset, L. Leal-Taixé, D. Cremers, and L. Van Gool
One-Shot Video Object Segmentation, Computer Vision and Pattern Recognition (CVPR), 2017.
	Video Object Segmentation
	https://github.com/scaelles/OSVOS-TensorFlow

## Use

This code is available for non-commercial research purposes only.