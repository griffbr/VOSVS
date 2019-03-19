import IPython; import cv2; import numpy as np
import tensorflow as tf
slim = tf.contrib.slim
import sys
from osvos_mod import osvos, osvos_arg_scope, interp_surgery, preprocess_img

class segmenter:
	def __init__(self, file_location):
		self.checkpoint_file = file_location
		config = tf.ConfigProto()
		config.gpu_options.allow_growth = True
		config.allow_soft_placement = True
		tf.logging.set_verbosity(tf.logging.INFO)
		batch_size = 1
		self.input_image = tf.placeholder(tf.float32, [batch_size, None, None, 3])
		with slim.arg_scope(osvos_arg_scope()):
			net, end_points = osvos(self.input_image)
		self.probabilities = tf.nn.sigmoid(net)
		global_step = tf.Variable(0, name='global_step', trainable=False)
		self.saver = tf.train.Saver([v for v in tf.global_variables() if '-up' not in v.name and '-cr' not in v.name])
		self.sess = tf.Session(config=config)
		self.sess.run(tf.global_variables_initializer())
		self.sess.run(interp_surgery(tf.global_variables()))
		self.saver.restore(self.sess, self.checkpoint_file)

	def change_model(self, file_location):
		self.checkpoint_file = file_location
		self.saver.restore(self.sess, self.checkpoint_file)

	def segment_image(self, img, write_file = False, file_name = 'mask.png'):	
		image = preprocess_img(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
		res = self.sess.run(self.probabilities, feed_dict={self.input_image: image})
		res_np = res.astype(np.float32)[0, :, :, 0] > 162.0/255.0
		mask_img = res_np.astype(np.uint8)*255
		if write_file:
			cv2.imwrite(file_name, mask_img)
		return mask_img 