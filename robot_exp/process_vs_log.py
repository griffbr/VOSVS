'''                                                                             
Script for processing and analyzing visual servoing experiment log data.                  
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

# TODO: Make log file automatically compare two directories and process files that have not already been processed.

LOG_DIR = './log/vs/'
OUT_DIR = './log/vs_processed/'

file_list = sorted(glob.glob(os.path.join(LOG_DIR,'*')))
for j, file_path in enumerate(file_list):
	print('Processing %s' % file_path)
	file_name = file_path.split('/')[-1]
	name = file_name.split('.')[0]
	log_out_dir = '%s/%s/' % (OUT_DIR, name)
	plot_out_dir = log_out_dir
	if not os.path.isdir(plot_out_dir): os.makedirs(plot_out_dir)
	else: continue

	# Open and read log file.
	log_file = LOG_DIR + file_name
	n_data = n_file_lines(log_file) - 1
	s_all = np.zeros(shape = (n_data, 2))
	e_all = np.zeros(shape = (n_data, 2))
	for i in range(n_data):
		data_list = read_data_line(log_file, i+1)
		s_all[i] = [float(data_list[0]), float(data_list[1])]
		e_all[i] = [float(data_list[2]), float(data_list[3])]

	# Save output plots.
	plot_file = plot_out_dir + name
	plot_2D_data([e_all[:,0], e_all[:,1]],['e_0','e_1'],plot_file+ '_error.png', tikz=True)
	# s1 is x, s0 is y but axis must be reversed for plot.
	plot_2D_data([s_all[:,1], -s_all[:,0]],['$s_1$','$-s_0$'],plot_file+ '_s.png', tikz=True)
