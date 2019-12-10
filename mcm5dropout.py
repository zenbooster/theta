#!/usr/bin/env python3
#coding: utf-8

import metric
from common import *
from zencad import *
from math import sin, cos, asin, sqrt

nut_m5_len = dropout_depth
nut_m5 = metric.metric_nut(5, 0.8, nut_m5_len, False).rotateX(deg(90)).forw(nut_m5_len/2)

small_rounding_r = 4
sole_angle = 2.5
sole_thick = 24
top_padding_holes = 3.6
wheel_axle_big_d = 36.2
wheel_axle_small_d = 16.2
pedal_axis_d = 8

def get_dropout_holes(is_holes):
	if is_holes:
		d = hole_d[5]
		n = cylinder(d/2, 4, True).rotateX(deg(90))
	else:
		d = 5
		n = nut_m5
	
	res = n.left(15) + n.right(15)
	n = n.down(44)
	res += n.left(15) + n.right(15)
	n = n.down(26)
	res += n.left(15) + n.right(15)
	return res

def get_dropout():
	sole_thick_before_rounding_cathet_a = (sole_thick-small_rounding_r) * cos(deg(sole_angle))
	sole = box(dropout_width, dropout_sole_size, sole_thick, center=True)
	
	delta = small_rounding_r+0.1
	a = sole_thick - delta
	b = (dropout_sole_size - (dropout_p_axle_pos))/4
	c = sqrt(a*a + b*b)
	step_size = 0.2
	f = a*b/c+step_size
	beta = asin(b/c)
	delta = (c - sole_thick)/2 + delta
	cut = box(dropout_width, f, c, center=True).up(delta)
	cut = cut.translate(0, -f/2, c/2-delta)
	cut = cut.rotateX(-beta)
	cut = cut.translate(0, f/2, -c/2+delta)

	sole -= cut.back((dropout_sole_size+f)/2-step_size)
	sole = sole.translate(0, -dropout_sole_size/2, -sole_thick/2)
	sole = sole.rotateX(deg(-sole_angle))
	sole = sole.translate(0, dropout_sole_size/2, sole_thick_before_rounding_cathet_a/2)
	holes = get_dropout_holes(False).up(dropout_height/2-top_padding_holes)
	small_rounding_cathet_b = small_rounding_r*sin(deg(sole_angle))
	delta_after_rounding = small_rounding_r-small_rounding_cathet_b
	res = box(dropout_width, dropout_depth, dropout_height-(sole_thick_before_rounding_cathet_a+delta_after_rounding), center=True).up((sole_thick_before_rounding_cathet_a+delta_after_rounding)/2)
	sole = fillet(proto=sole, r=sole_thick/2, refs=[(0, -dropout_sole_size/2, sole_thick/2)])
	sole = fillet(proto=sole, r=small_rounding_r, refs=[(0, dropout_sole_size/2, -sole_thick/2), (0, -dropout_sole_size/2, -sole_thick/2)])
	res += sole.back((dropout_sole_size-dropout_depth)/2).down((dropout_height-sole_thick_before_rounding_cathet_a)/2 - delta_after_rounding)
	res -= holes
	
	res -= cylinder(wheel_axle_small_d/2, dropout_depth, True).rotateX(deg(90)).up((dropout_height)/2 - dropout_m_axle_pos)
	hblock = 4.5
	hd = hblock+4.9#7.8
	res -= cylinder(wheel_axle_big_d/2, dropout_depth-hd, True).rotateX(deg(90)).up((dropout_height)/2 - dropout_m_axle_pos).back(hd/2)
	a = 8.4
	b = 9.0
	c = 11.8
	block = polygon(pnts=[(-a/2, -c/2), (-a/2, -c/2+b), (a/2, c/2), (a/2, -c/2)], wire=False).extrude(vec=dropout_width, center=True).rotateX(deg(90)).rotateZ(deg(-90)).forw((dropout_depth-a)/2 - hblock)
	s = 7.8
	res -= block.up((dropout_height)/2 - dropout_m_axle_pos + c/2+s/2)
	res -= block.mirrorXY().up((dropout_height)/2 - dropout_m_axle_pos - c/2-s/2)
	hdc = hblock+3
	cut = cylinder(wheel_axle_big_d/2, dropout_depth-hdc, True).rotateX(deg(90))
	cut ^= box(wheel_axle_big_d, dropout_depth-hdc, s, center = True)
	cut = cut.up((dropout_height)/2 - dropout_m_axle_pos).back(hdc/2)
	res -= cut
	
	ph = 18
	L = (dropout_height)/2-52.5
	pw = 8
	cut = box(dropout_width, pw, ph, center=True)
	cut = fillet(proto = cut, r = pw/2.01, refs=[(0, 1, ph/2), (0, -1, ph/2), (0, 1, -ph/2), (0, -1, -ph/2)])
	res -= cut.up(L-ph/2).back(-dropout_depth/2-pw/2+a+hblock)
	
	L -= ph+8
	
	ph = 15
	cut = box(dropout_width, pw, ph, center=True)
	cut = fillet(proto = cut, r = pw/2.01, refs=[(0, 1, ph/2), (0, -1, ph/2), (0, 1, -ph/2), (0, -1, -ph/2)])
	res -= cut.up(L-ph/2).back(-dropout_depth/2-pw/2+a+hblock)
	
	L -= ph+4

	ph = 24
	cut = box(dropout_width, ph, pw, center=True)
	cut = fillet(proto = cut, r = pw/2.01, refs=[(0, ph/2, 1), (0, ph/2, -1), (0, -ph/2, 1), (0, -ph/2, -1)])
	res -= cut.up(L-pw/2).back(-dropout_depth/2-pw+a+hblock + ph/2)
	
	res -= cylinder(pedal_axis_d/2, dropout_width, True).rotateY(deg(90)).up(L).back(dropout_p_axle_pos - dropout_depth/2)
	
	#res += box(dropout_width, dropout_depth, dropout_height, center=True).forw(dropout_depth*2)
	#res += box(dropout_width, dropout_depth, dropout_height, center=True).rotateX(deg(90)).down((dropout_height+dropout_depth)/2)
	return res

if __name__ == "__main__":
	m = get_dropout()
	#to_stl(m, 'd:\mcm5dropout.stl', 0.01)
	display(m)#, color=(1, 1, 1, 0.5))
	show()