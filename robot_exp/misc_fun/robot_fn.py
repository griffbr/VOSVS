#!/usr/bin/python
# -*- coding: utf-8 -*-

import cPickle as pickle
import numpy as np
import IPython

def load_pose(whole_body, pickle_file, filter_list = []):
	pose = pickle.load(open(pickle_file, 'rb'))
	for i, pose_name in enumerate(filter_list):
		del pose[pose_name]
	whole_body.move_to_joint_positions(pose)

def filter_pose(pose):
	del pose['base_roll_joint']
	del pose['hand_l_spring_proximal_joint']
	del pose['hand_r_spring_proximal_joint']
	del pose['base_l_drive_wheel_joint']
	del pose['base_r_drive_wheel_joint']
	return pose

def move_joint_amount(whole_body, joint, amount):
	pose = whole_body.joint_positions
	pose[joint] += amount
	pose = filter_pose(pose)
	whole_body.move_to_joint_positions(pose)

def move_n_joints(whole_body, joints, amounts):
	pose = whole_body.joint_positions
	for i, joint in enumerate(joints):
		pose[joint] += amounts[i]
	pose = filter_pose(pose)
	whole_body.move_to_joint_positions(pose)

def move_to_n_joint_positions(whole_body, joints, amounts):
	pose = whole_body.joint_positions
	for i, joint in enumerate(joints):
		pose[joint] = amounts[i]
	pose = filter_pose(pose)
	whole_body.move_to_joint_positions(pose)

def save_pose(whole_body, pickle_file):
	pose = whole_body.joint_positions
	pose = filter_pose(pose)
	pickle.dump(pose, open(pickle_file, 'wb'))

def joint_position(whole_body, joint_list):
	q_list = whole_body.joint_positions
	q = np.zeros(len(joint_list))
	for i, joint in enumerate(joint_list):
		q[i] = q_list[joint]
	return q	
