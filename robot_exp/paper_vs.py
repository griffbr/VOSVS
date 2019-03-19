#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Brent Griffin (griffb@umich.edu)
Script running VOS-VS Experiments.
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
POSE_DIR = './data/pose/'
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
def track_object(cam='grasp', name=''):
	if cam == 'grasp':
		img = deepcopy(grasp_cam._input_image)
	else:
		img = deepcopy(head_cam._input_image)
	mask_location(img)
	if LOG_IMG:
		base_name = '%s%s_%s' % (vs.img_dir, obj.name, name)
		write_seg_image(img, obj.mask, base_name + '.png', obj.overlay_color)
		if not name=='':
			cv2.imwrite(base_name + 'img.png', img)	
			cv2.imwrite(base_name + 'mask.png', obj.mask*255)	
		
def mask_location(img):
	mask = seg.segment_image(img)
	obj.mask, obj.n_mask_pixels = largest_region_only(mask)
	obj.mask_center = find_mask_centroid(obj.mask)

def time_segmentation():
	img = deepcopy(grasp_cam._input_image)
	n_iter = 1000
	tic = time.time()
	for i in range(n_iter):
		mask = seg.segment_image(img)
	toc = time.time()
	print('\n%i iterations of segmenter take %5.4f s, approximately %5.4f Hz\n' 
		% (n_iter, toc-tic, n_iter/(toc-tic)))

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

def base_vs(cycles = 10, update=0, seg_reps = 3, date=''):
	load_pose(whole_body, POSE_DIR + vs.pose)
	vs.Je_pinv_prev = vs.Je_pinv
	vs.update = update
	print('\nJe_pinv initial is:'); print(vs.Je_pinv)
	if date=='':
		date = str(time.time()).split('.')[0]
	s_all = np.zeros(shape=(cycles,2))
	e_all = np.zeros(shape=(cycles,2))
	for i in range(cycles):
		track_object(name='%s_%s_%ic_%ir' % (date, vs.name, i, 0))
		s = obj.mask_center
		for j in range(seg_reps-1):
			#track_object(name='%s_%s_%ic_%ir' % (date, vs.name, i, j+1))
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
			if update>0 and sum(abs(dq_e))>DQ_UPDATE: 
				print('\nUpdating Je_pinv.\n')
				vs.broyden_update(s, dq_e, base=True) 
			print('\nStep %i:' % i)
			print('s is [%5.4f, %5.4f]' % (s[0], s[1]))
			print('joints are:'); print(vs.joints)
		else: 
			print('\nStep %i: Object not in view!\n' % i)
	#print('\nJe_pinv final is:'); print(vs.Je_pinv)
	tts.say('Done with VS cycles.')
	# Log data.
	data_file = '%s%s_%s_%s.txt' % ( VS_LOG_DIR, date, vs.name, obj.name)
	print_data_file(data_file,[s_all[:,0],s_all[:,1],e_all[:,0],e_all[:,1]],['s0','s1','e0','e1']) 

def joint_vs(cycles = 10, update=0, seg_reps = 10, cam='grasp', date=''):
	vs.Je_pinv_prev = vs.Je_pinv
	vs.update = update
	q_command, q_prev = reset_vs_pose()
	print('\nJe_pinv initial is:'); print(vs.Je_pinv)
	if date=='':
		date = str(time.time()).split('.')[0]
	s_all = np.zeros(shape=(cycles,2))
	e_all = np.zeros(shape=(cycles,2))
	for i in range(cycles):
		print('\nStep %i:' % i)
		q = joint_position(whole_body, vs.joints)
		print('q is:'); print(q)
		dq = q - q_prev
		track_object(cam, name='%s_%s_%ic_%ir' % (date, vs.name, i, 0))
		s = obj.mask_center
		for j in range(seg_reps-1):
			#track_object(cam, name='%s_%s_%ic_%ir' % (date, vs.name, i, j+1))
			track_object(cam)
			s += obj.mask_center
		s /= seg_reps
		s_all[i,:] = deepcopy(s)
		e_all[i,:] = s - vs.s_des
		print('s is [%5.4f, %5.4f]' % (s[0], s[1]))
		if not np.isnan(s).any():
			if update>0 and sum(abs(dq))>DQ_UPDATE: 
				print('\nUpdating Je_pinv.\n')
				vs.broyden_update(s, q) 
				q_prev = deepcopy(q)
			dq_e, error_sum = vs.delta_q(s)
			q_command += dq_e
			try: 
				#move_to_n_joint_positions(whole_body, vs.joints, q_command)
				move_n_joints(whole_body, vs.joints, dq_e)
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
	#print('\nJe_pinv final is:'); print(vs.Je_pinv)
	tts.say('Done with VS cycles.')
	data_file = '%s%s_%s_%s.txt' % ( VS_LOG_DIR, date, vs.name, obj.name)
	print_data_file(data_file,[s_all[:,0],s_all[:,1],e_all[:,0],e_all[:,1]],['s0','s1','e0','e1']) 


# Code for running paper experiments.
def run_vs_exp(vs_config, object_list, cam='grasp'):
	# Count down and init.
	ct_down = 3
	tts.say('Starting in')
	for i in range(ct_down):
		tts.say(str(ct_down-i))
		time.sleep(1.0)
	date = str(time.time()).split('.')[0]
	vs.set_config(vs_config)
	if 'head' in vs_config: cam='head'
	# generate initial view or all objects
	load_pose(whole_body, POSE_DIR + vs.pose)
	vs.img_dir = './log/img/%s/init/' % date
	if not os.path.isdir(vs.img_dir): os.makedirs(vs.img_dir)
	tts.say('Generating initial image for all objects.')
	for i, vs_obj in enumerate(object_list):
		set_object(vs_obj)
		for j in range(2):
			track_object(cam, name='init_%s_%s_%ic_%ir' % (date, vs.name, i, j))
	# Perform visual servo and collect data.
	n_reps = 10; n_cycles = 20
	for i, vs_obj in enumerate(object_list):
		set_object(vs_obj)
		vs.img_dir = './log/img/%s/%s/' % (date, obj.name)
		if not os.path.isdir(vs.img_dir): os.makedirs(vs.img_dir)
		tts.say("Let's find the %s!" % vs_obj)
		gen_vs(vs_config, n_cycles, n_reps, cam, date)
		vs.img_dir = './log/img/%s/' % date
		track_object(cam, name='final_%s_%s' % (date, vs.name))

def gen_vs(vs_config, n_cycles = 5, n_reps = 3, cam='grasp', date=''):
	if 'head' in vs_config:
		joint_vs(n_cycles, 0, n_reps, cam, date)
	elif 'base' in vs_config:
		tts.say('About to start base visual servo, center then restart')
		IPython.embed()
		base_vs(n_cycles, 0, n_reps, date)
	else:
		joint_vs(n_cycles, 0, n_reps, cam, date)

# Main challenge script.
def	main():
	# Misc. Initialization.
	print('\n\nRobot moves next, make sure that you are ready!\n\n')
	#load_pose(whole_body, POSE_DIR + 'x_top.pk')
	set_object(INIT_OBJ)

	vs_config = 'base'
	vs_config = 'head_pan_head_tilt'
	object_list = ['sugar']

	IPython.embed()
	run_vs_exp(vs_config, object_list, 'head')
	# run_vs_exp(vs_config, object_list)

	#shirt or floor chain demo.
	if 0:
		vs_config = 'head_pan_head_tilt'
		vs_config = 'base'
		vs.set_config(vs_config)
		date = str(time.time()).split('.')[0]
		vs.img_dir = './log/img/%s/init/' % date
		if not os.path.isdir(vs.img_dir): os.makedirs(vs.img_dir)
		set_object('hood')
		set_object('plastic chain')
		IPython.embed()
		ct_down = 10
		tts.say('Starting in')
		for i in range(ct_down):
			tts.say(str(ct_down-i))
			time.sleep(1.0)
		base_vs(100, 0, 3)
		#joint_vs(100, 0, 3, cam='head')

	# time_segmentation()
	
	print('\nFinished.\n')
	IPython.embed()

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
