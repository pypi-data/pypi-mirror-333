from .hsl import get_hsl_comp,set_hsl_comp

def get_hue(im):
	return get_hsl_comp(im,0)

def set_hue(im,h):
	return set_hsl_comp(im,0,h)

def get_sat(im):
	return get_hsl_comp(im,1)

def set_sat(im,h):
	return set_hsl_comp(im,1,s)