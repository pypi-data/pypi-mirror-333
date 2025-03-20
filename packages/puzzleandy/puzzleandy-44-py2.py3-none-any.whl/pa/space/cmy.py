import cv2
from pa.misc.basic import get_num_comps

def rgb_to_cmy(im):
	assert get_num_comps(im) == 3
	r,g,b = cv2.split(im)
	c = 0.5*(g+b)
	m = 0.5*(r+b)
	y = 0.5*(r+g)
	return cv2.merge((c,m,y))

def cmy_to_rgb(im):
	assert get_num_comps(im) == 3
	c,m,y = cv2.split(im)
	r = m+y-c
	g = c+y-m
	b = c+m-y
	return cv2.merge((r,g,b))