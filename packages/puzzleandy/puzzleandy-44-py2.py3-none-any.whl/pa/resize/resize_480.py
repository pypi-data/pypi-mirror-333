from .resize import *

def resize_min_480(im):
	return resize_min(im,720,480)

def resize_max_480(im):
	return resize_max(im,720,480)

def resize_fit_480(im):
	return resize_fit(im,720,480)

def resize_fill_480(im):
	return resize_fill(im,720,480)