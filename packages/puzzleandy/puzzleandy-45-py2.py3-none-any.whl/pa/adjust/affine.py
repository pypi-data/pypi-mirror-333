from importlib.resources import files
import math
import moderngl
import numpy as np
from pa.io import contents

def sgn(x):
	if x < 0:
		return -1
	elif x == 0:
		return 0
	else:
		return 1

def rot_size(im,t):
	w,h = im.shape[1::-1]
	a = math.atan2(h,w)
	k = math.hypot(w,h)
	q = math.floor(2*t/math.pi)
	s = -2*sgn(q%2)+1
	w = int(math.ceil(k*abs(math.cos(t-s*a))))
	h = int(math.ceil(k*abs(math.sin(t+s*a))))
	return w,h

def rot(im,t):
	w = im.shape[1]
	h = im.shape[0]
	shaders_path = files().parent/'shaders'
	vert_path = shaders_path/'default.vert'
	frag_path = shaders_path/'rot.frag'
	ctx = moderngl.create_standalone_context()
	prog = ctx.program(
		contents(vert_path),contents(frag_path))
	prog['iChannel0'] = 0
	tex = ctx.texture((w,h),3,im.tobytes(),dtype='f4')
	samp = ctx.sampler(False,False,texture=tex)
	samp.use(0)
	rot_w,rot_h = rot_size(im,t)
	prog['iResolution'] = (rot_w,rot_h,1)
	prog['iChannelResolution'] = ((w,h,1))
	prog['t'] = t
	col = ctx.texture((rot_w,rot_h),4,dtype='f4')
	fbo = ctx.framebuffer([col])
	fbo.use()
	fbo.clear(0,0,0,0)
	verts = ((-1,-1),(1,-1),(1,1),(-1,1))
	verts = np.array(verts, np.float32)
	vbo = ctx.buffer(verts.tobytes())
	vao = ctx.simple_vertex_array(prog,vbo,'pos')
	vao.render(moderngl.TRIANGLE_FAN)
	im = np.frombuffer(
		fbo.read(components=4,dtype='f4'),dtype=np.float32)
	im = im.reshape((rot_h,rot_w,4))
	return im