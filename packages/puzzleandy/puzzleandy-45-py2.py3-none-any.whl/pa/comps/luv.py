from pa.misc.basic import get_comp,set_comp
from pa.space.luv import rgb_to_luv,luv_to_rgb

def get_luv_comp(im,i):
	im = rgb_to_luv(im)
	return get_comp(im,i)

def set_luv_comp(im,i,x):
	im = rgb_to_luv(im)
	im = set_comp(im,i,x)
	return luv_to_rgb(im)

def get_luv_l(im):
	return get_luv_comp(im,0)

def set_luv_l(im,l):
	return set_luv_comp(im,0,l)

def get_luv_u(im):
	return get_luv_comp(im,1)

def set_luv_u(im,u):
	return set_luv_comp(im,1,u)

def get_luv_v(im):
	return get_luv_comp(im,1)

def set_luv_v(im,v):
	return set_luv_comp(im,1,v)