# Quickly annotate multiple images per video using GrabCut. Update to previous Matlab-based annotation framework.
# Brent Griffin, 180430
# Questions? griffb@umich.edu
# 181127: Updated to work continuously if user wants to add more annotations.
# 190125: Updated to work for HSR seg-based work.
import numpy as np; import cv2; import IPython; import copy; import glob; import os
import sys; 
cwd = os.getcwd()
sys.path.insert(0, os.path.join(cwd, 'methods', 'preprocess'));
sys.path.insert(0, os.path.join(cwd, 'methods', 'annotate_suggest'));
from grabCutClass import * 
from videoProcessor import *
from annotation_suggester import *

# TODO:

user_scale = False
user_select = False

def get_user_annotation(videoDir):
	videoName = os.path.basename(videoDir)
	print ('\n\nGenerating user-guided annotation for ') + os.path.basename(videoDir) + ('.\n')
	annotationDir = os.path.join(videoDir, 'usrAnnotate')
	if not os.path.isdir(annotationDir):
		os.makedirs(annotationDir)
	imageDir = os.path.join(videoDir, 'src')
	imageFiles = glob.glob(os.path.join(imageDir,'*'))
	imageFiles.sort()
	userAnnotating = True
	while userAnnotating:
		antImageFiles = glob.glob(os.path.join(annotationDir,'*'))
		nAntImgs = len(antImageFiles)
		print ('Currently ') + str(nAntImgs) + (' annotation images:')
		for i in range(0,nAntImgs):
			print os.path.basename(antImageFiles[i])
		# Run automated annotation suggestion.
		suggester = annotation_suggester(videoDir)
		frame_idx_suggest, distance = suggester.suggest_frame()
		print ('Suggested annotation frame is ') + imageFiles[frame_idx_suggest]
		print ('Annotation frame distance is ') + str(distance) + ('.')
		# Ask if there are any other images they would like to annotate?
		response = raw_input('Annotate another image? (y or n)\n')
		if not response in {'y','Y','Yes','yes'}:
			userAnnotating = False
		if userAnnotating:
			# User annotation specific image.
			while True:
				if user_select:
					annotationImageIdx = input('What is preferred annotation image index? (' + str(os.path.basename(imageFiles[0])) + '-' + str(os.path.basename(imageFiles[-1])) + ' possible)\n')
					annotationImageIdx -= suggester.manip_start_idx
				else: annotationImageIdx = frame_idx_suggest
				try:
					imageDir = imageFiles[int(annotationImageIdx)]
					annotationImage = cv2.imread(imageDir)
					windowx = 100; windowy = 100
					if user_scale:
						cv2.imshow('Annotation Image', annotationImage)
						cv2.moveWindow('Annotation Image', windowx, windowy)
						cv2.waitKey(20)
						scale = input('What is preferred scale? (e.g., 1, 2, or 0.5)\n')
					else: scale = 2;
					annotationImageScaled = cv2.resize(annotationImage, (0,0), fx=scale, fy=scale)
					cv2.imshow('Scaled Annotation Image', annotationImageScaled)
					cv2.moveWindow('Scaled Annotation Image', windowx, windowy)
					cv2.waitKey(20)
					response = 'y'
					#response = raw_input('Is annotation frame acceptable? (y or n)\n')
					if response in {'y','Y','Yes','yes'}:
						cv2.destroyAllWindows()
						#cv2.waitKey()
						break
				except:
					print ('Image ') + str(annotationImageIdx) + (' does not exist!')
			outputMaskDir = os.path.join(annotationDir,os.path.basename(imageDir))
			# Let user annotate selected image.
			GrabCutter(imageDir, outputMaskDir, windowx, windowy, scale)
			save_extra_image_copy(imageDir, videoDir, nAntImgs)

def save_extra_image_copy(image_dir, video_dir, annotation_frame_num):
	# TODO: add visualization for mask on top of image.
	print ('Saving extra copy of annotation image for development.')
	extra_image_dir = os.path.join(video_dir, 'annotation_imgs')
	if not os.path.isdir(extra_image_dir):
		os.makedirs(extra_image_dir)
	cv2.imwrite(os.path.join(extra_image_dir, format(annotation_frame_num, '02d')
		+ '_annotation_' + os.path.basename(image_dir).split('.')[0] + '.jpg'),
		cv2.imread(image_dir))

def main():
	mainDir = os.getcwd()
	dataDir = os.path.join(mainDir, 'data')
	rawDataDir = os.path.join(dataDir, 'rawData')
	# Get list of video directories.
	videoList = sorted(next(os.walk(rawDataDir))[1])
	# Cycle through each video.
	for i, videoName in enumerate(videoList):
		# Misc. setup.
		videoDir = os.path.join(rawDataDir, videoName)
		# Check for src folder. If it doesn't exist, make it from video.
		VideoProcessor(videoDir)
		# Check for annotation files, if not there, ask users which frames they would like annotated.
		get_user_annotation(videoDir)
		print ('Finished with ') + videoName + (' annotation.\n\n')
	print ('\n\nFinished with all annotations!\n\n')

if __name__ == "__main__":
	main()	
