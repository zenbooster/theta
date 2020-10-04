#!/usr/bin/env python3
#coding: utf-8
from zencad import *

instrument_delta = -0.0001

def getH(P):
	H = P * math.cos(deg(30))
	#H = P * 0.866025404
	return H

@lazy
def instrument_metric_ext(d, step, h):
	r = d / 2
	H = getH(step)
	d2 = d - 2*(3 / 8 * H)
	r2 = d2 / 2

	d1 = d - 2*(5/8*H)
	r1 = d1 / 2
	d3 = d - 2*(17/24*H)
	r3 = d3 / 2

	p0 = point3(r, 0, 0)
	p1 = point3(r, 0, -(1/8*step))
	p2 = (r1, 0, -((8+1-2)/16*step))
	p3 = (r1, 0, -((8+1+2)/16*step))
	p4 = (r, 0, -step)
	p5 = (r2+H, 0, -step)
	p6 = (r2+H, 0, 0)

	r4 = (1/8*H)/3.4641
	pseg = sew([ \
		segment(p0, p1), \
		segment(p1, p2), \
		#segment(p2, p3), \
		circle_arc(p2, (r1 - (1/4*step)/3.4641, 0, -((8+1)/16*step)), p3), \
		segment(p3, p4), \
		segment(p4, p5), \
		segment(p5, p6), \
		segment(p6, p0)
	]).left(instrument_delta)

	'''
	display(segment(point(r, 0, 0), point(r, 0, -step)).down(0.75), color=color(1, 0, 0))
	display(segment(point(r1, 0, 0), point(r1, 0, -step)).down(0.75), color=color(1, 0.5, 0))
	display(segment(point(r2, 0, 0), point(r2, 0, -step)).down(0.75), color=color(1, 1, 0))
	display(segment(point(r3, 0, 0), point(r3, 0, -step)).down(0.75), color=color(0, 1, 0))
	m = pseg.up(step+0.4)
	for i in range(4):
		print(i)
		m += m.down(int(step)<<i)

	rib_ofs = 39.55/2+4+5
	display(m.rotateX(deg(90)).back(wheel_arch_width/2+screw_m24_len).up(side_compartment_height/2 - rib_ofs-12+2).left(side_compartment_width/2 - rib_ofs))
	'''
	path = helix(r=r2, h=h, step=step)
	base = pipe_shell(spine = path, profiles = [pseg], frenet = True)
	return base

def instrument_metric_int(d, step, h):
	r = d / 2
	H = getH(step)
	d2 = d - 2*(3 / 8 * H)
	r2 = d2 / 2

	d1 = d - 2*(5/8*H)
	r1 = d1 / 2
	d3 = d - 2*(17/24*H)
	r3 = d3 / 2

	p0 = point3(r + 0.125*H, 0, 0)
	p1 = point3(r1, 0, -(3/8*step))
	p2 = point3(r1, 0, -(5/8*step))
	p3 = point3(r + 0.125*H, 0, -step)
	p4 = (r2+H, 0, -step)
	p5 = (r2+H, 0, 0)

	r4 = (1/8*H)/3.4641
	pseg = sew([ \
		segment(p0, p1), \
		segment(p1, p2), \
		segment(p2, p3), \
		segment(p3, p4), \
		segment(p4, p5), \
		segment(p5, p0) \
	]).left(instrument_delta)

	'''
	display(segment(point(r, 0, 0), point(r, 0, -step)).down(0.75), color=color(1, 0, 0))
	display(segment(point(r1, 0, 0), point(r1, 0, -step)).down(0.75), color=color(1, 0.5, 0))
	display(segment(point(r2, 0, 0), point(r2, 0, -step)).down(0.75), color=color(1, 1, 0))
	display(segment(point(r3, 0, 0), point(r3, 0, -step)).down(0.75), color=color(0, 1, 0))

	m = pseg.up(step+0.4)
	for i in range(4):
		print(i)
		m += m.down(step*(1<<i))
	#rib_ofs = 39.55/2+4+5
	display(m.rotateX(deg(90)).left(10))#.down(shell_height_half + side_compartment_wheel_axle_distance + dropout_height/2-dropout_m_axle_pos).back(150))
	'''
	path = helix(r=r2, h=h, step=step)
	base = pipe_shell(spine = path, profiles = [pseg], frenet = True)
	
	return base

@lazy
def metric_screw(d, step, h, is_chamfer):
	z = {
		0.8 : 1.0,
		1.25: 1.6,
		1.5 : 1.6,
		3.0 : 2.5
	}

	a = {
		0.8	: 1.6,
		1.25: 2.5,
		1.5 : 2.5,
		3.0 : 4
	}

	if is_chamfer:
		vz = (step in z) and z[step] or 1
		H = getH(step)
		cil = cylinder(r=d / 2, h=h)
		#cil = cylinder(r=12.325, h=h-0)
		instr = instrument_metric_ext(d=d, step=step, h=h + step-vz)
		ret = cil - instr
		#ret = instr
		chm = (cylinder(r=d / 2, h=vz*2).chamfer(vz, refs=[point(0, 0, h)]) - \
			cylinder(r=d / 2, h=vz)).mirrorX().up(vz*2)

		ret = (ret - cylinder(r=d / 2, h=vz)) + (ret ^ chm)
		ret = (ret - cylinder(r=d / 2, h=vz).up(h-vz)) + (ret ^ chm.up(h-vz))

	else:
		cil = cylinder(r=d / 2, h=h)
		instr = instrument_metric_ext(d=d, step=step, h=h + step)
		ret = cil - instr

	return ret

@lazy
def metric_nut(d, step, h, is_chamfer):
	if is_chamfer:
		return None
	else:
		H = getH(step)
		cil = cylinder(r=d / 2 + 0.125*H, h=h)
		instr = instrument_metric_int(d=d, step=step, h=h + step)
		ret = cil - instr

	return ret
