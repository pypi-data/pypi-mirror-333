#version 330

vec2 fragCoord = gl_FragCoord.xy;
uniform sampler2D iChannel0;
uniform sampler2D iChannel1;
uniform vec3 iChannelResolution[2];

out vec3 fragColor;

vec3 lerp(float x, vec3 f0, vec3 f1)
{
	vec3 fx = (1-x)*f0+x*f1;
	return fx;
}

vec3 lookup(int x)
{
	vec2 uv = vec2(x+0.5,0.5)/iChannelResolution[1].xy;
	return texture(iChannel1,uv).rgb;
}

void main()
{
	vec2 uv = fragCoord/iChannelResolution[0].xy;
	float g = texture(iChannel0,uv).r;
	int w = int(iChannelResolution[1].x);
	int x0 = int(min(floor(g*w),w-1));
	int x1 = int(min(ceil(g*w),w-1));
	vec3 c0 = lookup(x0);
	vec3 c1 = lookup(x1);
	fragColor = lerp(g,c0,c1);
}