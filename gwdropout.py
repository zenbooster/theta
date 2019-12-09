#!/usr/bin/env python3
#coding: utf-8

import metric
from common import *
from zencad import *
from math import sin, cos

nut_m5_len = dropout_depth
nut_m5 = metric.metric_nut(5, 0.8, nut_m5_len, False).rotateX(deg(90)).forw(nut_m5_len/2)

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

def get_gwdropout():
	betta = 2.5
	sole_thick = 24
	sole_thick_a = sole_thick * cos(deg(betta))
	sole_thick_dr_a = (sole_thick-4) * cos(deg(betta))
	sole = box(dropout_width, dropout_sole_size, sole_thick, center=True)
	sole = sole.translate(0, -dropout_sole_size/2, -sole_thick/2)
	sole = sole.rotateX(deg(-betta))
	sole = sole.translate(0, dropout_sole_size/2, sole_thick_dr_a/2)
	holes = get_dropout_holes(False).up(dropout_height/2-3.6)
	delta = 4-(4*sin(deg(betta)))
	res = box(dropout_width, dropout_depth, dropout_height-(sole_thick_dr_a+delta), center=True).up((sole_thick_dr_a+delta)/2)
	sole = fillet(proto=sole, r=sole_thick/2, refs=[(0, -10, 10)])
	sole = fillet(proto=sole, r=4, refs=[(0, 10, -10), (0, -10, -10)])
	res += sole.back((dropout_sole_size-dropout_depth)/2).down((dropout_height-sole_thick_dr_a)/2 - delta)
	res -= holes
	
	res -= cylinder(16.2/2, dropout_depth, True).rotateX(deg(90)).up((dropout_height)/2 - 24.5)
	hblock = 4.5
	hd = hblock+4.9#7.8
	res -= cylinder(36.2/2, dropout_depth-hd, True).rotateX(deg(90)).up((dropout_height)/2 - 24.5).back(hd/2)
	a = 8.4
	b = 9.0
	c = 11.8
	block = polygon(pnts=[(-a/2, -c/2), (-a/2, -c/2+b), (a/2, c/2), (a/2, -c/2)], wire=False).extrude(vec=dropout_width, center=True).rotateX(deg(90)).rotateZ(deg(-90)).forw((dropout_depth-a)/2 - hblock)
	s = 7.8
	res -= block.up((dropout_height)/2 - 24.5 + c/2+s/2)
	res -= block.mirrorXY().up((dropout_height)/2 - 24.5 - c/2-s/2)
	hdc = hblock+3
	cut = cylinder(36.2/2, dropout_depth-hdc, True).rotateX(deg(90))
	cut ^= box(36.2, dropout_depth-hdc, s, center = True)
	cut = cut.up((dropout_height)/2 - 24.5).back(hdc/2)
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
	
	res -= cylinder(4, dropout_width, True).rotateY(deg(90)).up(L).back(dropout_p_axle_pos - dropout_depth/2)
	
	#res += box(dropout_width, dropout_depth, dropout_height, center=True).forw(dropout_depth*2)
	#res += box(dropout_width, dropout_depth, dropout_height, center=True).rotateX(deg(90)).down((dropout_height+dropout_depth)/2)
	return res

if __name__ == "__main__":
	m = get_gwdropout()
	display(m, color=(1, 1, 1, 0.5))
	show()