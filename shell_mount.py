#!/usr/bin/env python3
#coding: utf-8
from math import sqrt
from common import *
import mcm5dropout

hex_nut_m10_d = gap(17)
#hex_nut_m10_D = 18.9
#side_compartment_thickness_at_the_base = 2.5
side_compartment_thickness_at_the_base = 5 # IRL, уже напечатали просто
top_mount_depth = bearing_width[10] + side_compartment_thickness_at_the_base * 2
lug_depth = top_mount_depth

gap_dropout_width = gap(dropout_width, 2)
gap_dropout_height = gap(dropout_height)
gap_dropout_depth = gap(dropout_depth)
gap_dropout_sole_pos = gap(dropout_sole_pos)

def get_shell_mount_holes():
	d = hole_d[10]
	hole = cylinder(d/2, 10, True)
	res = hole.left((gap_dropout_width+8+d*4)/2-d) + hole.right((gap_dropout_width+8+d*4)/2-d)
	return res

def get_stiffener(a):
	res = box(a, 4, a, center=True)
	c = sqrt(a*a+a*a)
	cut = box(c, 4, c, center=True).rotateY(deg(45))
	res -= cut.down(a/2).left(a/2)
	return res

def get_shell_mount():
	sole_thick = gap_dropout_height - gap_dropout_sole_pos
	d = hole_d[10]
	top_mounting = box(gap_dropout_width+8+d*2*2, top_mount_depth, 4, center=True)
	top_mounting -= get_shell_mount_holes()
	res = top_mounting
	stiffener = get_stiffener(d*2)
	stiffener = stiffener.down(2+d)
	stiffener = stiffener.left((gap_dropout_width+8+d*2*2)/2 - d)
	stiffener += stiffener.mirrorZ()
	dt_stiffener_y = hex_nut_m10_d/2+2
	stiffener = stiffener.forw(dt_stiffener_y) + stiffener.back(dt_stiffener_y)
	res += stiffener
	res = res.up((gap_dropout_height-sole_thick)/2)
	gap_hbh = mcm5dropout.get_dropout_higher_bevel_height()-gap(4.3)
	dt_down = (gap_hbh - (gap_dropout_height - sole_thick))/2
	dt_down4 = (gap_hbh+4 - (gap_dropout_height - sole_thick+4))/2
	dt_down_d2 = (gap_hbh-d*2 - (gap_dropout_height - sole_thick-d*2))/2
	res += box(gap_dropout_width+8, lug_depth, gap_hbh+4, center=True).down(dt_down4).forw(top_mount_depth/2-lug_depth/2)
	# делаем полость под стойку:
	res -= box(gap_dropout_width, gap_dropout_depth, gap_hbh, center=True).down(dt_down).translate(0, top_mount_depth/2-gap_dropout_depth/2, -2)
	fwd_cut_depth = lug_depth - gap_dropout_depth-4
	res -= box(gap_dropout_width, fwd_cut_depth, gap_hbh+4, center=True).down(dt_down4).translate(0, top_mount_depth/2-gap_dropout_depth-(fwd_cut_depth/2+4), -2+2)
	res -= box(gap_dropout_width+8, fwd_cut_depth, gap_hbh-d*2, center=True).down(dt_down_d2).translate(0, top_mount_depth/2-gap_dropout_depth-(fwd_cut_depth/2+4), -2-d)
	stiffener = get_stiffener(fwd_cut_depth).rotateZ(deg(90))
	stiffener = stiffener.translate(-(gap_dropout_width/2+4)+4/2, 0, (gap_dropout_height-sole_thick-4)/2-fwd_cut_depth/2-d*2)
	stiffener += stiffener.mirrorYZ()
	stiffener = stiffener.forw(top_mount_depth/2-gap_dropout_depth-(fwd_cut_depth/2+4))
	res += stiffener

	dt_holes_back = (lug_depth-4)/2-fwd_cut_depth
	res -= mcm5dropout.get_dropout_holes(HoleType.fasteners).up(gap_dropout_height/2 - mcm5dropout.top_padding_holes - (sole_thick/2+4/2)).back(dt_holes_back)
	res -= cylinder(gap(mcm5dropout.wheel_axle_big_d/2), 4, True).rotateX(deg(90)).back(dt_holes_back).up((gap_dropout_height-sole_thick-4)/2-dropout_m_axle_pos)
	return res

if __name__ == "__main__":
	m = get_shell_mount()
	#to_stl(m, 'd:\shell_mount.stl', 0.01)
	display(m)#, color=(1, 1, 1, 0.5))
	show()