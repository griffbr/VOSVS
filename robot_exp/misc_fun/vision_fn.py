#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
from scipy import ndimage
from copy import deepcopy
from skimage.measure import label


# Note: some functions kept in main script to avoid classes as function input.

# Vision functions.
def largest_region_only(init_mask):
	labels = label(init_mask)
	bin_count = np.bincount(labels.flat)
	if len(bin_count)>1:
		mask_bin = np.argmax(bin_count[1:]) + 1
		n_mask_pixels = bin_count[mask_bin]
		single_mask = labels == mask_bin
	else: single_mask = init_mask; n_mask_pixels = 0
	return single_mask, n_mask_pixels

def find_mask_centroid(mask):
	centroid_idx = np.array(ndimage.measurements.center_of_mass(mask))
	return centroid_idx

def combine_masks(mask_list):
	n_masks = len(mask_list)
	mask_out = mask_list[0]
	for i in range(1,n_masks):
		mask_out = mask_out | mask_list[i]
	return mask_out > 0

def eval_intersect(mask1, mask2):
	msk1 = mask1.astype(np.bool)
	msk2 = mask2.astype(np.bool)
	return np.sum((msk1 & msk2))

def write_seg_image(img_in, mask, file_name, overlay=[0,0,255], transparency=0.6):
	img = deepcopy(img_in) 
	for i, hue in enumerate(overlay):                                           
		img[mask,i] = hue*transparency + img[mask,i] * (1 - transparency)
	cv2.imwrite(file_name, img)