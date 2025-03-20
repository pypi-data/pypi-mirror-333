from pa.misc.basic import get_comp,set_comp
from pa.space.xyz import rgb_to_xyz,xyz_to_rgb

def get_xyz_comp(im,i):
	im = rgb_to_xyz(im)
	return get_comp(im,i)

def set_xyz_comp(im,i,xp):
	im = rgb_to_xyz(im)
	im = set_comp(im,i,xp)
	return xyz_to_rgb(im)

def get_xyz_x(im):
	return get_xyz_comp(im,0)

def set_xyz_x(im,x):
	return set_xyz_comp(im,0,x)

def get_xyz_y(im):
	return get_xyz_comp(im,1)

def set_xyz_y(im,y):
	return set_xyz_comp(im,1,y)

def get_xyz_z(im):
	return get_xyz_comp(im,2)

def set_xyz_z(im,z):
	return set_xyz_comp(im,2,z)