from importlib.resources import files
import moderngl
import numpy as np
from pa.io import contents

def apply_gray_to_rgb_lut(im,lut):
	im_w = im.shape[1]
	im_h = im.shape[0]
	lut_w = lut.shape[0]
	shaders_path = files().parent/'shaders'
	vert_path = shaders_path/'default.vert'
	frag_path = shaders_path/'apply_gray_to_rgb_lut.frag'
	ctx = moderngl.create_standalone_context()
	prog = ctx.program(
		contents(vert_path),contents(frag_path))
	prog['iChannel0'] = 0
	tex = ctx.texture(
		(im_w,im_h),1,im.tobytes(),dtype='f4')
	tex.use(0)
	prog['iChannel1'] = 1
	tex = ctx.texture(
		(lut_w,1),3,lut.tobytes(),dtype='f4')
	samp = ctx.sampler(False,texture=tex)
	samp.use(1)
	uni = prog['iChannelResolution'] = (
		(im_w,im_h,1),
		(lut_w,1,1))
	col = ctx.texture((im_w,im_h),3,dtype='f4')
	fbo = ctx.framebuffer([col])
	fbo.use()
	fbo.clear(0,0,0,0)
	verts = ((-1,-1),(1,-1),(1,1),(-1,1))
	verts = np.array(verts, np.float32)
	vbo = ctx.buffer(verts.tobytes())
	vao = ctx.simple_vertex_array(prog,vbo,'pos')
	vao.render(moderngl.TRIANGLE_FAN)
	im = np.frombuffer(
		fbo.read(components=3,dtype='f4'),dtype=np.float32)
	im = im.reshape((im_h,im_w,3))
	return im