import cv2
import numpy as np
from .lib import to_cv

def show(im):
	match type(im):
		case np.ndarray:
			arr = to_cv(im)
			cv2.imshow('',arr)
			cv2.waitKey()
		case Im:
			arr = to_cv(im.arr)
			cv2.imshow('',arr)
			cv2.waitKey()