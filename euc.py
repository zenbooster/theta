#!/usr/bin/env python3
#coding: utf-8

import metric
#import rib
from common import *
from zencad import *


PG29=from_brep('./PE_PG29.brep')
nut_m5_len = dropout_depth
nut_m5 = metric.metric_nut(5, 0.8, nut_m5_len, False).rotateX(deg(90)).forw(nut_m5_len/2)

def get_side_compartment():
	'''
	w = side_compartment_width - 4
	h = side_compartment_height - 4
	d = side_compartment_depth - 4
	rear = rectangle(w - 5, h - 5, True, True);
	front = rectangle(w, h, True, True).up(d);

	res = loft([rear, front])
	res = thicksolid(proto=res, t=4, refs=[point(0, 0, side_compartment_depth+side_compartment_depth/10)])
	res = res.rotateX(deg(90))
	'''
	res = from_brep('./1550j.brep')
	res = res.rotateY(deg(180))
	res = res.rotateX(deg(90))
	res = res.back(side_compartment_depth-9)#.mirrorX()

	return res;

side_compartment = get_side_compartment().forw(side_compartment_depth / 2 - 4)

def get_dropout_holes(is_holes):
	if is_holes:
		d = hole_d[5]
		n = cylinder(d/2, 4, True).rotateX(deg(90))
	else:
		d = 5
		n = nut_m5
	
	res = n.left(15) + n.right(15)
	n = n.down(43)
	res += n.left(15) + n.right(15)
	n = n.down(26)
	res += n.left(15) + n.right(15)
	return res

def get_dropout():
	sole_thick = dropout_height - dropout_sole_pos
	sole = box(dropout_width, dropout_sole_size, sole_thick, center=True)
	return \
		box(dropout_width, dropout_depth, dropout_height, center=True)+\
		fillet(proto=sole, r=sole_thick/2, refs=[(0, -10, 10)])\
			.back((dropout_sole_size-dropout_depth)/2).down((dropout_height-sole_thick)/2)-\
		get_dropout_holes(False).up(dropout_height/2 - (dropout_sole_pos - 69) + 14)-\
		cylinder(4, dropout_width, True).rotateY(deg(90)).down((dropout_height-sole_thick)/2).back(dropout_p_axle_pos - dropout_depth/2)

def get_shell_mount():
	sole_thick = dropout_height - dropout_sole_pos
	d = hole_d[10]
	res = box(dropout_width+8+d*2*2, dropout_depth+4, 4, center=True)
	res -= cylinder(d/2, 4, True).left((dropout_width+8+d*4)/2-d)
	res -= cylinder(d/2, 4, True).right((dropout_width+8+d*4)/2-d)
	res = res.up((dropout_height-sole_thick)/2)
	res += \
		box(dropout_width+8, dropout_depth+4, dropout_height - sole_thick+4, center=True) - \
		box(dropout_width, dropout_depth, dropout_height - sole_thick, center=True).translate(0, 2, -2) - \
		get_dropout_holes(True).up(dropout_height/2 - (dropout_sole_pos - 69) + 14 - (sole_thick/2+4/2)).back(dropout_depth/2)
	res -= cylinder(37/2, 4, True).rotateX(deg(90)).back(dropout_depth/2).up((dropout_height-sole_thick+4)/2-dropout_m_axle_pos-4)
	return res

def get_sm_spacer():
	#res = box(dropout_width+8+5*4, dropout_depth+4, 8, center=True)
	#res -= cylinder(hole_d[5]/2, 8, True).left((dropout_width+8+5*4)/2-5)
	#res -= cylinder(hole_d[5]/2, 8, True).right((dropout_width+8+5*4)/2-5)
	d = hole_d[10]
	res = box(dropout_width+8+d*2*2, dropout_depth+4, 4, center=True)
	res -= cylinder(d/2, 4, True).left((dropout_width+8+d*4)/2-d)
	res -= cylinder(d/2, 4, True).right((dropout_width+8+d*4)/2-d)

	res -= side_compartment.up(side_compartment_height/2).back(side_compartment_depth/2-(dropout_depth+4)/2)
	res -= box(dropout_width+8+d*4, dropout_depth+4, 4, center=True).up(4)
	return res

def get_inner_spacer():
	d = hole_d[10]
	h = 4
	res = box(d*2, dropout_depth+4, h, center=True)
	res -= cylinder(d/2, h, True)
	cut_depth = (dropout_depth+4)/2
	cut = box(d*2, cut_depth, h, center=True).back(cut_depth/2) - cylinder(r=d, h=h, yaw=deg(180), center=True).rotateZ(deg(180))
	res -= cut

	res -= side_compartment.up(side_compartment_height/2-5.4).back(side_compartment_depth/2-(dropout_depth+4)/2).right((dropout_width+h+d*4)/2-d)
	return res

def get_cable_protection():
	res = box(cable_protection_width, 4, cable_protection_height, center=True)
	delta=1
	r = cable_protection_depth / 2
	res += fillet(proto=box(cable_protection_width, cable_protection_depth, cable_protection_height-5*2*2, center=True), r=r, refs=[(0, -30, -1), (0, -30, 1)]).back(r-2)
	res -= fillet(proto=box(cable_protection_width, cable_protection_depth-4, cable_protection_height-5*2*2-8, center=True), r=r-2, refs=[(0, -30, -1), (0, -30, 1)]).back(r-2-2)
	#res += box(cable_protection_width, cable_protection_depth, cable_protection_height-5*2*2, center=True).back(cable_protection_depth/2-2)
	#res -= box(cable_protection_width, cable_protection_depth-4, cable_protection_height-5*2*2-8, center=True).back((cable_protection_depth-4)/2-2)
	res -= get_dropout_holes(True).up((cable_protection_height) / 2 - 5)#.forw((cable_protection_depth)/2.0-0.25)
	return res

#rib_ofs = 39.55/2+4+5
def display_shell(alpha):
	ofs_y = (wheel_arch_width+side_compartment_depth)/2
	'''
	rb_hole = rib.get_rib(True).up(side_compartment_height/2 - rib_ofs)
	rb = rib.get_rib(False)
	rb = rb.up(side_compartment_height/2 - rib_ofs)

	model = \
		(side_compartment.back(ofs_y) + \
		side_compartment.mirrorXZ().forw(ofs_y) - \
		rb_hole.left(side_compartment_width/2 - rib_ofs) - rb_hole.right(side_compartment_width/2 - rib_ofs)) + \
		rb.left(side_compartment_width/2 - rib_ofs) + rb.right(side_compartment_width/2 - rib_ofs)
	'''
	m = side_compartment.back(ofs_y) + side_compartment.mirrorXZ().forw(ofs_y)
	#m += side_compartment.rotateX(deg(-90)).up((side_compartment_height+side_compartment_depth)/2)

	top_width = side_compartment_width-5.5*2
	top_height = (side_compartment_depth-5.5)*2+wheel_arch_width
	top_depth = 4
	top1 = box(top_width, top_height, top_depth, center=True)
	
	cut = box(10, wheel_arch_width + 2*10, 2, center=True).left(top_width/4)
	cut += cylinder(5, 2, True).translate(-top_width/4, (wheel_arch_width + 2*10)/2, 0)
	cut += cylinder(5, 2, True).translate(-top_width/4, -(wheel_arch_width + 2*10)/2, 0)
	cut += box(10, (wheel_arch_width + 2*10) / 2, 2, center=True).forw((wheel_arch_width + 2*10) / 4)
	cut += cylinder(5, 2, True)#.translate(0, 0, 0)
	cut += cylinder(5, 2, True).translate(0, (wheel_arch_width + 2*10)/2, 0)
	top1 -= cut.up(1)
	
	top1 = top1.up(side_compartment_height/2)
	#top = fillet(proto=top, r=3, refs=[(0, -1, side_compartment_height), (-1, 0, side_compartment_height)])
	#top = fillet(proto=top, r=1, refs=[(-10, 0, side_compartment_height/2+10)])
	top1 -= m
	top2 = box(top_width, top_height, top_depth, center=True)
	top2 -= cut.down(1)
	top2 = top2.up((side_compartment_height+2*top_depth)/2)
	
	m += top1.up(15)
	m += top2.up(30)
	m += PG29.rotateZ(deg(90)).rotateX(deg(-1.5)).right((dropout_width+50*2+8)/2).forw(wheel_arch_width/2 + 50/2 + 0.4 + 1).down(side_compartment_height/2+35)
	m += from_brep('./1550Z102.brep').rotateX(deg(90)).up((side_compartment_height+2*top_depth)/2 + 25).up(45)
	
	#m += box(41, 57, 20, center=True).up((side_compartment_height+20)/2+8-2).left((side_compartment_width-11)/2-41/2)
	m += box(41, 57, 20, center=True).up((side_compartment_height-20-4)/2).left((side_compartment_width-11)/2-41/2)

	m = m.up(6)

	display(m, color=(0.5, 0.5, 0.5, alpha))

def display_shell_mounts():
	shell_height_half = (side_compartment_height) / 2
	sole_thick = dropout_height - dropout_sole_pos
	m = get_shell_mount()

	sole_thick = dropout_height - dropout_sole_pos
	sp = get_sm_spacer().up((dropout_height-sole_thick+4+4)/2)
	d = hole_d[10]
	spi = get_inner_spacer().up((dropout_height-sole_thick+0)/2+4+5.4)
	m += sp + spi.left((dropout_width+8+d*4)/2-d) + spi.right((dropout_width+8+d*4)/2-d)

	mr = ml = m.down(shell_height_half + dropout_m_axle_pos + (dropout_height-sole_thick)/2-dropout_m_axle_pos-2)
	ml = mr.back((wheel_arch_width+dropout_depth+4)/2)
	
	mr = mr.rotateZ(deg(180))
	mr += get_cable_protection().rotateZ(deg(180)).down(shell_height_half + dropout_m_axle_pos+3.5).right((cable_protection_width-dropout_width)/2).forw((dropout_depth)/2.0+4)
	mr = mr.forw((wheel_arch_width+dropout_depth+4)/2)
	display(ml + mr, color=(0.4, 0.5, 0.4, 0.5))

def display_wheel():
	shell_height_half = (side_compartment_height) / 2

	display(torus( \
		(tire_diameter_inch-tire_thickness_inch)*12.7, \
		tire_thickness_inch*12.7).rotateX(deg(90)).down(shell_height_half + dropout_m_axle_pos), \
		color=(0.1, 0.1, 0.1, 0.0)\
	)

	display(cylinder(12, 140, center=True).rotateX(deg(90)).down(shell_height_half + dropout_m_axle_pos)+\
			cylinder((tire_diameter_inch-2*tire_thickness_inch)*12.7, tire_thickness_inch*12.7, center=True)\
				.rotateX(deg(90)).down(shell_height_half + dropout_m_axle_pos), \
			color=(0.4, 0.2, 0.2, 0.0)
	)

	dropout = get_dropout().down(shell_height_half + dropout_height/2)
	display(\
		dropout.back((wheel_arch_width+dropout_depth)/2)+\
		dropout.mirrorXZ().forw((wheel_arch_width+dropout_depth)/2),\
		color=(0.4, 0.4, 0.4, 0.0))

def get_handle():
	width = side_compartment_width-70# - rib_ofs
	model = interpolate([\
		(-width*0.5, side_compartment_height), \
		(-width*0.25, side_compartment_height + 90), \
		(width*0.25, side_compartment_height + 90), \
		(width*0.5, side_compartment_height)], \
		[(0, 1), (1, 0), (1, 0), (0, -1)]).rotateX(deg(90))

	return sweep(circle(12, wire=True).left(width*0.5-15).up(side_compartment_height), model)


display_wheel()
#display_shell(0.5)
display_shell(0)
display_shell_mounts()

#display(get_handle().down(side_compartment_height/2+rib_ofs-20), color=(0.5, 0.5, 0.5, 0))
#display(get_handle().down(side_compartment_height/2+rib_ofs-6-10), color=(0.5, 0.5, 0.5, 0))
##display(get_handle().down(side_compartment_height/2+70-6-10), color=(0.5, 0.5, 0.5, 0))

#display(nut_m5)
show()