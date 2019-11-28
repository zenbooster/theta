#!/usr/bin/env python3
#coding: utf-8

import metric
from common import *
from zencad import *

rib_diameter = 24
screw_m24_len = 19+4+2*2
screw_m24 = metric.metric_screw(24, 3.0, screw_m24_len, True)

def get_rib(is_hole):
	if is_hole:
		d = hole_d[rib_diameter]
		res = cylinder(d/2, wheel_arch_width + 4*2 + 19.55*2, True).rotateX(deg(90))
	else:
		d = rib_diameter
		r = d/2

		step = 3
		dt = 3*2
		#d3 = d - 2*(17/24*metric.getH(3))
		H = metric.getH(step)
		d2 = d - 2*(3 / 8 * H)
		r2 = d2 / 2

		d1 = d - 2*(5/8*H)
		r1 = d1 / 2
		d3 = d - 2*(17/24*H)
		r3 = d3 / 2

		#print("d3 = {}".format(d3))

		flange = \
			(cylinder((d+10)/2, 4, True).rotateX(deg(90)) - \
			cylinder(r3, 4, True).rotateX(deg(90))).back((wheel_arch_width-4)/2)

		res = cylinder(r, wheel_arch_width, True).rotateX(deg(90))
		
		th = screw_m24.rotateX(deg(90))
		res += (th.forw(wheel_arch_width/2+screw_m24_len) + th.mirrorXZ().back(wheel_arch_width/2+screw_m24_len))
		len = wheel_arch_width + screw_m24_len*2

		res = (res -  \
			(cylinder(r, wheel_arch_width - 4*2, True).rotateX(deg(90)) - \
			cylinder(r3, wheel_arch_width - 4*2, True).rotateX(deg(90))) - \
			(cylinder(r, wheel_arch_width - 40, True).rotateX(deg(90)) - \
			cylinder(10, wheel_arch_width - 40, True).rotateX(deg(90)))) + \
			(flange + flange.mirrorXZ())

		hex = linear_extrude(ngon(r=r, n=6), (0, 0, 20), True).rotateX(deg(90))
		res += hex.back((wheel_arch_width-20)/2) + hex.forw((wheel_arch_width-20)/2)
		#res -= cylinder((d3-4)/2, len, True).rotateX(deg(90))
		res -= cylinder(16/2, len, True).rotateX(deg(90))

		res = res.chamfer(1, refs=[
			point(0, -len/2, 0),
			point(0, len/2, 0)
		])

	return res

if __name__ == "__main__":
	step = 3
	H = metric.getH(step)
	d = 24
	r = d/2
	d3 = d - 2*(17/24*H)
	ri = (d3-4)/2+1

	m = get_rib(False).rotateX(deg(90))
	h_base = 1
	h0 = 2
	dt = (25+ri)/2
	base = cylinder(25, h_base, True) + cylinder(ri+0.2, h0, True).up((h0+h_base)/2)
	base -= cylinder(25/4, h_base, True).left(dt)
	base -= cylinder(25/4, h_base, True).right(dt)
	base -= cylinder(25/4, h_base, True).forw(dt)
	base -= cylinder(25/4, h_base, True).back(dt)

	dt = 5
	ang = 22.5
	yaw = deg(ang-dt)
	#cut = (cylinder(r=ri+0.2, h=h0, yaw=yaw, center=True) - cylinder(r=ri+0.1, h=h0, yaw=yaw, center=True)).up((h0+h_base)/2+1)
	cut = (cylinder(r=ri+0.2, h=h0, yaw=yaw, center=True) - cylinder(r=ri, h=h0, yaw=yaw, center=True)).up((h0+h_base)/2+1)
	for i in range(int(360 / ang)):
		base -= cut
		cut = cut.rotateZ(deg(ang))

	base -= cylinder(r=ri, h=h0+h_base, center=True).up((h0+h_base)/2- h_base/2)
	base = base.down((wheel_arch_width + screw_m24_len*2) / 2+h0+h_base/2)
	m += base
	#to_stl(m, 'd:/rib.stl', 0.01)
	display(m)
	show()