# VOSVS: Video Object Segmentation-based Visual Servo

Contact: Brent Griffin (griffb at umich dot edu)

TODO: update arxiv link, update citation for arxiv

## Paper
[Video Object Segmentation-based Visual Servo Control and Object Depth Estimation on a Mobile Robot Platform](https://arxiv.org/abs/1811.07958 "ArXiV Paper")<br />
[Brent Griffin](https://www.griffb.com), Victoria Florence, and [Jason J. Corso](http://web.eecs.umich.edu/~jjcorso/)<br />

Please cite our paper if you find it useful for your research.
```
@inproceedings{GrFlCoWACV19,
  author = {Griffin, Brent and Florence, Victoria and Corso, Jason J.},
  title = {Tukey-Inspired Video Object Segmentation},
  journal = {CoRR},
  year = {2019}
}
```

## Method

__VOS-based Visual Servo Control, Active Depth Estimation, and Mobile Robot Grasping.__ After identifying the sugar box, HSR uses our video object segmentation-based framework to first center the object on the optical axis of the grasp camera (columns 1-2). From there, HSR estimates the depth of the segmented object as the gripper approaches on the optical axis (columns 2-4). Finally, HSR uses VOS-based grasping and error detection to pick up the sugar box (columns 5-6).
![alt text](https://github.com/griffbr/VOSVS/blob/master/figure/complete_exp.png "VOS-based Visual Servo Control, Active Depth Estimation, and Mobile Robot Grasping")
<br />






# !! UPDATES IN PROGRESS 190319 !!


## Use

This code is available for non-commercial research purposes only.