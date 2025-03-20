from pa.misc.basic import get_comp,set_comp
from pa.space.hsv import rgb_to_hsv,hsv_to_rgb

def get_hsv_comp(im,i):
	im = rgb_to_hsv(im)
	return get_comp(im,i)

def set_hsv_comp(im,i,x):
	im = rgb_to_hsv(im)
	im = set_comp(im,i,x)
	return hsv_to_rgb(im)

def get_hsv_v(im):
	return get_hsv_comp(im,2)

def set_hsv_v(im,s):
	return set_hsv_comp(im,2,v)