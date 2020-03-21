#!/usr/bin/env python3
#coding: utf-8

from math import sqrt, tan
import metric
from common import *
import mcm5dropout

alp2020l = from_brep('.\\brep\\alp2020l.brep')
alp2040l = from_brep('.\\brep\\alp2040l.brep')
con2020d = from_brep('.\\brep\\con2020d.brep')
con2020 = from_brep('.\\brep\\con2020.brep').left(10).down(6.25).rotateY(deg(-90)).rotateX(deg(180))
con4040s = from_brep('.\\brep\\con4040s.brep').down((38.5-3.7)/2).rotateX(deg(90)).left(38.5/2).down(38.5/2)

gap_dropout_width = gap(dropout_width, 2)
gap_dropout_height = gap(dropout_height)
gap_dropout_depth = gap(dropout_depth)
gap_dropout_sole_pos = gap(dropout_sole_pos)

spit_dt = 8.9

'''
def get_side_compartment(is_right):
    res = side_compartment_base
    cut = sm.get_shell_mount_holes().down(side_compartment_height/2).forw(side_compartment_depth/2-sm.top_mount_depth/2)
    cut += get_top_spacer_holls().up(side_compartment_height/2).back(top_height/2-side_compartment_depth/2)

    if is_right:
        cut = cut.mirrorYZ()

    res -= cut
    
    if is_right:
        res = res.rotateZ(deg(180))

    return res;
    
def get_upper_compartment():
    res = j1550
    tsh = get_top_spacer_holls().down(side_compartment_depth/2)
    res -= tsh.back((wheel_arch_width+top_height)/2)
    res -= tsh.forw((wheel_arch_width+top_height)/2)

    #d = hole_d[10] 
    #nut = ngon((16 * 2 / sqrt(3))/2, 6, False).extrude(10).down(side_compartment_inner_depth/2)
    #res += nut.back((wheel_arch_width+top_height)/2).left(side_compartment_inner_width/2-spit_dt-d)
    
    return res
'''

def display_shell(alpha):
    m = get_alp2040(side_compartment_width).rotateY(deg(90)).rotateX(deg(-90))
    m = m.up(dropout_m_axle_pos + 10)

    h = side_compartment_height - 20*2
    m += m.up(h + 20)
    m1 = get_alp2040(h).rotateZ(deg(-90))
    m1 = m1.up(dropout_m_axle_pos + 20 + h/2)
    
    m += m1.left(side_compartment_width/2-10)
    m += m1.right(side_compartment_width/2-10)
    con = con4040s.back(38/4).up(dropout_m_axle_pos + 20 + 38.5/2)
    con = con.left(side_compartment_inner_width/2 - 38.5/2)
    m += con
    #m = m.back(wheel_arch_width/2 + 20 + gap_dropout_depth - 20 - 10)
    display(m, color=(0.5, 0.5, 0.5, alpha))

def get_alp2020(len):
    return alp2020l.scaleZ(len / 1000).up(len / 2)

def get_alp2040(len):
    return alp2040l.scaleZ(len / 1000).up(len / 2)
    
def get_con2020():
    return con2020

def display_shell_mounts():
    h = gap_dropout_sole_pos - 4
    m = get_alp2020(h)
    m = m.left(gap_dropout_width/2+10) + m.right(gap_dropout_width/2+10)

    con = get_con2020()
    con = con.up(h/2-10)
    con = con.back(10)
    dt = gap_dropout_width/2+17/2 + (20-17)/2
    m += con.left(dt)
    m += con.right(dt)

    con = get_con2020().rotateZ(deg(-90))#con2020d.rotateX(deg(180)).up(h/2-10+2).rotateZ(deg(-90))
    con = con.up(h/2-10)
    m += con.left(gap_dropout_width/2+20)
    m += con.rotateZ(deg(180)).right(gap_dropout_width/2+20)
    m = m.down(h/2 - dropout_m_axle_pos)
    m = m.back(wheel_arch_width/2 + gap_dropout_depth - 10)
    display(m)

def display_wheel():
    shell_height_half = (side_compartment_height) / 2

    display(torus( \
        (tire_diameter_inch-tire_thickness_inch)*12.7, \
        tire_thickness_inch*12.7).rotateX(deg(90)), \
        color=(0.1, 0.1, 0.1, 0.0)\
    )

    display(cylinder(12, 140, center=True).rotateX(deg(90))+\
            cylinder((tire_diameter_inch-2*tire_thickness_inch)*12.7, tire_thickness_inch*12.7, center=True)\
                .rotateX(deg(90)), \
            color=(0.4, 0.2, 0.2, 0.0)
    )

    dropout = mcm5dropout.get_dropout().down(dropout_height/2 - dropout_m_axle_pos)
    display(\
        dropout.back((wheel_arch_width+dropout_depth)/2)+\
        dropout.mirrorXZ().forw((wheel_arch_width+dropout_depth)/2),\
        color=(0.4, 0.4, 0.4, 0.0))

#display_wheel()
#display_shell_mounts()
#display_shell(0.5)
display_shell(0)

show()
