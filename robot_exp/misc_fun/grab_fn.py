#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import glob
import os
import cv2

# Grab object.
def grab_object():
	initial_object_location()
	if obj.init_center[1] < IV_MAX: reach = 'near'
	else: reach = 'far'
	center_on_object('high'+reach)
	center_on_object('low'+reach)
	grasp_object(reach)

def grasp_object(reach):
	tts.say('Grasping %s, let me know how this goes!' % obj.name)
	object_grasped = False
	while not object_grasped:
		center_on_object('low'+reach)
		rotate_grip(reach)
		object_grasped = try_grasp()
		if not voice.switch == 'switch none':
			switch_object()
	voice.grasp_config = 'config rotation'

def try_grasp():
	grasped = False; answered = False
	try:
		init_grip = smart_grip()
		if init_grip > GRIP_MIN or obj.thin_grip:
			move_joint_amount(whole_body, 'arm_lift_joint', 0.2)
			gripper.apply_force(0.5)
			while not answered:
				answer = voice.task_feedback.split(' ', 1)[1]
				if answer == 'none':
					time.sleep(0.250)
				else:
					answered = True
					if answer == 'success':
						grasped = True
						#tts.say('Object grasped!')
					voice.task_feedback = 'task none'
		else:
			gripper.command(1.0)
	except:
		tts.say('I could not grasp the %s that time.' % obj.name)
	return grasped

def smart_grip(grip_min = -0.70, force = 0.5):
	gripper.apply_force(force)
	init_grip = whole_body.joint_positions['hand_motor_joint']
	grip_pos = np.max([init_grip, grip_min])
	gripper.command(grip_pos)
	return init_grip

def rotate_grip(reach):
	config = voice.grasp_config.split(' ', 1)[1]
	if reach == 'far' or config == 'horizontal':
		grasp_angle = 0.0
	elif config == 'vertical':
		grasp_angle = 1.5708
	else:
		grasp_angle = wrist_grip_angle()
	whole_body.move_to_joint_positions({'wrist_roll_joint': grasp_angle})

def wrist_grip_angle():
	track_object()
	grasp_ang = np.radians(select_grasp_angle(obj.mask, GRASP_DIR))
	cur_ang = whole_body.joint_positions['wrist_roll_joint']
	cmd_wrist_angle = grasp_angle_to_pm90(cur_ang-grasp_ang, angle_mod=1.5708)
	return cmd_wrist_angle

def select_grasp_angle(object_mask, grasp_dir):
	object_mask = np.atleast_3d(object_mask)[...,0]
	grasp_img_list = glob.glob(os.path.join(grasp_dir, '*.png'))
	n_grasps = len(grasp_img_list)
	grasp_cost = np.zeros(n_grasps)
	for i, grasp_img in enumerate(grasp_img_list):
		grasp_candidate = np.atleast_3d(cv2.imread(grasp_img))[...,0]
		grasp_cost[i] = eval_intersect(grasp_candidate, object_mask)
	best_grasp_img = grasp_img_list[np.argmin(grasp_cost)]
	grasp_angle = float(best_grasp_img.split('/')[-1].split('.')[0])
	return grasp_angle

def eval_intersect(mask1, mask2):
	msk1 = mask1.astype(np.bool)
	msk2 = mask2.astype(np.bool)
	return np.sum((msk1 & msk2))

def grasp_angle_to_pm90(grasp_angle, angle_mod = 90):
	if grasp_angle < -angle_mod:
		grasp_angle %= angle_mod
	elif grasp_angle > angle_mod:
		grasp_angle = grasp_angle % angle_mod - angle_mod
	return grasp_angle
