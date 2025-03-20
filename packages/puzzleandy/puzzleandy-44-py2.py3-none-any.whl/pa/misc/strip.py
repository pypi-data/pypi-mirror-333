import cv2
import numpy as np
from pa.space.hsv import hsv_to_rgb

def gray_strip(width,height):
	im = np.linspace(0,1,width,dtype=np.float32)
	im = im.reshape(1,width)
	im = np.tile(im,(height,1))
	return im

def hue_strip(width,height):
	h = np.linspace(0,360,width,dtype=np.float32)
	s = v = np.full(width,1,np.float32)
	im = cv2.merge((h,s,v))
	im = hsv_to_rgb(im)
	im = im.reshape(1,width,3)
	im = np.tile(im,(height,1,1))
	return im