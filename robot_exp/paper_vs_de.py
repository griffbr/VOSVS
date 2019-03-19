#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Brent Griffin (griffb@umich.edu)
Script for testing VOS-VS and VOS-DE.
'''

import IPython
import time
import glob
import sys
sys.path.insert(0, './misc_fun/')

from scipy.optimize import minimize

from object_conf import *
from vs_conf import *
from segment import *
from vision_fn import *
from grab_fn import *
from robot_fn import *
from data_log_utils import *
from depth_estimate import *

# With ROS depend.
from data_subscriber import *
#from cyclops import *
import hsrb_interface

# Misc. parameters.
IV_MAX = 350
VS_PXL_MIN = 200
POSE_DIR = './data/pose/'
GRASP_DIR = './data/g_msk/'
BOUND_DIR = './data/b_msk/'
VIS_DIR = './data/models/'	
IMG_DIR = './img/'
DPTH_LOG_DIR = './log/depth/'
VS_LOG_DIR = './log/vs/'
LOG_IMG = True
DQ_UPDATE = 0.02
DEPTH_ERR_TOL = 0.001
DPTH_CHNG_TOL = 0.001
GRIP_OFFSET = 0.08
GRIP_MIN = -0.85
Z_ARM_MIN = 0.005
CAM2OBJ_MAX = 0.3
INIT_OBJ = 'sugar'
C_MAX = 100
Z_ARM_MAX = 0.68

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

def check_obj_boundary():
	jaccard = 1000; ct = 0; bound = 60
	bound_img_list = glob.glob(os.path.join(BOUND_DIR,'*'))
	n_img = len(bound_img_list)
	while jaccard > 1 and ct < n_img:
		bound_file = bound_img_list[ct]
		bound_img = np.atleast_3d(cv2.imread(bound_file))[...,0]
		jaccard = eval_intersect(bound_img, obj.mask)
		ct += 1
	if jaccard > 1:
		bound = int(bound_file.split('/')[-1].split('.')[0])
	return bound

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
def base_vs(cycles = 5, update=0, seg_reps = 10, pose = True, date=''):
	tts.say('Centering on %s.' % obj.name)
	if pose:
		load_pose(whole_body, POSE_DIR + vs.pose)
	vs.Je_pinv_prev = vs.Je_pinv
	vs.update = update
	s_all = np.zeros(shape=(cycles,2))
	e_all = np.zeros(shape=(cycles,2))
	for i in range(cycles):
		track_object(name='%s_%s_%ic_%ir' % (date, vs.name, i, 0))
		s = obj.mask_center
		for j in range(seg_reps-1):
			track_object()
			s += obj.mask_center
		s /= seg_reps
		s_all[i,:] = deepcopy(s)
		e_all[i,:] = s - vs.s_des
		if not np.isnan(s).any():
			dq_e, error_sum = vs.delta_q(s)
			try: 
				base.go_rel(dq_e[0], dq_e[1], 0)	
			except: 
				print("Can't move there!")
				print('\n\n Add code to go back to home position here!\n\n')
				dq_e *= 0
			if update>0 and sum(abs(dq_e))>DQ_UPDATE: 
				print('\nUpdating Je_pinv.\n')
				vs.broyden_update(s, dq_e, base=True) 
		else: 
			print('\nStep %i: Object not in view!\n' % i)
		track_object(name='%s_%s_f' % (date, vs.name))
		data_file='%s%s_%s_%s.txt'%(VS_LOG_DIR, str(time.time()).split('.')[0],vs.name,obj.name)
		print_data_file(data_file,[s_all[:,0],s_all[:,1],e_all[:,0],e_all[:,1]],['s0','s1','e0','e1'])

# Depth estimation.
def determine_depth(arm_limit, date=''):
	tts.say('Determining depth for %s.' % obj.name)
	track_object(name='%s_%s_d0' % (date, vs.name))
	depth_known = False
	move_up = False
	n_pxls = []; z_cam = [];
	z_obj_list = []
	# Run initial approach.
	init_seg_reps = 10; init_n = 10;
	second_n = 5;
	for i in range(3):
		n_pxls, z_cam, z_obj, cam2obj, err, const, nrm_rsd_err = add_depth_data(
			n_pxls, z_cam, arm_limit, dist = 0.1, n = init_n, seg_reps = init_seg_reps, date = date)
		z_obj_list.append(z_obj)
		track_object(name='%s_%s_ip_%i' % (date, vs.name, i))
	data_file = '%sinit_%ireps_%in_%s%s.txt' % (DPTH_LOG_DIR, init_seg_reps, init_n, str(time.time()).split('.')[0], obj.name)
	print_data_file(data_file, [n_pxls, z_cam], ['n_pxls', 'z_cam'])
	vs.set_config('base_gripper')
	vs.s_des = [240,320]
	vs.img_dir = './log/img/%s/%s/' % (date, obj.name)
	base_vs(3, pose=False)
	track_object(name='%s_%s_d1' % (date, vs.name))
	while not depth_known:
		#z_obj_change = z_obj_list[-2] - z_obj_list[-3]
		z_obj_change = z_obj_list[-3] - z_obj_list[-2]
		print('z_obj list is '); print(z_obj_list)
		print('z_obj change is %5.4f' % z_obj_change)
		#err_sqrt_pxl = err / n_pxls[-1]**0.5
		boundary = check_obj_boundary()
		#print('Err_sqrt_pxl: %5.5f' % err_sqrt_pxl)
		# Make decision for next action based on boundary, err, and distance to object.
		if boundary > 50 and abs(z_obj_change) < DPTH_CHNG_TOL and cam2obj < CAM2OBJ_MAX:
			depth_known = True
		else:
			tts.say('Collecting more data.')
			if boundary > 50 and cam2obj > CAM2OBJ_MAX or move_up:
				second_dist = np.random.uniform(0.05,0.15)
				move_up = False
			else: 
				base_vs(2, pose=False)
				move_up = True
				second_dist = -np.random.uniform(0.05, 0.3)
			n_pxls, z_cam, z_obj, cam2obj, err, const, nrm_rsd_err = add_depth_data(
				n_pxls, z_cam, arm_limit, dist = second_dist, n = second_n, seg_reps = init_seg_reps)
			z_obj_list.append(z_obj)
	data_file = '%s%s%s.txt' % (DPTH_LOG_DIR, str(time.time()).split('.')[0], obj.name)
	print_data_file(data_file, [n_pxls, z_cam], ['n_pxls', 'z_cam'])
	track_object(name='%s_%s_df' % (date, vs.name))
	return depth_known, z_obj, const 

def add_depth_data(n_pxls, z_cam, arm_limit, dist = 0.1, n = 5, seg_reps = 3, date=''):
	tic = time.time()
	n_pxls_tmp, z_cam_tmp = collect_approach_data(arm_limit, dist, n, seg_reps, date=date)		
	n_pxls = np.concatenate((n_pxls, n_pxls_tmp), axis=0)
	z_cam = np.concatenate((z_cam, z_cam_tmp), axis=0)
	#z_obj, depth_err, size_const = depth_MILAE(n_pxls, z_cam)
	z_obj, depth_err, size_const, nrm_rsd_err = depth_LS(n_pxls, z_cam)
	cam2obj = z_cam[-1] - z_obj
	print('%5.3f z_obj, %5.4f nrm_res_err, %5.3f error, %5.3f size_const, %5.3f z_camf, %5.3f cam2obj, %i points, %5.3f s' % 
		(z_obj, nrm_rsd_err, depth_err, size_const, z_cam[-1], cam2obj, len(n_pxls), time.time()-tic)) 
	return n_pxls, z_cam, z_obj, cam2obj, depth_err, size_const, nrm_rsd_err
def collect_approach_data(arm_limit, dist = 0.1, n = 5, seg_reps = 3, date=''):
	# Collect data as approaching object.
	z_cam_0 = joint_position(whole_body, ['arm_lift_joint'])[0]
	z_cam = np.linspace(z_cam_0, z_cam_0 - dist, n)
	n_pxls = np.zeros(n)
	fail_list = []
	tic = time.time()
	for i, pos in enumerate(z_cam):
		try:
			if pos < arm_limit:
				tts.say('Command is past arm limit!')
				fail_list.append(i)
			else:
				move_to_n_joint_positions(whole_body, ['arm_lift_joint'], [pos])
				track_object(name='_ap_%s_%s_%i' % (vs.name, date, i))
				s = obj.n_mask_pixels
				for j in range(seg_reps-1):
					track_object()
					s += obj.n_mask_pixels
				s /= seg_reps
				n_pxls[i] = deepcopy(s)
				# Optional intermediate depth calculations.
				if False:
					z_obj, depth_err, size_const, nrm_rsd_err = depth_LS(n_pxls[:i+1], z_cam[:i+1])
					print('%5.3f z_obj, %5.4f nrm_res_err, %5.3f error, %5.3f size_const, %5.3f z_cam, %i points, %5.3f s' % 
						(z_obj, nrm_rsd_err, depth_err, size_const, z_cam[i], i, time.time()-tic)) 
		except:
			print('Approach move failed!')
			fail_list.append(i)
	n_pxls = np.delete(n_pxls, fail_list)
	z_cam = np.delete(z_cam, fail_list)
	return n_pxls, z_cam

# Grasp object.
def grasp_object(z_obj, c_size, arm_limit, graspable, date=''):
	ct = 0
	tts.say('Grasping %s.' % obj.name)
	object_grasped = False
	z_arm = z_obj + GRIP_OFFSET
	if z_arm < arm_limit:
		print('\nz_arm is %5.4f and limit is %5.4f\n' % (z_arm, arm_limit))
		tts.say('Arm command is lower than limit.')
		graspable = False
		IPython.embed()
	z_arm = max(z_arm, Z_ARM_MIN)
	vs.set_config('base_gripper')
	vs.img_dir = './log/img/%s/%s/' % (date, obj.name)
	track_object(name='%s_%s_g0' % (date, vs.name))
	while not object_grasped and ct<3:
		gripper.command(1.0)
		move_to_n_joint_positions(whole_body, ['arm_lift_joint'], [z_arm])
		base_vs(3, pose=False, date=date)
		track_object(name='_g1_c_%i' % ct)
		if graspable:
			rotate_gripper()
			track_object(name='_g2_r_%i' % ct)
			object_grasped = try_grasp(ct, date)
			z_arm -= 0.01
		ct += 1
	track_object(name='_gf_g')

	if object_grasped:
		# Give object to user.
		tts.say('%s grasped!' % obj.name)
		tts.say('Here you go.')
		move_to_n_joint_positions(whole_body, ['arm_lift_joint'], [0.65])
		base.go_rel(0,0,-1.57)
		track_object(name='_gf_user')
		gripper.command(1.0)
		base.go_rel(0,0,1.57)
	else:
		tts.say('%s not graspable.' % obj.name)

def try_grasp(ct, date=''):
	grasped = False
	prev_pxls = deepcopy(obj.n_mask_pixels)
	try:
		init_grip = smart_grasp()
		if init_grip > GRIP_MIN:
			move_joint_amount(whole_body, 'arm_lift_joint', 0.015)
			gripper.apply_force(0.5)
			move_joint_amount(whole_body, 'arm_lift_joint', -0.01)
			gripper.apply_force(0.65)
			move_joint_amount(whole_body, 'arm_lift_joint', 0.2)
			time.sleep(1.0)
			if whole_body.joint_positions['hand_motor_joint'] > GRIP_MIN:
				track_object(name='_g3_chk_%i' % ct)
				if obj.n_mask_pixels > 0.5 * prev_pxls:
					tts.say('Visual grasp confirmed!')
					grasped = True
				else:
					tts.say('Visual grasp check failed!')
	except:	
		tts.say('Could not grasp %s object that time.' % obj.name)
	return grasped
def rotate_gripper():
	track_object()
	grasp_ang = np.radians(select_grasp_angle(obj.mask, GRASP_DIR))
	cur_ang = whole_body.joint_positions['wrist_roll_joint']
	cmd_wrist_angle = grasp_angle_to_pm90(cur_ang-grasp_ang, angle_mod=1.5708)
	whole_body.move_to_joint_positions({'wrist_roll_joint': cmd_wrist_angle})
def smart_grasp(grip_min=-0.7, force=0.5):
	gripper.apply_force(force)
	init_grip = whole_body.joint_positions['hand_motor_joint']
	grip_pos = np.max([init_grip, grip_min])
	gripper.command(grip_pos)
	return init_grip

def run_vs_exp(object_list, graspable):	
	ct_down = 10
	tts.say('Starting in')
	for i in range(ct_down):
		tts.say(str(ct_down-i))
		time.sleep(1.0)
	# Generate intial view of all objects.
	date = str(time.time()).split('.')[0]
	vs.set_config('base')
	load_pose(whole_body, POSE_DIR + vs.pose)
	vs.img_dir = './log/img/%s/init/' % date
	os.makedirs(vs.img_dir)	
	tts.say('Generating initial segmentation of all objects.')
	for i, depth_obj in enumerate(object_list):
		set_object(depth_obj)
		for j in range(5):
			track_object(name='init_%s_%s_%i' % (date, vs.name, j))
	# Grab actual objects.
	arm_limits = [0.25, 0.125, Z_ARM_MIN]
	arm_limits = [Z_ARM_MIN]
	for i, depth_obj in enumerate(object_list):
		set_object(depth_obj)
		vs.set_config('base')
		vs.img_dir = './log/img/%s/%s/' % (date, obj.name)
		if not os.path.isdir(vs.img_dir): os.makedirs(vs.img_dir)
		tts.say("Let's grab the %s!" % obj.name)
		base_vs(date=date, cycles=10)
		depth_known, z_obj, c_size = determine_depth(arm_limits[i], date=date)
		grasp_object(z_obj, c_size, arm_limits[i], graspable[i], date=date)

# Main challenge script.
def	main():
	# Misc. Initialization.
	print('\n\nRobot moves next, make sure that you are ready!\n\n')
	object_list = ['sugar', 'tuna', 'jello']
	graspable = [True, True, True]
	object_list = ['sugar']
	graspable = [True]

	IPython.embed()
	run_vs_exp(object_list, graspable)

	print('\nFinished!\n')
	IPython.embed()

if __name__ == '__main__':
	with hsrb_interface.Robot() as robot:
		base = robot.try_get('omni_base')
		whole_body = robot.get('whole_body')
		gripper = robot.get('gripper')
		tts = robot.try_get('default_tts')
		tts.language = tts.ENGLISH
		grasp_cam = image_subscriber('/hsrb/hand_camera/image_raw', True)
		#head_cam = image_subscriber('/hsrb/head_rgbd_sensor/rgb/image_rect_color', True)
		robot_state = state_subscriber('/hsrb/joint_states')
		seg = segmenter('./data/models/sg/sg.ckpt-10000')
		obj = manipulation_objects()
		vs = visual_servo()
		main()
