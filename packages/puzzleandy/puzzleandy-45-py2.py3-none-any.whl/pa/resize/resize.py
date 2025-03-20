import cv2

def resize(im,w,h,interp=None):
	return cv2.resize(im,(w,h),None,0,0,interp)

def resize_fac(im,fac,interp=None):
	return cv2.resize(im,None,None,fac,fac,interp)

def resize_match(im1,im2,interp=None):
	return resize(im1,*im2.shape[1::-1],interp)

def resize_width(im,w,interp=None):
	fac = w/im.shape[1]
	return resize_fac(im,fac,interp)

def resize_height(im,h,interp=None):
	fac = h/im.shape[0]
	return resize_fac(im,fac,interp)

def resize_max_width(im,w,interp=None):
	fac = w/im.shape[1]
	if fac < 1:
		return resize_fac(im,fac,interp)
	else:
		return im

def resize_max_height(im,h,interp=None):
	fac = h/im.shape[0]
	if fac < 1:
		return resize_fac(im,fac,interp)
	else:
		return im

def resize_min_width(im,w,interp=None):
	fac = w/im.shape[1]
	if fac > 1:
		return resize_fac(im,fac,interp)
	else:
		return im

def resize_min_height(im,h,interp=None):
	fac = h/im.shape[0]
	if fac > 1:
		return resize_facs(im,fac,interp)
	else:
		return im

def resize_min(im,w,h,interp=None):
	fac_x = w/im.shape[1]
	fac_y = h/im.shape[0]
	fac = max(fx,fy)
	if fac > 1:
		return resize_fac(im,fac,interp)
	else:
		return im

def resize_max(im,w,h,interp=None):
	fac_x = w/im.shape[1]
	fac_y = h/im.shape[0]
	fac = min(fac_x,fac_y)
	if fac < 1:
		return resize_fac(im,fac,interp)
	else:
		return im

def resize_fit(im,w,h,interp=None):
	fac_x = w/im.shape[1]
	fac_y = h/im.shape[0]
	if fac_x != 1 and fac_y != 1:
		fac = min(fac_x,fac_y)
		return resize_fac(im,fac,interp)
	else:
		return im

def resize_fill(im,w,h,interp=None):
	fac_x = w/im.shape[1]
	fac_y = h/im.shape[0]
	if fac_x != 1 and fac_y != 1:
		fac = max(fac_x,fac_y)
		return resize_fac(im,fac,interp)
	else:
		return im