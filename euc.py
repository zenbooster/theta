#!/usr/bin/env python3
#coding: utf-8

import metric
from common import *
from zencad import *


PG29=from_brep('./PE_PG29.brep')
j1550 = from_brep('./1550j.brep').down((side_compartment_depth-8.11)/2).rotateY(deg(180))
nut_m5_len = dropout_depth
nut_m5 = metric.metric_nut(5, 0.8, nut_m5_len, False).rotateX(deg(90)).forw(nut_m5_len/2)
spit_dt = 8.9

def get_shell_mount_holes():
	d = hole_d[10]
	hole = cylinder(d/2, 10, True)
	res = hole.left((dropout_width+8+d*4)/2-d) + hole.right((dropout_width+8+d*4)/2-d)
	return res

def get_top_spacer_holls():
	d = hole_d[10]
	hole = cylinder(d/2, 10, True)
	#res = hole.left(side_compartment_width/4) + hole.right(side_compartment_width/4)
	res = hole.left(side_compartment_width/2 - spit_dt-d) + hole.right(side_compartment_width/2 - spit_dt-d)
	return res

def get_side_compartment_base():
	res = j1550
	res = res.rotateX(deg(90))
	return res

side_compartment_base = get_side_compartment_base()

def get_side_compartment():
	res = side_compartment_base
	res -= get_shell_mount_holes().down(side_compartment_height/2).forw(side_compartment_depth/2-(dropout_depth+4)/2)
	res -= get_top_spacer_holls().up(side_compartment_height/2).back(top_height/2-side_compartment_depth/2)

	return res;
	
def get_upper_compartment():
	res = j1550
	tsh = get_top_spacer_holls().down(side_compartment_depth/2)
	res -= tsh.back((wheel_arch_width+top_height)/2)
	res -= tsh.forw((wheel_arch_width+top_height)/2)
	return res

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
	res -= get_shell_mount_holes()
	res = res.up((dropout_height-sole_thick)/2)
	res += \
		box(dropout_width+8, dropout_depth+4, dropout_height - sole_thick+4, center=True) - \
		box(dropout_width, dropout_depth, dropout_height - sole_thick, center=True).translate(0, 2, -2) - \
		get_dropout_holes(True).up(dropout_height/2 - (dropout_sole_pos - 69) + 14 - (sole_thick/2+4/2)).back(dropout_depth/2)
	res -= cylinder(37/2, 4, True).rotateX(deg(90)).back(dropout_depth/2).up((dropout_height-sole_thick+4)/2-dropout_m_axle_pos-4)
	return res

def get_sm_spacer():
	d = hole_d[10]
	res = box(dropout_width+8+d*2*2, dropout_depth+4, 4, center=True)
	res -= get_shell_mount_holes()

	res -= side_compartment_base.up(side_compartment_height/2).back(side_compartment_depth/2-(dropout_depth+4)/2)
	res -= box(dropout_width+8+d*4, dropout_depth+4, 4, center=True).up(4)
	return res

def get_inner_spacer():
	d = hole_d[10]
	h = 4
	back_dt = 1
	res = box(d*2, dropout_depth+4-back_dt, h, center=True).back(back_dt/2)
	res -= cylinder(d/2, h, True)
	cut_depth = (dropout_depth+4)/2
	cut = box(d*2, cut_depth, h, center=True).back(cut_depth/2) - cylinder(r=d, h=h, yaw=deg(180), center=True).rotateZ(deg(180))
	res -= cut

	res -= side_compartment_base.up(side_compartment_height/2-5.52).back(side_compartment_depth/2-(dropout_depth+4)/2).right((dropout_width+8+d*4)/2-d)
	return res
'''
def get_sm_inner_spacer():
	d = hole_d[10]
	h = 4
	back_dt = 1
	res = box(d*2, top_height-back_dt, h, center=True).back(back_dt/2)
	res -= cylinder(d/2, h, True)
	cut_depth = top_height/2
	cut = box(d*2, cut_depth, h, center=True).back(cut_depth/2) - cylinder(r=d, h=h, yaw=deg(180), center=True).rotateZ(deg(180))
	res -= cut

	res -= side_compartment_base.down(side_compartment_height/2-5.37).back(side_compartment_depth/2-top_height/2).right((dropout_width+8+d*4)/2-d)
	return res
'''
def get_top_inner_spacer():
	d = hole_d[10]
	h = 4
	back_dt = 1
	res = box(d*2, top_height-back_dt, h, center=True).back(back_dt/2)
	res -= cylinder(d/2, h, True)
	cut_depth = top_height/2
	cut = box(d*2, cut_depth, h, center=True).back(cut_depth/2) - cylinder(r=d, h=h, yaw=deg(90), center=True).rotateZ(deg(180+90))
	cut -= box(d, d, h, center=True).left(cut_depth/4).back(d/2)
	res -= cut

	res -= side_compartment_base.down(side_compartment_height/2-5.37).back(side_compartment_depth/2-top_height/2).right(side_compartment_width/2 - spit_dt-d)
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

def get_top_spacer():
	m = side_compartment_base
	top = box(top_width, top_height, top_depth, center=True)
	m = m.down(side_compartment_height/2)
	top -= m
	top -= get_top_spacer_holls()
	return top

def display_shell(alpha):
	ofs_y = (wheel_arch_width+side_compartment_depth)/2

	sc = get_side_compartment()
	top = get_top_spacer().back(top_height/2-side_compartment_depth/2)
	top = top.up(side_compartment_height/2)
	sc += top
	#sc = top
	#spi = get_sm_inner_spacer().up((side_compartment_height)/2 - 5.37)
	spi = get_top_inner_spacer().up((side_compartment_height)/2 - 5.37)
	spi = spi.back(top_height/2-side_compartment_depth/2)
	#sc += spi.left(side_compartment_width/4) + spi.right(side_compartment_width/4)
	d = hole_d[10]
	sc += spi.left(side_compartment_width/2 - spit_dt-d) + spi.mirrorYZ().right(side_compartment_width/2 - spit_dt-d)
	m = sc.back(ofs_y) + sc.rotateZ(deg(180)).forw(ofs_y)

	m += get_upper_compartment().up((side_compartment_height+side_compartment_depth+4)/2)
	#m += get_side_compartment().rotateX(deg(-90)).up((side_compartment_height+side_compartment_depth+4)/2)
	m += PG29.rotateZ(deg(90)).rotateX(deg(-1.5)).right((dropout_width+50*2+8)/2).forw(wheel_arch_width/2 + 50/2 + 0.4 + 1).down(side_compartment_height/2+35)

	m = m.up(6)
	
	display(m, color=(0.5, 0.5, 0.5, alpha))

def display_shell_mounts():
	shell_height_half = (side_compartment_height) / 2
	sole_thick = dropout_height - dropout_sole_pos
	m = get_shell_mount()

	sole_thick = dropout_height - dropout_sole_pos
	sp = get_sm_spacer().up((dropout_height-sole_thick+4+4)/2)
	d = hole_d[10]
	spi = get_inner_spacer().up((dropout_height-sole_thick)/2+4+5.52)
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

handle_ofs = -(4 + side_compartment_depth)
def get_handle():
	m = from_brep('./1427C5.brep')
	m = m.rotateX(deg(90))
	m = m.up(side_compartment_height/2+side_compartment_depth+4+6).left(108.35/2)
	return m

display_wheel()
display_shell(0.5)
#display_shell(0)
display_shell_mounts()

display(get_handle().down(side_compartment_height/2+handle_ofs-6-10), color=(0.5, 0.5, 0.5, 0))

#display(get_top_spacer())
show()