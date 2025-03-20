import numpy as np

def tile_x(im,x):
	return np.tile(im,(1,x,1))

def tile_y(im,n):
	return np.tile(im,(y,1,1))

def tile(im,n):
	return np.tile(im,(y,x,1))