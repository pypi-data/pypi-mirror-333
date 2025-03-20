import math
import numpy as np
from pa.misc.lerp import lerp,unlerp
from pa.sig import smooth_step,dino_step

def get_t_y1_y2(x,xi,yi):
	j = np.searchsorted(xi,x,side='right')
	j = np.clip(j,1,len(xi)-1)
	i = j-1
	old = np.seterr(divide='ignore')
	t = np.where(i == j,0,unlerp(x,xi[i],xi[j]))
	np.seterr(**old)
	return t,yi[i],yi[j]

def lin_interp(x,xi,yi):
	return np.interp(x,xi,yi)

def lin_interp_angle(x,xi,yi):
	xi = np.concatenate(([xi[-1]-360],xi,[xi[0]+360]))
	yi = np.concatenate(([yi[-1]],yi,[yi[0]]))
	return lin_interp(x,xi,yi)

def pchip_interp(x,xi,yi):
	return pchip_interpolate(xi,yi,x)

def pchip_interp_angle(x,xi,yi):
	xi = np.concatenate(([xi[-1]-360],xi,[xi[0]+360]))
	yi = np.concatenate(([yi[-1]],yi,[yi[0]]))
	return pchip_interp(x,xi,yi)

def cos_interp(x,xi,yi):
	t,y1,y2 = get_t_y1_y2(x,xi,yi)
	u = (1-np.cos(t*math.pi))/2
	return lerp(u,y1,y2)

def cos_interp_angle(x,xi,yi):
	xi = np.concatenate(([xi[-1]-360],xi,[xi[0]+360]))
	yi = np.concatenate(([yi[-1]],yi,[yi[0]]))
	return cos_interp(x,xi,yi)

def smooth_step_interp(x,xi,yi,N):
	t,y1,y2 = get_t_y1_y2(x,xi,yi)
	old = np.seterr(divide='ignore',invalid='ignore')
	y = smooth_step(t,y1,y2,N)
	y = np.where(y1 == y2,y1,y)
	np.seterr(**old)
	return y

def smooth_step_interp_angle(x,xi,yi,N):
	xi = np.concatenate(([xi[-1]-360],xi,[xi[0]+360]))
	yi = np.concatenate(([yi[-1]],yi,[yi[0]]))
	return smooth_step_interp(x,xi,yi,N)

def dino_step_interp(x,xi,yi,k):
	t,y1,y2 = get_t_y1_y2(x,xi,yi)
	old = np.seterr(divide='ignore',invalid='ignore')
	y = dino_step(t,y1,y2,k)
	y = np.where(y1 == y2,y1,y)
	np.seterr(**old)
	return y

def dino_step_interp_angle(x,xi,yi,k):
	xi = np.concatenate(([xi[-1]-360],xi,[xi[0]+360]))
	yi = np.concatenate(([yi[-1]],yi,[yi[0]]))
	return dino_step_interp(x,xi,yi,k)