#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Brent Griffin (griffb@umich.edu)
Script for learning VOS-VS parameters.
'''

import IPython
import time
import sys
sys.path.insert(0, './misc_fun/')


from object_conf import *
from vs_conf import *
from segment import *
from vision_fn import *
from grab_fn import *
from robot_fn import *
from data_log_utils import *

# With ROS depend.
from data_subscriber import *
import hsrb_interface

# Misc. parameters.
IV_MAX = 350
VS_PXL_MIN = 200
GRIP_MIN = -0.8
POSE_DIR = './data/pose/'
GRASP_DIR = './data/g_msk/'
VIS_DIR = './data/models/'	
IMG_DIR = './img/'
VS_LOG_DIR = './log/vs/'
LOG_IMG = True
DQ_UPDATE = 0.02
INIT_OBJ = 'sugar'

# Vision
def initial_object_location():
	seg.change_model(VIS_DIR + obj.vision_model)
	track_object()
	obj.init_center = deepcopy(obj.mask_center)
def track_object(cam='grasp'):
	if cam == 'grasp':
		img = deepcopy(grasp_cam._input_image)
	else:
		img = deepcopy(head_cam._input_image)
	mask_location(img)
	if LOG_IMG:
		write_seg_image(img, obj.mask, IMG_DIR + obj.name + '_track.png', obj.overlay_color)
		
def mask_location(img):
	mask = seg.segment_image(img)
	obj.mask, obj.n_mask_pixels = largest_region_only(mask)
	obj.mask_center = find_mask_centroid(obj.mask)

# Used in main.
def set_object(target_name=''):
	if target_name == '':	
		target_name = voice.grab_object.split(' ', 1)[1]
		voice.grab_object = 'grab none'
	obj.set_object(target_name)
	seg.change_model(VIS_DIR + obj.vision_model)
def switch_object():
	target_name = voice.switch.split(' ', 1)[1]
	obj.set_object(target_name)
	seg.change_model(VIS_DIR + obj.vision_model)
	voice.switch = 'switch none'
def return_home():
	go_to_map_home(base)
	load_pose(whole_body, POSE_DIR + 'initial_view.pk')

# VS
def reset_vs_pose():
	print('Reseting VS pose.')
	load_pose(whole_body, POSE_DIR + vs.pose)
	q_command = deepcopy(joint_position(whole_body, vs.joints))
	q_prev = deepcopy(q_command)
	vs.Je_pinv = deepcopy(vs.Je_pinv_prev)
	return q_command, q_prev

def base_vs(cycles = 10, update=0, seg_reps = 3):
	load_pose(whole_body, POSE_DIR + vs.pose)
	vs.Je_pinv_prev = vs.Je_pinv
	vs.update = update
	print('\nJe_pinv initial is:'); print(vs.Je_pinv)
	s_all = np.zeros(shape=(cycles,2))
	e_all = np.zeros(shape=(cycles,2))
	for i in range(cycles):
		track_object()
		s = obj.mask_center
		for j in range(seg_reps-1):
			track_object()
			s += obj.mask_center
		s /= seg_reps
		s_all[i,:] = deepcopy(s)
		e_all[i,:] = s - vs.s_des
		if not np.isnan(s).any():
			dq_e, error_sum = vs.delta_q(s)
			print('\ndq_e is:'); print(dq_e)
			try: 
				base.go_rel(dq_e[0], dq_e[1], 0)	
			except: 
				print("Can't move there!")
				print('\n\n Add code to go back to home position here!\n\n')
				dq_e *= 0
			if sum(abs(dq_e))>DQ_UPDATE: 
				print('\nUpdating Je_pinv.\n')
				vs.broyden_update(s, dq_e, base=True) 
			print('\nStep %i:' % i)
			print('s is [%5.4f, %5.4f]' % (s[0], s[1]))
			print('joints are:'); print(vs.joints)
		else: 
			print('\nStep %i: Object not in view!\n' % i)
	print('\nJe_pinv final is:'); print(vs.Je_pinv)
	tts.say('Done with VS cycles.')
	# Log data.
	data_file='%s%s_%s_%s.txt'%(VS_LOG_DIR, str(time.time()).split('.')[0],vs.name,obj.name)
	print_data_file(data_file,[s_all[:,0],s_all[:,1],e_all[:,0],e_all[:,1]],['s0','s1','e0','e1']) 

def joint_vs(cycles = 10, update=0.01, seg_reps = 10, cam='grasp'):
	vs.Je_pinv_prev = vs.Je_pinv
	vs.update = update
	q_command, q_prev = reset_vs_pose()
	print('\nJe_pinv initial is:')
	print(vs.Je_pinv)
	for i in range(cycles):
		print('\nStep %i:' % i)
		q = joint_position(whole_body, vs.joints)
		print('q is:'); print(q)
		dq = q - q_prev
		track_object(cam)
		s = obj.mask_center
		for j in range(seg_reps-1):
			track_object(cam)
			s += obj.mask_center
		s /= seg_reps
		print('s is [%5.4f, %5.4f]' % (s[0], s[1]))
		if not np.isnan(s).any():
			if sum(abs(dq))>DQ_UPDATE: 
				print('\nUpdating Je_pinv.\n')
				vs.broyden_update(s, q) 
				q_prev = deepcopy(q)
			dq_e, error_sum = vs.delta_q(s)
			q_command += dq_e
			try: 
				move_to_n_joint_positions(whole_body, vs.joints, q_command)
			except: 
				print("Can't move there!")
				q_command, q_prev = reset_vs_pose()
			print('q_prev is [%5.4f, %5.4f]' % (q_prev[0], q_prev[1]))
			print('dq is [%5.4f, %5.4f]' % (dq[0], dq[1]))
			print('dq_e is:'); print(dq_e)
			print('q_com:'); print(q_command)
			print('joints are:'); print(vs.joints)
		else: 
			print('\nStep %i: Object not in view!\n' % i)
			q_command, q_prev = reset_vs_pose()
	print('\nJe_pinv final is:'); print(vs.Je_pinv)
	tts.say('Done with VS cycles.')

# Main challenge script.
def	main():
	# Misc. Initialization.
	print('\n\nRobot moves next, make sure that you are ready!\n\n')
	set_object(INIT_OBJ)
	vs_config = 'arm_roll_arm_lift_wrist_flex'
	vs_config = 'base'
	vs_config = 'arm_roll_arm_lift'
	vs_config = 'base_gripper'
	vs_config = 'base'
	vs_config = 'head_pan_head_tilt'
	vs.set_config(vs_config)
	IPython.embed()
	joint_vs(10, 0.1, 10, 'head')
	# base_vs(10, 0.1, 10)
	# joint_vs(10, 0.1, 10)

if __name__ == '__main__':
	with hsrb_interface.Robot() as robot:
		base = robot.try_get('omni_base')
		whole_body = robot.get('whole_body')
		gripper = robot.get('gripper')
		tts = robot.try_get('default_tts')
		tts.language = tts.ENGLISH
		grasp_cam = image_subscriber('/hsrb/hand_camera/image_raw', True)
		head_cam = image_subscriber('/hsrb/head_rgbd_sensor/rgb/image_rect_color', True)
		robot_state = state_subscriber('/hsrb/joint_states')
		seg = segmenter('./data/models/sg/sg.ckpt-10000')
		obj = manipulation_objects()
		vs = visual_servo()
		main()
