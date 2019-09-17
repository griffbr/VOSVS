# VOSVS: Video Object Segmentation-based Visual Servo

Contact: Brent Griffin (griffb at umich dot edu)

## Paper
[Video Object Segmentation-based Visual Servo Control and Object Depth Estimation on a Mobile Robot](https://arxiv.org/abs/1903.08336 "arXiv Paper")<br />
[Brent Griffin](https://www.griffb.com), Victoria Florence, and [Jason J. Corso](http://web.eecs.umich.edu/~jjcorso/)<br />

Please cite our paper if you find it useful for your research.
```
@inproceedings{GrCoWACV20,
  author = {Griffin, Brent and Florence, Victoria and Corso, Jason J.},
  booktitle = {IEEE Winter Conference on Applications of Computer Vision (WACV)},
  title = {Video Object Segmentation-based Visual Servo Control and Object Depth Estimation on a Mobile Robot Platform},
  year = {2020}
}
```

## Code

Source code for our video object segmentation-based framework is located in the ``/robot_exp`` folder.

Source code for annotating data and training OSVOS for segmentation is located in the ``/OSVOS_train`` folder.

## Method

__Video Demonstration:__ https://youtu.be/hlog5FV9RLs

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/hlog5FV9RLs/0.jpg)](https://www.youtube.com/watch?v=hlog5FV9RLs)

__HSR Segmenting Objects at Various Heights.__ HSR's grasp camera faces downward (left) and only collects RGB data for objects in the scene (top right). However, using active perception and video object segmentation (bottom right), HSR can locate and grasp a variety of objects in real time.
![alt text](https://github.com/griffbr/VOSVS/blob/master/figure/annotation_example.png "VOS-based Visual Servo Control, Active Depth Estimation, and Mobile Robot Grasping")
<br />

__Depth Estimation of Sugar Box.__ Data are collected and processed in real time during the initial approach to the sugar box in the video demonstration.
![alt text](https://github.com/griffbr/VOSVS/blob/master/figure/depth_estimation.png "Depth Estimation of Sugar Box")
<br />

## Use

This code is available for non-commercial research purposes only.

## Misc.

__Robot Fine Motor Skills using VOSVS:__ https://youtu.be/4L6Q8sAjiCI
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/4L6Q8sAjiCI/0.jpg)](https://www.youtube.com/watch?v=4L6Q8sAjiCI)
