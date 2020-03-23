#!/usr/bin/env python3
#coding: utf-8

from math import sqrt, tan
import metric
from common import *
import mcm5dropout

alp2020l = from_brep('.\\brep\\alp2020l.brep')
alp2040l = from_brep('.\\brep\\alp2040l.brep').left(10)
con2020d = from_brep('.\\brep\\con2020d.brep')
con2020 = from_brep('.\\brep\\con2020.brep').left(10).down(6.25).rotateY(deg(-90)).rotateX(deg(180))
#con2040 = from_brep('.\\brep\\con2040d.brep').right(38.1/2).back(38.1/2).down(17.4/2).rotateX(deg(90)).rotateZ(deg(-90)).rotateX(deg(-90))
#con2040 = from_brep('.\\brep\\con2040d.brep').right(38.1/2).back(38.1/2).down(17.4/2)#.rotateZ(deg(-90))
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
    mv = get_alp2040(side_compartment_height - 20*2).rotateZ(deg(90))
    mh = get_alp2040(side_compartment_width).rotateZ(deg(90)).rotateY(deg(90)).down(side_compartment_height/2 - 10)
    m = mv.left(side_compartment_width/2 - 10) + mh
    con = con4040s.down(side_compartment_height/2 - 20 - 38.5/2)
    con = con.left(side_compartment_inner_width/2 - 38.5/2)
    con += con.mirrorYZ()
    m += con
    m += m.rotateY(deg(180))
    
    m = m.up(side_compartment_height/2 + dropout_m_axle_pos)
    m = m.back(wheel_arch_width/2 + 20 + gap_dropout_depth - 20)
    m += m.mirrorXZ()
    
    hv = tire_diameter_inch*12.7 + 10 + 20
    ddt = dropout_depth - 20
    dcdt = ddt - cover_thickness
    htop = wheel_arch_width - 40 - dcdt*2 - cover_thickness*2
    rib = get_alp2020(htop).rotateX(deg(90)).up(hv)
    rib = rib.left(side_compartment_width/2 - 10)
    rib += rib.mirrorYZ()
    rib2 = get_alp2020(wheel_arch_width + ddt*2).rotateX(deg(90)).up(hv)
    rib2 = rib2.left(side_compartment_width/2 - 10)
    rib2 += rib2.mirrorYZ()
    rib2 = rib2.up(10+dropout_m_axle_pos - hv + side_compartment_height - 20)
    m += rib + rib2
    guide = get_alp2020(side_compartment_width).rotateY(deg(90))
    guide = guide.up(hv)
    guide = guide.back(wheel_arch_width/2 - 10 + dcdt)
    guide += guide.mirrorXZ()
    m += guide
    
    h = hv - dropout_m_axle_pos + 10
    inner_cover = box(side_compartment_width, h, cover_thickness, center = True).rotateX(deg(90))
    inner_cover = inner_cover.back(wheel_arch_width/2 - cover_thickness/2 + dropout_depth - 20)
    inner_cover = inner_cover.up(h/2 + dropout_m_axle_pos)
    inner_cover += inner_cover.mirrorXZ()
    m += inner_cover
    '''
    con = con2040.up(hv+17.4/2).left(side_compartment_inner_width/2 - 38.1/2)
    con = con.back(wheel_arch_width/2 - 20 - 38.1/2 - dcdt).up(5)
    '''
    con = con2020d.rotateY(deg(90)).up(hv).left(side_compartment_inner_width/2 - 18/2).back(wheel_arch_width/2 - 20 - 18/2 + dcdt)
    con += con.mirrorXZ()
    con += con.mirrorYZ()
    m += con
    
    con = con2020.rotateX(deg(90)).up(hv-10 - cover_thickness).left(side_compartment_width/2 - 17/2).back(wheel_arch_width/2 - 20/2 + dcdt)
    con += con.mirrorXZ()
    con += con.mirrorYZ()
    m += con
    
    inner_cover = box(side_compartment_width, htop + 20*2, cover_thickness, center = True).up(hv - 10 - cover_thickness/2)
    m += inner_cover
    
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

    con = get_con2020().rotateZ(deg(-90))
    con = con.up(h/2-10)
    m += con.left(gap_dropout_width/2+20)
    m += con.rotateZ(deg(180)).right(gap_dropout_width/2+20)
    m = m.down(h/2 - dropout_m_axle_pos)
    m = m.back(wheel_arch_width/2 + gap_dropout_depth - 10)
    m += m.mirrorXZ()
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
display_shell_mounts()
#display_shell(0.5)
display_shell(0)

len2040v = side_compartment_height - 20*2
len2040h = side_compartment_width
print("2040:\n4 x {}\n4 x {}\n".format(len2040v, len2040h))
len_gap = 0
len2040 = (len2040v + len_gap) * 4 + (len2040h + len_gap) * 4
print("length of 2040 = {}\n".format(len2040))

len2020v = (gap_dropout_sole_pos - 4)
len2020h_rib = wheel_arch_width - 40 - dcdt*2 - cover_thickness*2
print("2020:\n4 x {}\n2 x {}\n".format(len2020v, len2020h_rib))
len2020 = len2020v*4 + len2020h_rib*2
print("length of 2020 = {}\n".format(len2020))

show()
