from importlib.resources import files
from math import cbrt
import moderngl
import numpy as np
from pa.io import contents

def apply_rgb_to_rgb_lut(im,lut,fac=1):
	im_w = im.shape[1]
	im_h = im.shape[0]
	lut_w = lut.shape[1]
	lut_h = lut.shape[0]
	shaders_path = files().parent/'shaders'
	vert_path = shaders_path/'default.vert'
	frag_path = shaders_path/'apply_rgb_to_rgb_lut.frag'
	ctx = moderngl.create_standalone_context()
	prog = ctx.program(
		contents(vert_path),contents(frag_path))
	prog['iChannel0'] = 0
	tex = ctx.texture(
		(im_w,im_h),3,im.tobytes(),dtype='f4')
	tex.use(0)
	prog['iChannel1'] = 1
	tex = ctx.texture(
		(lut_w,lut_h),3,lut.tobytes(),dtype='f4')
	tex.use(1)
	prog['iResolution'] = (im_w,im_h,1)
	prog['n'] = int(cbrt(lut_w**2))
	prog['fac'] = fac
	col = ctx.texture((im_w,im_h),3,dtype='f4')
	fbo = ctx.framebuffer([col])
	fbo.use()
	fbo.clear(0,0,0,0)
	verts = ((-1,-1),(1,-1),(1,1),(-1,1))
	verts = np.array(verts, np.float32)
	vbo = ctx.buffer(verts.tobytes())
	vao = ctx.simple_vertex_array(prog,vbo,'pos')
	vao.render(moderngl.TRIANGLE_FAN)
	im = np.frombuffer(fbo.read(dtype='f4'),dtype=np.float32)
	im = im.reshape((im_h,im_w,3))
	return im