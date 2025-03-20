import cv2
from .misc.basic import get_num_comps

def rgb_to_rgba(im):
	assert get_num_comps(im) == 3
	return cv2.cvtColor(im,cv2.COLOR_RGB2RGBA)

def rgba_to_rgb(im):
	assert get_num_comps(im) == 4
	return cv2.cvtColor(im,cv2.COLOR_RGBA2RGB)

def rgba_to_bgra(im):
	assert get_num_comps(im) == 4
	return cv2.cvtColor(im,cv2.COLOR_RGBA2BGRA)

def bgra_to_rgba(im):
	assert get_num_comps(im) == 4
	return cv2.cvtColor(im,cv2.COLOR_BGRA2RGBA)