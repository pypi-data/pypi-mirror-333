import cv2
from .sig import *
from pa.misc.type import to_float

def sig_contrast(x,c):
	k = remap(c,-1,1,1,-1)
	return (sig(2*x-1,k)+1)/2

def min_max_contrast(x,m,M):
	x = remap(x,m,M,0,1)
	x = clamp(x)
	return x

def auto_min_max(img,eps):
	img_w = img.shape[1]
	img_h = img.shape[0]
	n = img_w*img_h
	img = to_uint(img)
	hist,_ = np.histogram(img,bins=256,range=(0,256))
	cv2.imshow('',img)
	cv2.waitKey()
	if np.any(hist > eps*n):
		m = np.argmax(hist > eps*n)
		M = 256-np.argmax(hist[::-1] > eps*n)
		if m < M:
			img = remap(img,m,M,0,255)
			return to_float(img)
	return None