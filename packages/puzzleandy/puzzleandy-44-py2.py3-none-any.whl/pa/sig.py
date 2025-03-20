import numpy as np
from scipy.special import comb
from .misc.math import remap

def binom(n,k):
	if n >= 0:
		return comb(n,k)
	else:
		return (-1)**k*comb(k-n-1,k)

def smooth_step(x,e1,e2,N):
	x = remap(x,e1,e2,0,1)
	total = np.zeros(x.shape,x.dtype)
	for n in range(N+1):
		c = binom(-N-1,n)*binom(2*N+1,N-n)
		p = (N+n+1)
		total += c*x**p
	return total

def dino_sig(x,k):
	return (x-x*k)/(np.abs(x)*2*k-k+1)

def dino_step(x,e1,e2,k):
	x = remap(x,e1,e2,0,1)
	return 0.5*(dino_sig(2*x-1,k)+1)
