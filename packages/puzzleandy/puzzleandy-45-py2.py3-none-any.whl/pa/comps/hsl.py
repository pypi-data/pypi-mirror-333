from pa.misc.basic import get_comp,set_comp
from pa.space.hsl import rgb_to_hsl,hsl_to_rgb

def get_hsl_comp(im,i):
	im = rgb_to_hsl(im)
	return get_comp(im,i)

def set_hsl_comp(im,i,x):
	im = rgb_to_hsl(im)
	im = set_comp(im,i,x)
	return hsl_to_rgb(im)

def get_hsl_l(im):
	return get_hsl_comp(im,2)

def set_hsl_l(im,s):
	return set_hsl_comp(im,2,l)