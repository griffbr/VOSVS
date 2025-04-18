# VOSVS: Video Object Segmentation-based Visual Servo

Contact: Brent Griffin (griffb at umich dot edu)

## Paper
[Video Object Segmentation-based Visual Servo Control and Object Depth Estimation on a Mobile Robot](https://openaccess.thecvf.com/content_WACV_2020/html/Griffin_Video_Object_Segmentation-based_Visual_Servo_Control_and_Object_Depth_Estimation_WACV_2020_paper.html "WACV Paper")<br />
[Brent Griffin](https://www.griffb.com), Victoria Florence, and [Jason J. Corso](http://web.eecs.umich.edu/~jjcorso/)<br />
IEEE Winter Conference on Applications of Computer Vision (WACV), 2020

Please cite our paper if you find it useful for your research.
```
@inproceedings{GrFlCoWACV20,
  author = {Griffin, Brent and Florence, Victoria and Corso, Jason J.},
  booktitle = {IEEE Winter Conference on Applications of Computer Vision (WACV)},
  title = {Video Object Segmentation-based Visual Servo Control and Object Depth Estimation on a Mobile Robot},
  year = {2020}
}
```

## Code

Source code for our video object segmentation-based framework is located in the ``/robot_exp`` folder.

Source code for annotating data and training OSVOS for segmentation is located in the ``/OSVOS_train`` folder.

## Benchmark

VOSVS Visual Servo Control and Depth Estimation Benchmark.

| Object Set | Support Height (m) | YCB Object | [ClickBot](https://openaccess.thecvf.com/content/WACV2023/html/Griffin_Mobile_Robot_Manipulation_Using_Pure_Object_Detection_WACV_2023_paper.html "Mobile Robot Manipulation using Pure Object Detection, WACV 2023") | [VOSVS](https://openaccess.thecvf.com/content_WACV_2020/html/Griffin_Video_Object_Segmentation-based_Visual_Servo_Control_and_Object_Depth_Estimation_WACV_2020_paper.html) |
| --------------- | --------------- | --------------- | --------------- | --------------- | 
| Tool | 0.25 | Power Drill | \\ | X |
| Tool | 0.125 | Marker | \\ | \\ |
| Tool | 0.0 | Padlock | X | \\ |
| Tool | 0.25 | Wood | X | \\ |
| Tool | 0.125 | Spring Clamp | \\ | \\ |
| Tool | 0.0 | Screwdriver | X | \\ |
| Food | 0.25 | Chips Can | X | X |
| Food | 0.125 | Potted Meat | X | X |
| Food | 0.0 | Plastic Banana | X | X |
| Food | 0.25 | Box of Sugar | X | X |
| Food | 0.125 | Tuna | X | \\ |
| Food | 0.0 | Gelatin | X | X |
| Kitchen | 0.25 | Mug | X | X |
| Kitchen | 0.125 | Softscrub | \\ | |
| Kitchen | 0.0 | Skillet with Lid | \\ | |
| Kitchen | 0.25 | Plate | X | X |
| Kitchen | 0.125 | Spatula | \\ | |
| Kitchen | 0.0 | Knife | X | \\ |
| Shape | 0.25 | Baseball | X | \\ |
| Shape | 0.125 | Plastic Chain | X | \\ |
| Shape | 0.0 | Washer | \\ | \\ |
| Shape | 0.25 | Stacking Cup | X | X |
| Shape | 0.125 | Dice | \\ | |
| Shape | 0.0 | Foam Brick | X | X |
|  |  |  |  | 
| | Success Rate | (%VS / %DE) | 100 / 67 | 83 / 42 |

The VOSVS Benchmark uses a single consecutive set of mobile robot trials using a single RGB camera. Visual Servo (VS) is a success ( \\ ) if the robot moves within reach of an object for depth estimation (DE), which, in turn, is a success if the robot’s gripper closes on an object without collision (X). Please see our paper for more details. YCB Dataset objects are available [here](https://www.ycbbenchmarks.com/). The bins we use for varying depth were originally purchased [here](https://www.amazon.com/IRIS-USA-Inc-Multi-Purpose-Plastic/dp/B07CQ9B8W3/ref=sr_1_7?ie=UTF8&qid=1547231250&sr=8-7&keywords=plastic+bins+for+toys).

Is your technique missing although the paper and results are public? Let us know and we'll add it.

## Method

__WACV 2020 Oral Presentation:__ https://youtu.be/_SaMQjLxpZ8

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/_SaMQjLxpZ8/0.jpg)](https://www.youtube.com/watch?v=_SaMQjLxpZ8)

__HSR Segmenting Objects at Various Heights.__ HSR's grasp camera faces downward (left) and only collects RGB data for objects in the scene (top right). However, using active perception and video object segmentation (bottom right), HSR can locate and grasp a variety of objects in real time.
![alt text](https://github.com/griffbr/VOSVS/blob/master/figure/annotation_example.png "VOS-based Visual Servo Control, Active Depth Estimation, and Mobile Robot Grasping")
<br />

__Depth Estimation of Sugar Box.__ Data are collected and processed in real time during the initial approach to the sugar box in the video demonstration.
![alt text](https://github.com/griffbr/VOSVS/blob/master/figure/depth_estimation.png "Depth Estimation of Sugar Box")
<br />

## Use

This code is available for non-commercial research purposes only.

## Misc.

__WACV 2020 presentation video:__ https://youtu.be/5OIk-0HJJmc
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/5OIk-0HJJmc/0.jpg)](https://youtu.be/5OIk-0HJJmc)

__Robot Fine Motor Skills using VOSVS:__ https://youtu.be/4L6Q8sAjiCI
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/4L6Q8sAjiCI/0.jpg)](https://www.youtube.com/watch?v=4L6Q8sAjiCI)
