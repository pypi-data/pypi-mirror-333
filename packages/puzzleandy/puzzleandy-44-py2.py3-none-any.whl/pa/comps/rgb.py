from pa.misc.basic import get_comp,set_comp

def get_r(im):
	return get_comp(im,0)

def set_r(im,r):
	return set_comp(im,0,r)

def get_g(im):
	return get_comp(im,1)

def set_g(im,g):
	return set_comp(im,1,g)

def get_b(im):
	return get_comp(im,2)

def set_b(im,b):
	return set_comp(im,2,b)