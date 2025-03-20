from pa.misc.basic import get_comp,set_comp
from pa.space.cmy import rgb_to_cmy,cmy_to_rgb

def get_cmy_comp(im,i):
	im = rgb_to_cmy(im)
	return get_comp(im,i)

def set_cmy_comp(im,i,x):
	im = rgb_to_cmy(im)
	im = set_comp(im,i,x)
	return cmy_to_rgb(im)

def get_c(im):
	return get_cmy_comp(im,0)

def set_c(im,c):
	return set_cmy_comp(im,0,c)

def get_m(im):
	return get_cmy_comp(im,1)

def set_m(im,c):
	return set_cmy_comp(im,1,m)

def get_y(im):
	return get_cmy_comp(im,2)

def set_y(im,c):
	return set_cmy_comp(im,2,m)