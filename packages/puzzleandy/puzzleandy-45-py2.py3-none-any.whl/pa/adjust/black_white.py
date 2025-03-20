from copy import deepcopy
import numpy as np
from pa.misc.lerp import unlerp
from pa.misc.math import clamp

def black(im,b):
	match type(im):
		case np.ndarray:
			arr = im-b
			return clamp(arr)
		case Im:
			im = deepcopy(im)
			im.arr = im.arr-b
			im.arr = clamp(im.arr)
			return im

def white(im,w):
	match type(im):
		case np.ndarray:
			arr = im/w
			return clamp(arr)
		case Im:
			im = deepcopy(im)
			im.arr = im.arr/w
			im.arr = clamp(im.arr)
			return im

def black_white(im,b,w):
	match type(im):
		case np.ndarray:
			arr = unlerp(im,b,w)
			return clamp(arr)
		case Im:
			im = deepcopy(im)
			im.arr = unlerp(im.arr,b,w)
			im.arr = clamp(im.arr)
			return im