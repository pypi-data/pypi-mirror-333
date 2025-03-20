import numpy as np
from scipy.interpolate import *
from pa.misc.const import *

def make_gray_to_rgb_lut(xi,yi,x,interp):
	xi = np.array(xi,np.float32)
	yi = np.array(yi,np.float32)
	y = np.empty((len(x),3),np.float32)
	for i in range(3):
		match interp:
			case Interp.LIN:
				y[:,i] = np.interp(x,xi,yi[:,i])
			case Interp.PCHIP:
				f = PchipInterpolator(xi,yi[:,i],dydx=dydx)
				y[:,i] = f(x)
	return y