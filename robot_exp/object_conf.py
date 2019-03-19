#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Brent Griffin (griffb@umich.edu)

Class for storing and using manipulation object information.
Class instances inherit properties of the initial object specified.
Class is defined such that object dictionary is extendable.
'''

import IPython

class manipulation_objects:
	def __init__(self):
		self.object_dict = {
			'dice':{
			'overlay_color': [1,1,1],
			'vision_model' : '/dc/dc.ckpt-10000',
			'name'		   : 'dice'},
			'marker':{
			'overlay_color': [0,0,0],
			'vision_model' : '/mr/mr.ckpt-10000',
			'name'		   : 'marker'},
			'baseball':{
			'overlay_color': [0,0,0],
			'vision_model' : '/bs/bs.ckpt-10000',
			'name'		   : 'baseball'},
			'foam brick':{
			'overlay_color': [65,72,131],
			'vision_model' : '/fm/fm.ckpt-10000',
			'name'		   : 'foam_brick'},
			'plate':{
			'overlay_color': [0,0,153],
			'vision_model' : '/pl/pl.ckpt-10000',
			'name'		   : 'plate'},
			'screwdriver':{
			'overlay_color': [132,0,0],
			'vision_model' : '/sc/sc.ckpt-10000',
			'name'		   : 'screwdriver'},
			'soft scrub':{
			'overlay_color': [190,237,255],
			'vision_model' : '/sf/sf.ckpt-10000',
			'name'		   : 'soft_scrub'},
			'spring clamp':{
			'overlay_color': [48,48,48],
			'vision_model' : '/spr/spr.ckpt-10000',
			'name'		   : 'spring_clamp'},
			'stacking cup':{
			'overlay_color': [0,252,255],
			'vision_model' : '/st/st.ckpt-10000',
			'name'		   : 'stacking_cup'},
			'wood':{
			'overlay_color': [132,180,220],
			'vision_model' : '/wd/wd.ckpt-10000',
			'name'		   : 'wood'},
			'washer':{
			'overlay_color': [235,228,219],
			'vision_model' : '/ws/ws.ckpt-10000',
			'name'		   : 'washer'},
			'knife':{
			'overlay_color': [41,32,206],
			'vision_model' : '/kn/kn.ckpt-10000',
			'name'		   : 'knife'},
			'spatula':{
			'overlay_color': [251,194,115],
			'vision_model' : 'spt/spt.ckpt-10000',
			'name'		   : 'spatula'},
			'hood':{
			'overlay_color': [102,102,102],
			'vision_model' : '/hood/hood.ckpt-10000',
			'name'		   : 'hood'},
			'tuna':{
			'overlay_color': [255,0,0],
			'vision_model' : '/tn/tn.ckpt-10000',
			'name'		   : 'tuna'},
			'spam':{
			'overlay_color': [255,0,0],
			'vision_model' : '/sp/sp.ckpt-10000',
			'name'		   : 'spam'},
			'sugar':{
			'overlay_color': [100,255,255],
			'vision_model' : '/sg/sg.ckpt-10000',
			'name'		   : 'sugar'},
			'pan handle':{
			'overlay_color': [40,90,144],
			'vision_model' : '/pn_hn/pn_hn.ckpt-10000',
			'name'		   : 'pan_handle'},
			'pan':{
			'overlay_color': [40,90,144],
			'vision_model' : '/pn/pn.ckpt-10000',
			'name'		   : 'pan'},
			'mug':{
			'overlay_color': [0,0,255],
			'vision_model' : '/mg/mg.ckpt-10000',
			'name'		   : 'mug'},
			'lock':{
			'overlay_color': [192,192,192],
			'vision_model' : '/lc/lc.ckpt-10000',
			'name'		   : 'lock'},
			'jello':{
			'overlay_color': [180,105,255],
			'vision_model' : '/gl/gl.ckpt-10000',
			'name'		   : 'jello'},
			'dice':{
			'overlay_color': [255,255,255],
			'vision_model' : '/dc/dc.ckpt-10000',
			'name'		   : 'dice'},
			'banana':{
			'overlay_color': [0,255,255],
			'vision_model' : '/bn/bn.ckpt-10000',
			'name'		   : 'banana'},
			'drill':{
			'overlay_color': [0,165,255],
			'vision_model' : '/dr/dr.ckpt-10000',
			'name'		   : 'drill'},
			'pringles can':{
			'overlay_color': [0,0,255],
			'vision_model' : '/pr/pr.ckpt-10000',
			'name'		   : 'pringles_can'},
			'plastic chain':{
			'overlay_color': [0,255,255],
			'vision_model' : '/ch/ch.ckpt-10000',
			'name'		   : 'plastic_chain'}
			}

	def set_object(self, obj_name):
		if obj_name in self.object_dict.keys():
			instance_dict = self.object_dict[obj_name]
			self.properties = instance_dict.keys()
			for _, key in enumerate(self.properties):
				setattr(self, key, instance_dict[key])
		else:
			print ('Error: object instance %s currently undefined.' % obj_name)
