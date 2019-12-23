#!/usr/bin/env python3
#coding: utf-8

from math import sqrt, tan
import metric
from common import *
import mcm5dropout
import shell_mount

j1550 = from_brep('./1550J.brep').down((side_compartment_depth-8.11)/2).rotateY(deg(180))
spit_dt = 8.9

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
	res -= shell_mount.get_shell_mount_holes().down(side_compartment_height/2).forw(side_compartment_depth/2-shell_mount.top_mount_depth/2)
	res -= get_top_spacer_holls().up(side_compartment_height/2).back(top_height/2-side_compartment_depth/2)

	return res;
	
def get_upper_compartment():
	res = j1550
	tsh = get_top_spacer_holls().down(side_compartment_depth/2)
	res -= tsh.back((wheel_arch_width+top_height)/2)
	res -= tsh.forw((wheel_arch_width+top_height)/2)
	return res

def get_sm_spacer():
	d = hole_d[10]
	res = box(dropout_width+8+d*2*2, shell_mount.top_mount_depth, 4, center=True)
	res -= shell_mount.get_shell_mount_holes()

	res -= side_compartment_base.up(side_compartment_height/2).back(side_compartment_depth/2-shell_mount.top_mount_depth/2)
	res -= box(dropout_width+8+d*4, shell_mount.top_mount_depth, 4, center=True).up(4)
	return res

def get_inner_spacer():
	d = hole_d[10]
	h = 4
	back_dt = 1
	res = box(d*2, shell_mount.top_mount_depth-back_dt, h, center=True).back(back_dt/2)
	res -= cylinder(d/2, h, True)
	cut_depth = shell_mount.top_mount_depth/2
	cut = box(d*2, cut_depth, h, center=True).back(cut_depth/2) - cylinder(r=d, h=h, yaw=deg(180), center=True).rotateZ(deg(180))
	res -= cut

	res -= side_compartment_base.up(side_compartment_height/2-5.52).back(side_compartment_depth/2-shell_mount.top_mount_depth/2).right((dropout_width+8+d*4)/2-d)
	return res

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
	res += fillet(proto=box(cable_protection_width, cable_protection_depth, cable_protection_height-5*2, center=True), r=r, refs=[(0, -30, -1), (0, -30, 1)]).down(5).back(r-2)
	res -= fillet(proto=box(cable_protection_width, cable_protection_depth-4, cable_protection_height-5*2-8, center=True), r=r-2, refs=[(0, -30, -1), (0, -30, 1)]).down(5).back(r-2-2)
	res -= mcm5dropout.get_dropout_holes(HoleType.fasteners).up((cable_protection_height) / 2 - mcm5dropout.top_padding_holes)#.forw((cable_protection_depth)/2.0-0.25)
	return res

def get_top_spacer():
	m = side_compartment_base
	top = box(top_width, top_height, top_depth, center=True)
	m = m.down(side_compartment_height/2)
	top -= m
	top -= get_top_spacer_holls()
	return top

def get_shell():
	ofs_y = (wheel_arch_width+side_compartment_depth)/2

	sc = get_side_compartment()
	top = get_top_spacer().back(top_height/2-side_compartment_depth/2)
	top = top.up(side_compartment_height/2)
	sc += top
	spi = get_top_inner_spacer().up((side_compartment_height)/2 - 5.37)
	spi = spi.back(top_height/2-side_compartment_depth/2)
	d = hole_d[10]
	sc += spi.left(side_compartment_width/2 - spit_dt-d) + spi.mirrorYZ().right(side_compartment_width/2 - spit_dt-d)
	m = sc.back(ofs_y) + sc.rotateZ(deg(180)).forw(ofs_y)

	m += get_upper_compartment().up((side_compartment_height+side_compartment_depth+4)/2)
	#m += PG29.rotateZ(deg(90)).rotateX(deg(-1.5)).right((dropout_width+50*2+8)/2).forw(wheel_arch_width/2 + 50/2 + 0.4 + 1).down(side_compartment_height/2+35)
	
	vmu20_D1 = 25.8
	vmu20_S1 = 39 # меньше за счёт скруглений
	vmu20_S2 = 35
	vmu20_y = wheel_arch_width/2 +2.5 + gap(vmu20_S2/2)
	vmu20_y2 = wheel_arch_width/2 +side_compartment_depth - gap(vmu20_S2/2)
	#dt_right = (dropout_width+50*2+8)/2
	dt_right = side_compartment_width/2 - vmu20_S1/2 - 11
	m -= cylinder(vmu20_D1/2, 12, True).rotateX(deg(-1.5)).right(dt_right).forw(vmu20_y).down(side_compartment_height/2)
	nut = ngon((vmu20_S2 * 2 / sqrt(3))/2, 6, False).extrude(10)
	nut = nut.translate(0, -vmu20_S2/2, 0)
	nut = nut.rotateX(deg(-1.5))
	nut = nut.translate(0, vmu20_S2/2, 0)
	m += nut.right(dt_right).forw(vmu20_y).down(side_compartment_height/2 - ((vmu20_y2-vmu20_y) * tan(deg(1.5))) - 3)

	m = m.up(6)
	return m

def display_shell(alpha):
	m = get_shell()
	display(m, color=(0.5, 0.5, 0.5, alpha))

def display_shell_mounts():
	shell_height_half = (side_compartment_height) / 2
	m = shell_mount.get_shell_mount()

	sole_thick = dropout_height - dropout_sole_pos
	sp = get_sm_spacer().up((dropout_height-sole_thick+4+4)/2)
	d = hole_d[10]
	spi = get_inner_spacer().up((dropout_height-sole_thick)/2+4+5.52)
	m += sp + spi.left((dropout_width+8+d*4)/2-d) + spi.right((dropout_width+8+d*4)/2-d)

	mr = ml = m.down(shell_height_half + dropout_m_axle_pos + (dropout_height-sole_thick)/2-dropout_m_axle_pos-2)
	ml = mr.back((wheel_arch_width+shell_mount.top_mount_depth)/2)
	
	mr = mr.rotateZ(deg(180))
	mr += get_cable_protection().rotateZ(deg(180)).down(shell_height_half + dropout_m_axle_pos+4/2).right((cable_protection_width-dropout_width)/2).forw(-shell_mount.top_mount_depth/2 + dropout_depth+4+2)
	mr = mr.forw((wheel_arch_width+shell_mount.top_mount_depth)/2)
	display(ml + mr, color=(0.4, 0.5, 0.4, 0))#.5))

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

	dropout = mcm5dropout.get_dropout().down(shell_height_half + dropout_height/2)
	display(\
		dropout.back((wheel_arch_width+dropout_depth)/2)+\
		dropout.mirrorXZ().forw((wheel_arch_width+dropout_depth)/2),\
		color=(0.4, 0.4, 0.4, 0.0))

handle_ofs = -(4 + side_compartment_depth)
#def get_handle():
	#m = from_brep('./1427C5.brep')
	#m = m.rotateX(deg(90))
	#m = m.up(side_compartment_height/2+side_compartment_depth+4+6).left(108.35/2)
	#return m

def display_safety_arc():
	shell_height_half = (side_compartment_height) / 2
	wd = 355.6 # 14"
	wheel_arch_clearance = side_compartment_height+dropout_m_axle_pos - wd/2
	wd_padding = wd + wheel_arch_clearance*2

	a = (-wd_padding/2+wheel_arch_clearance, -(shell_height_half + dropout_m_axle_pos)-wheel_arch_clearance)
	b = (-side_compartment_width/2, shell_height_half + side_compartment_depth+4+6)
	c = (side_compartment_width/2, shell_height_half + side_compartment_depth+4+6)
	d = (wd_padding/2-wheel_arch_clearance, -(shell_height_half + dropout_m_axle_pos)-wheel_arch_clearance)
	m = interpolate(pnts=[a, b, c, d],
		tangs=[(0, 1), (1, 1), (1, -1), (0, -1)],
		closed=False
	)
	h = b[1] - a[1]
	k = (h + wheel_arch_clearance*2) / h
	pnts = m.uniform_points(6)
	rib = (cylinder(20/2, wheel_arch_width, True)-cylinder(hole_d[5]/2, wheel_arch_width, True)).rotateX(deg(90))
	t = 1+(k-1)/2
	ribs = nullshape()
	for rib in [rib.translate(pnt[0]*t, 0, pnt[1]*t) for pnt in pnts]:
		ribs += rib

	hl = circle(hole_d[5]/2).rotateX(deg(90))
	holes = nullshape()
	for hl in [hl.translate(pnt[0]*t, 0, pnt[1]*t) for pnt in pnts]:
		holes += hl

	# handle
	ribs += (cylinder(20/2, pnts[3][0]-pnts[2][0], True).rotateY(deg(90)).translate((pnts[2][0]+pnts[3][0])*t/2, 0, pnts[2][1]*t))

	m = sew([m, segment(a, d)])
	m = m.rotateX(deg(90))
	m = fill(m)

	m = m.translate(0, 0, -(b[1] - h/2))
	m = m.scale(k) - m
	m = m.translate(0, 0, (b[1] - h/2))

	cut = rectangle(wd, wheel_arch_clearance, center=True).rotateX(deg(90)).down(shell_height_half + dropout_m_axle_pos + wheel_arch_clearance+ wheel_arch_clearance/2 + (4+2)-6)
	m -= cut
	m -= holes

	m = m.extrude(vec=(0, 4, 0), center=True)
	m = m.back((wheel_arch_width+4)/2) + m.forw((wheel_arch_width+4)/2)
	m += ribs
	# поперечные:
	b1_height = side_compartment_height + 2 + side_compartment_depth
	b1_up = 6+(side_compartment_depth+2)/2
	'''
	b1 = box(4, side_compartment_depth+25, b1_height, center=True).back((wheel_arch_width+(side_compartment_depth+25))/2).left(side_compartment_width/2).up(b1_up)
	transverse_arc = fillet(proto=b1, r=25, refs=[
		(-side_compartment_width/2, -(wheel_arch_width/2 + (side_compartment_depth+25)), b1_up + b1_height/2),
		(-side_compartment_width/2, -(wheel_arch_width/2 + (side_compartment_depth+25)), -(b1_up + b1_height/2))
	])
	'''
	b1_width = side_compartment_depth+25
	b1 = box(4, b1_width, b1_height, center=True)
	transverse_arc = fillet(proto=b1, r=25, refs=[
		(0, -b1_width, b1_height/2),
		(0, -b1_width, -(b1_height/2))
	])
	cut_height = side_compartment_height-25*2
	cut = box(4, side_compartment_depth, cut_height, center=True).forw(25/2).down((b1_height-cut_height)/2 - 25)
	transverse_arc -= cut
	cut_height = side_compartment_depth+2-25
	cut = box(4, side_compartment_depth, cut_height, center=True).forw(25/2).up((b1_height-cut_height)/2-25)
	transverse_arc -= cut
	cut_height = 25
	cut_width = (side_compartment_height-wheel_arch_width)/2
	cut = box(4, cut_width, cut_height, center=True).forw(b1_width/2-cut_width/2).up((b1_height-cut_height)/2)
	transverse_arc -= cut
	transverse_arc = transverse_arc.translate(0, -b1_width/2, 0)
	transverse_arc = transverse_arc.rotateZ(deg(-1.5))
	transverse_arc = transverse_arc.translate(0, b1_width/2, 0)
	transverse_arc_mxz = transverse_arc.mirrorXZ()
	transverse_arc_myz = transverse_arc.mirrorYZ()
	transverse_arc_mxzyz = transverse_arc_mxz.mirrorYZ()
	m += transverse_arc.back((wheel_arch_width+b1_width)/2).left((side_compartment_width)/2).up(b1_up)
	m += transverse_arc_mxz.forw((wheel_arch_width+b1_width)/2).left((side_compartment_width)/2).up(b1_up)
	m += transverse_arc_myz.back((wheel_arch_width+b1_width)/2).right((side_compartment_width)/2).up(b1_up)
	m += transverse_arc_mxzyz.forw((wheel_arch_width+b1_width)/2).right((side_compartment_width)/2).up(b1_up)

	display(m, color=(0.3, 0.3, 0.3, 0))#.5))
	#display(ribs, color=(0.3, 0.3, 0.3, 0))#.5))

display_wheel()
#display_shell(0.5)
display_shell(0)
display_shell_mounts()

#display(get_handle().down(side_compartment_height/2+handle_ofs-6-10), color=(0.5, 0.5, 0.5, 0))

display_safety_arc()
show()
