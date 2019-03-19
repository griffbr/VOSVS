#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import IPython
from scipy.optimize import minimize

def depth_MILAE(n_pxls, z_cam):
	# Multiplicative inverse-inspired linear absolute error.
	n = len(n_pxls)
	sqrt_p = n_pxls**0.5
	A = np.zeros(shape=(n, 2))
	b = np.zeros(shape=(n, 1))
	A[:,0] = sqrt_p
	A[:,1] = 1
	b = z_cam*sqrt_p
	x0 = np.zeros(shape=(2,1))
	output = minimize(cost_function, x0, args=(A,b))
	x = output.x
	z_obj = x[0]; size_const = x[1]
	#print('Object depth (MILAE) is %5.3f from %i points.' % (z_obj, n))
	avg_abs_err = output.fun / n
	return z_obj, avg_abs_err, size_const

def fit(A,x):
	return A.dot(x)

def cost_function(x, A, b):
	return np.sum(np.abs(b - fit(A,x)))

def depth_LS(n_pxls, z_cam):
	# Multiplicative inverse-inspired least square error.
	n = len(n_pxls)
	sqrt_p = n_pxls**0.5
	A = np.zeros(shape=(n, 2))
	b = np.zeros(shape=(n, 1))
	A[:,0] = sqrt_p
	A[:,1] = 1
	b = z_cam*sqrt_p
	x = np.matmul(np.matmul(np.linalg.inv(np.matmul(A.T,A)),A.T),b)
	z_obj = x[0]; size_const = x[1]
	res_err = np.abs(b-A.dot(x))
	avg_abs_err = np.sum(res_err)/n
	nrm_res_err = np.sum(res_err / sqrt_p)/n
	#avg_abs_err = cost_function(x,A,b) / n
	return z_obj, avg_abs_err, size_const, nrm_res_err