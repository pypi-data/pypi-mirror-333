from pa.misc.basic import get_comp,set_comp
from pa.space.lab import rgb_to_lab,lab_to_rgb

def get_lab_comp(im,i):
	im = rgb_to_lab(im)
	return get_comp(im,i)

def set_lab_comp(im,i,x):
	im = rgb_to_lab(im)
	im = set_comp(im,i,x)
	return lab_to_rgb(im)

def get_lab_l(im):
	return get_lab_comp(im,0)

def set_lab_l(im,l):
	return set_lab_comp(im,0,l)

def get_lab_a(im):
	return get_lab_comp(im,1)

def set_lab_a(im,a):
	return set_lab_comp(im,1,a)

def get_lab_b(im):
	return get_lab_comp(im,1)

def set_lab_b(im,b):
	return set_lab_comp(im,1,b)