import cv2
import numpy as np
from pa.space.hsv import hsv_to_rgb

def pick_hsv(h,width,height):
	i,j = np.indices((height,width),np.float32)
	h = np.full((height,width),h,np.float32)
	s = j/width
	v = 1-i/height
	im = cv2.merge((h,s,v))
	return hsv_to_rgb(im)