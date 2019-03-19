#!/usr/bin/python
# -*- coding: utf-8 -*-

# Functions for logging data to text files and plots.
# Questions?, griffb@umich.edu

import matplotlib.pyplot as plt
import IPython

from matplotlib2tikz import save as tikz_save
# import seaborn as sns

# Text logging functions.
def print_out_vector(file_name, vector):
	output_file = open(file_name, 'w')
	num_row = vector.shape
	for j in range(0,num_row[0]):
		output_file.write(str(vector[j]) + ' ')
		output_file.write('\n')
	output_file.close()

def print_data_file(file_name, data_list, data_names):
	print_data_line(file_name, data_names)
	n_data = len(data_list[0])
	n_type = len(data_list)
	for i in range(n_data):
		temp_list = []
		for j in range(n_type):
			temp_list.append(data_list[j][i])
		print_data_line(file_name, temp_list)

def print_data_line(file_name, data_list):
	output_file = open(file_name, 'a')
	for i, data_point in enumerate(data_list):
		output_file.write(str(data_point) + ' ')
	output_file.write('\n')
	output_file.close()

def read_data_line(file_name, line_n):
	with open(file_name) as input_file:
		for i, line in enumerate(input_file):
			if i == line_n:
				data_list = line.split(' ')
			elif i > line_n:
				break
	return data_list

def n_file_lines(file_name):
	with open(file_name) as f:
		for i, l in enumerate(f):
			pass
	return i + 1

# Visual data.
def plot_vector_data(vectors, labels, filename, ylim = [0,0], title='', tikz = False):
	for i, vec in enumerate(vectors):
		plt.plot(vec, label=labels[i])
	if not ylim == [0,0]:
		plt.ylim(ylim[0], ylim[1])
	if not title == '':
		plt.title(title)
	plt.legend()
	plt.grid()
	plt.savefig(filename, bbox_inches='tight')
	if tikz:
		tikz_save(filename.split('.png')[0] + '.tex')
	plt.clf()

def plot_2D_data(vectors, labels, filename, use_scatter = False, tikz = False):
	if use_scatter:
		plt.scatter(vectors[0], vectors[1])
	else:
		plt.plot(vectors[0], vectors[1])
	plt.xlabel(labels[0])
	plt.ylabel(labels[1])
	plt.legend()
	plt.grid()
	plt.savefig(filename, bbox_inches='tight')
	if tikz:
		tikz_save(filename.split('.png')[0] + '.tex')
	plt.clf()
