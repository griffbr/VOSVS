#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Brent Griffin (griffb@umich.edu)

Class for storing and using visual servoing configurations.
Class is defined such that object dictionary is extendable.
Broyden update enables automatic tuning of feature Jacobian matrix.
'''

import numpy as np
import IPython
from copy import deepcopy

# TODO: 

class visual_servo:
	def __init__(self):
		self.config_dict = {
			# Complete 190208
			'head_pan_head_tilt': {
			'joints'   : ['head_pan_joint', 'head_tilt_joint'],
			'pose'     : 'head_cam.pk',
			's_des'    : [240,320], # [horizontal, vertical]
			#'Je_pinv'  : np.array([[0, 0.001],[0.001, 0]]), # Initial
			'Je_pinv'  : np.array([[0, 0.00182544],[0.00172504, 0]]), # Broyden 190208
			'Hadamard' : np.array([[0, 1],[1, 0]]),
			'name'     : 'head_pan_head_tilt'},
			# Complete 190215
			'base_gripper': {
			'joints'   : ['base_fwd', 'base_lat'],
			'pose'     : 'x_lower.pk',
			's_des'    : [240,220], # [horizontal, vertical]
			#'Je_pinv'  : np.array([[0, 0.001],[0.001, 0]]), # Initial
			'Je_pinv'  : np.array([[0, -0.00040371],[0.00039624, 0]]), # Broyden 190208
			'Hadamard' : np.array([[0, 1],[1, 0]]),
			'name'     : 'base_gripper'},
			# Complete 190208
			'base': {
			'joints'   : ['base_fwd', 'base_lat'],
			'pose'     : 'x_top.pk',
			's_des'    : [240,320], # [horizontal, vertical]
			#'Je_pinv'  : np.array([[0, 0.001],[0.001, 0]]), # Initial
			'Je_pinv'  : np.array([[0, -0.00178988],[0.00173277, 0]]), # Broyden 190208
			'Hadamard' : np.array([[0, 1],[1, 0]]),
			'name'     : 'base'},
			# Complete 190208
			'arm_roll_arm_lift': {
			'joints'   : ['arm_roll_joint', 'arm_lift_joint'],
			'pose'     : 'arm_lift_arm_roll_vs.pk',
			's_des'    : [240,320], # [horizontal, vertical]
			#'Je_pinv'  : np.array([[0,-0.001],[0.0025,0]]), # Hand-tuned
			#'Je_pinv'  : np.array([[0.0021, 0],[0, -0.0024]]), # Early broyden
			'Je_pinv'  : np.array([[0.001, 0],[0, 0.001]]), # Initial
			'Je_pinv'  : np.array([[0.00321418, 0],[0, -0.00157098]]), # Broyden 190208
			'Hadamard' : np.array([[1, 0],[0, 1]]),
			'name'     : 'arm_roll_arm_lift'},
			# Complete 190208
			'arm_roll_arm_lift_wrist_flex': {
			'joints'   : ['arm_roll_joint', 'arm_lift_joint', 'wrist_flex_joint'],
			'pose'     : 'arm_lift_arm_roll_vs.pk',
			's_des'    : [240,320], # [horizontal, vertical]
			#'Je_pinv'  : np.array([[0.001, 0],[0, 0.001],[0,0.001]]), # Initial
			'Je_pinv'  : np.array([[0.00328185, 0],[0, -0.00035489],[0, -0.00391664]]), # Broyden 190208
			'Hadamard' : np.array([[1, 0],[0, 1],[0,1]]),
			'name'     : 'arm_roll_arm_lift_wrist_flex'},
			# Complete 190208
			'arm_roll_wrist_flex': {
			'joints'   : ['arm_roll_joint', 'wrist_flex_joint'],
			'pose'     : 'arm_lift_arm_roll_vs.pk',
			's_des'    : [240,320], # [horizontal, vertical]
			#'Je_pinv'  : np.array([[0.001, 0],[0, 0.001]]), # Initial
			'Je_pinv'  : np.array([[0.0044488, 0],[0, -0.00221097]]), # Broyden 190208
			'Hadamard' : np.array([[1, 0],[0, 1]]),
			'name'     : 'arm_roll_wrist_flex'}
			}
		# Feature Jacobian Broyden update parameters.
		self.update = 0
		self.e_prev = 0
		self.q_prev = 0
		self.gain = -1

	def set_config(self, name):
		if name in self.config_dict.keys():
			instance_dict = self.config_dict[name]
			self.properties = instance_dict.keys()
			for _, key in enumerate(self.properties):
				setattr(self, key, instance_dict[key])
		else:
			print ('Error: object instance %s currently undefined.' % name)

	def delta_q(self, s):
		#error_logic = abs(self.Je_pinv).sum(axis=0) > 0
		e = s - self.s_des
		delta_q = self.gain * np.matmul(self.Je_pinv, e)
		e_sum = np.sum(abs(e)) #*error_logic))
		return delta_q, e_sum
	
	def broyden_update(self, s, q, base=False):
		e = s - self.s_des
		n_act = len(q)
		de = (e - self.e_prev).reshape(2,1)
		if base:
			dq = q.reshape(n_act,1)
		else:
			dq = (q - self.q_prev).reshape(n_act,1)
		# See ADE derivation 190129 pg. 17.
		if self.update > 0:
			self.Je_pinv_prev = deepcopy(self.Je_pinv)
			Jinv_de = np.matmul(self.Je_pinv, de)
			dqT_Jinv = np.matmul(dq.T, self.Je_pinv)
			# See ADE derivation 190205 pg. 18.
			self.Je_pinv += self.update * self.Hadamard * \
				np.matmul(dq - Jinv_de, dqT_Jinv) / np.dot(dqT_Jinv,de)
		# See ADE derivation 190128 pg. 16.
		#self.Je_pinv += self.update * np.matmul(dq - np.matmul(self.Je_pinv, de), de.T) / np.dot(de.T,de)
		self.e_prev = e
		self.q_prev = q
		print('Je_pinv is:')
		print(self.Je_pinv)
