#version 330

vec2 fragCoord = gl_FragCoord.xy;
uniform sampler2D iChannel0;
uniform vec3 iResolution;
uniform vec3 iChannelResolution[1];
uniform float t;
out vec4 fragColor;

#define PI 3.14

// w0, w1, w2, and w3 are the four cubic B-spline basis functions
float w0(float a)
{
	return (1.0/6.0)*(a*(a*(-a + 3.0) - 3.0) + 1.0);
}

float w1(float a)
{
	return (1.0/6.0)*(a*a*(3.0*a - 6.0) + 4.0);
}

float w2(float a)
{
	return (1.0/6.0)*(a*(a*(-3.0*a + 3.0) + 3.0) + 1.0);
}

float w3(float a)
{
	return (1.0/6.0)*(a*a*a);
}

// g0 and g1 are the two amplitude functions
float g0(float a)
{
	return w0(a) + w1(a);
}

float g1(float a)
{
	return w2(a) + w3(a);
}

// h0 and h1 are the two offset functions
float h0(float a)
{
	return -1.0 + w1(a) / (w0(a) + w1(a));
}

float h1(float a)
{
	return 1.0 + w3(a) / (w2(a) + w3(a));
}

vec4 samp(float x, float y)
{
	vec2 q = vec2(x,y);
	vec2 p = (q+vec2(0.5))/iChannelResolution[0].xy;
	vec4 c = texture(iChannel0,p);
	if (!(0 <= p.x && p.x <= 1
	&& 0 <= p.y && p.y <= 1))
		c.a = 0;
	return c;
}

vec4 texture_bicubic(vec2 p)
{
	vec2 res = iChannelResolution[0].xy;
	vec2 q = p*res-0.5;
	vec2 i = floor(q);    
	vec2 f = fract(q);

	float g0x = g0(f.x);
	float g1x = g1(f.x);
	float g0y = g0(f.y);
	float g1y = g1(f.y);
	float h0x = h0(f.x);
	float h1x = h1(f.x);
	float h0y = h0(f.y);
	float h1y = h1(f.y);

	vec4 c0 = samp(i.x+h0x,i.y+h0y);
	vec4 c1 = samp(i.x+h1x,i.y+h0y);
	vec4 c2 = samp(i.x+h0x,i.y+h1y);
	vec4 c3 = samp(i.x+h1x,i.y+h1y);
	
	return
		g0y*(g0x*c0+g1x*c1)+
		g1y*(g0x*c2+g1x*c3);
}

vec2 rot(vec2 p, float t)
{
	float c = cos(t);
	float s = sin(t);
	mat2 m = mat2(c,-s,s,c);
	return m*p;
}

void main()
{
	vec2 p = fragCoord;
	p -= iResolution.xy/2;
	p = rot(p,-t);
	p /= iChannelResolution[0].xy;
	p += 0.5;
	vec4 c = texture_bicubic(p);	
	fragColor = c;
}