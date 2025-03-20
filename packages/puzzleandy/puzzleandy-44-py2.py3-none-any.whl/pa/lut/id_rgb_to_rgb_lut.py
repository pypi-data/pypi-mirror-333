from importlib.resources import files
from math import sqrt
import moderngl
import numpy as np
from pa.io import contents

def id_rgb_to_rgb_lut(n):
	shaders_path = files().parent/'shaders'
	vert_path = shaders_path/'default.vert'
	frag_path = shaders_path/'id_rgb_to_rgb_lut.frag'
	ctx = moderngl.create_standalone_context()
	prog = ctx.program(
		contents(vert_path),contents(frag_path))
	prog['n'] = n
	s = n*int(sqrt(n))
	col = ctx.texture((s,s),3,dtype='f4')
	fbo = ctx.framebuffer([col])
	fbo.use()
	fbo.clear(0,0,0,0)
	verts = ((-1,-1),(1,-1),(1,1),(-1,1))
	verts = np.array(verts, np.float32)
	vbo = ctx.buffer(verts.tobytes())
	vao = ctx.simple_vertex_array(prog,vbo,'pos')
	vao.render(moderngl.TRIANGLE_FAN)
	im = np.frombuffer(fbo.read(dtype='f4'),dtype=np.float32)
	im = im.reshape((s,s,3))
	return im