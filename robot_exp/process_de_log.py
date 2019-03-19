'''                                                                             
Script for processing and analyzing depth experiment log data.                  
'''

import numpy as np
import IPython
import os
import glob
import time
import sys
sys.path.insert(0, './misc_fun/')

from data_log_utils import *
from depth_estimate import *

LOG_DIR = './log/depth/'
OUT_DIR = './log/depth_processed/'

file_list = sorted(glob.glob(os.path.join(LOG_DIR,'*')))
done_list = glob.glob(os.path.join(LOG_DIR,'*'))

for j, file_path in enumerate(file_list):
	file_name = file_path.split('/')[-1]
	name = file_name.split('.')[0]
	log_out_dir = '%s/%s/' % (OUT_DIR, name)
	plot_out_dir = log_out_dir
	if not os.path.isdir(plot_out_dir): os.makedirs(plot_out_dir)
	else: continue	

	# Open and read log file.
	log_file = LOG_DIR + file_name
	n_data = n_file_lines(log_file) - 1
	n_pxls = np.zeros(n_data)
	z_cam = np.zeros(n_data)
	for i in range(n_data):
		data_list = read_data_line(log_file, i+1)
		n_pxls[i] = float(data_list[0])
		z_cam[i] = float(data_list[1])
	# Save new output file.
	log_file = log_out_dir + file_name
	plot_file = plot_out_dir + name

	if False:
		# Calculate progressive z_obj estimate using MILAE.
		z_obj = np.zeros(n_data)
		err = np.zeros(n_data)
		const = np.zeros(n_data)
		tic = time.time()
		for i in range(n_data):
			print('Calculating processing data for %i points.' % i)
			z_obj[i], err[i], const[i] = depth_MILAE(n_pxls[:i+1],z_cam[:i+1])
		toc = time.time()
		print('Point-wise calculations took %5.4f for %i points.\n' % (toc-tic, i)) 
		z_cam2obj = z_cam + z_obj
		sqrt_n_pxls = n_pxls**0.5
		err_sqrt_pxl = err / sqrt_n_pxls

		data_list = [n_pxls, z_cam, z_obj, z_cam2obj, const, err, err_sqrt_pxl]
		data_list_names = ['n_pxls', 'z_cam', 'z_obj', 'z_cam2obj', 'const', 'err', 'err_sqrt_pxl']
		print_data_file(log_file, data_list, data_list_names)
		
		plot_2D_data([-z_cam, z_obj],['-z_cam','z_obj'],plot_file+ '_ncam_obj.png', tikz=True)
		plot_2D_data([-z_cam, err_sqrt_pxl],['-z_cam','err_sqrt_pxl'],plot_file+ '_ncam_err_sqrt_pxl.png', tikz=True)
		plot_2D_data([-z_cam, n_pxls],['-z_cam','n_pxls'],plot_file+ '_ncam_npxls.png', tikz=True)

	if True:
		# Repeat for least squares error.
		z_obj = np.zeros(n_data)
		err = np.zeros(n_data)
		const = np.zeros(n_data)
		tic = time.time()
		for i in range(1,n_data):
			print('Calculating processing data for %i points.' % i)
			z_obj[i], err[i], const[i], nrm_rsd_err = depth_LS(n_pxls[:i+1],z_cam[:i+1])
		toc = time.time()
		print('Point-wise calculations took %5.4f for %i points.\n' % (toc-tic, i)) 
		z_cam2obj = z_cam + z_obj
		sqrt_n_pxls = n_pxls**0.5
		err_sqrt_pxl = err / sqrt_n_pxls
		
		# Only relevant for older plots when z_obj was poorly defined.
		plot_2D_data([-z_cam, z_obj],['-z_cam','z_obj'],plot_file+ '_ncam_obj_LS.png', tikz=True)
		plot_2D_data([-z_cam, err_sqrt_pxl],['-z_cam','err_sqrt_pxl'],plot_file+ '_ncam_err_sqrt_pxl_LS.png', tikz=True)
		plot_2D_data([-z_cam, n_pxls],['-z_cam','n_pxls'],plot_file+ '_ncam_npxls.png', tikz=True)

		plot_vector_data([z_obj],['z_obj'],plot_file+ '_z_obj_LS.png', tikz=True)
		plot_vector_data([z_cam],['z_cam'],plot_file+ '_z_cam.png', tikz=True)
		plot_vector_data([n_pxls],['n_pxls'],plot_file+ '_n_pxls.png', tikz=True)