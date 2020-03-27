#!/usr/bin/env python3
#coding: utf-8

from math import sqrt, tan, ceil
import metric
from common import *
import mcm5dropout

#alp2020l = from_brep('.\\brep\\alp2020l.brep')
alp2020l = from_brep('.\\brep\\alp2020almk.brep').left(47.4).back(75.2)
#alp2040l = from_brep('.\\brep\\alp2040l.brep').left(10)
alp2040l = from_brep('.\\brep\\alp2040almk.brep').back(81.55).left(37.25)
con2020d = from_brep('.\\brep\\con2020d.brep')
con2020 = from_brep('.\\brep\\con2020.brep').left(10).down(6.25).rotateY(deg(-90)).rotateX(deg(180))
#con2040 = from_brep('.\\brep\\con2040d.brep').right(38.1/2).back(38.1/2).down(17.4/2).rotateX(deg(90)).rotateZ(deg(-90)).rotateX(deg(-90))
con2040 = from_brep('.\\brep\\con2040d.brep').right(38.1/2).back(38.1/2).down(17.4/2)#.rotateZ(deg(-90))
con2040s = from_brep('.\\brep\\con2040s.brep').down(18/2 - 2).left(38.5/2).back(38.5/2).rotateX(deg(90)).rotateY(deg(180))
con4040s = from_brep('.\\brep\\con4040s.brep').down((38.5-3.7)/2).rotateX(deg(90)).left(38.5/2).down(38.5/2)
#cub3 = from_brep('.\\brep\\cub3.brep').down(10).rotateX(deg(180))

gap_dropout_width = gap(dropout_width, 2)
gap_dropout_height = gap(dropout_height)
gap_dropout_depth = gap(dropout_depth)
gap_dropout_sole_pos = gap(dropout_sole_pos)

ddt = gap_dropout_depth - 20
dcdt = ddt - cover_thickness

len2020v = (gap_dropout_sole_pos - 4)
len2020h_rib = wheel_arch_width - 40 + dcdt*2# - cover_thickness*2
len2020h_rib2 = wheel_arch_width + ddt*2
len2020_guid = side_compartment_width
len2020_drw = dropout_width + 20*2

dmns_shell_mount_cover = (dropout_width + 20*2, cover_thickness, len2020v + 20)

def display_shell(alpha):
    mv = get_alp2040(side_compartment_height - 20*2).rotateZ(deg(90))
    #mh = get_alp2040(side_compartment_width - 20*2).rotateZ(deg(90)).rotateY(deg(90)).down(side_compartment_height/2 - 10)
    mh = get_alp2040(side_compartment_width).rotateZ(deg(90)).rotateY(deg(90)).down(side_compartment_height/2 - 10)
    m = mv.left(side_compartment_width/2 - 10) + mh
    con = con4040s.down(side_compartment_height/2 - 20 - 38.5/2)
    con = con.left(side_compartment_inner_width/2 - 38.5/2)
    con += con.mirrorYZ()
    m += con
    m += m.rotateY(deg(180))
    
    #m += cub3.up(side_compartment_height/2-10).left(side_compartment_width/2 - 10).forw(10)
    
    m = m.up(side_compartment_height/2 + dropout_m_axle_pos + 20)
    m = m.back(wheel_arch_width/2 + 20 + ddt)
    m += m.mirrorXZ()
    
    hv = tire_diameter_inch*12.7 + 10 + 20
    htop = len2020h_rib
    rib = get_alp2020(htop).rotateX(deg(90)).up(hv)
    rib = rib.left(side_compartment_width/2 - 10)
    rib += rib.mirrorYZ()
    rib2 = get_alp2020(len2020h_rib2).rotateX(deg(90)).up(hv)
    rib2 = rib2.left(side_compartment_width/2 - 10)
    rib2 += rib2.mirrorYZ()
    rib2 = rib2.up(10+dropout_m_axle_pos - hv + side_compartment_height)
    m += rib + rib2
    guide = get_alp2020(len2020_guid).rotateY(deg(90))
    guide = guide.up(hv)
    guide = guide.back(wheel_arch_width/2 - 10 + dcdt)
    guide += guide.mirrorXZ()
    m += guide
    
    h = hv - dropout_m_axle_pos + 10 - 20
    icl = box(side_compartment_width, h, cover_thickness, center = True).rotateX(deg(90))
    hole = cylinder(hole_d[5]/2, cover_thickness, True).rotateX(deg(90))
    holes = hole.up(h/2 - 10).left(side_compartment_width/2 - 10)
    holes += holes.mirrorYZ()
    holes += holes.down(20 + cover_thickness)
    holes += holes.mirrorXY()
    holes += holes + hole.down(h/2 - 10)
    holes += hole.left(side_compartment_width/2 - 10) + hole.right(side_compartment_width/2 - 10)
    t = hole.up(h/2 - 10)
    holes_l = holes + t
    t = t.left(ctrl_width/2 + gap(11.8/2)) # 11.8 - самый большой диаметр шляпки винта М5, что удалось на вскидку найти...
    holes_r = holes + t + t.mirrorYZ()
    icl -= holes_l
    #to_brep(icl.rotateX(deg(90)), "vector/icl.brep")
    
    hicr = 20 + common_clearance + ctrl_height
    icr = box(side_compartment_width, hicr, cover_thickness, center = True).rotateX(deg(90))
    icr = icr.up((hicr - h)/2)
    icr -= holes_r
    icl = icl.back(wheel_arch_width/2 - cover_thickness/2 + ddt)
    icr = icr.forw(wheel_arch_width/2 - cover_thickness/2 + ddt)
    icl = icl.up(h/2 + dropout_m_axle_pos + 20)
    icr = icr.up(h/2 + dropout_m_axle_pos + 20)
    #inner_cover += inner_cover.mirrorXZ()
    inner_cover = icl + icr
    m += inner_cover

    con = con2020d.rotateY(deg(90)).up(hv).left(side_compartment_inner_width/2 - 18/2).back(wheel_arch_width/2 - 20 - 18/2 + dcdt)
    con += con.mirrorXZ()
    con += con.mirrorYZ()
    m += con
    
    #con = con2020.rotateX(deg(90)).up(hv-10 - cover_thickness).left(side_compartment_width/2 - 17/2).back(wheel_arch_width/2 - 20/2 + dcdt)
    con = con2020.rotateX(deg(90)).up(hv-10 - cover_thickness).left(side_compartment_width/2 - 20/2).back(wheel_arch_width/2 - 20/2 + dcdt)
    con += con.mirrorXZ()
    con += con.mirrorYZ()
    m += con
    
    hitc = htop + 20*2
    inner_cover = box(side_compartment_width, hitc, cover_thickness, center = True)
    hole = cylinder(hole_d[5]/2, cover_thickness, True)
    holes = hole.forw(hitc/2 - 10).left(side_compartment_width/2 - 10)
    holes += holes.mirrorYZ()
    holes += hole.forw(hitc/2 - 10)
    holes += holes.mirrorXZ()
    holes2 = hole.forw(hitc/2-10-20).left(side_compartment_width/2 - 10)
    holes2 += holes2.mirrorYZ()
    holes2 += holes2.mirrorXZ()
    holes += holes2
    inner_cover -= holes
    #to_brep(inner_cover, "vector/ict.brep")
    inner_cover = inner_cover.up(hv - 10 - cover_thickness/2)
    m += inner_cover
    
    #con = con2040.rotateY(deg(90)).rotateZ(deg(180)).rotateX(deg(180)).up(hv + 10 + 38.1/2).left(side_compartment_width/2 - 17.4/2)
    con = con2040.rotateX(deg(180)).rotateZ(deg(90)).up(dropout_m_axle_pos + side_compartment_height + 20 - 17.4/2).left(side_compartment_inner_width/2 - 38.1/2)
    con = con.back(len2020h_rib2 / 2 - 38.1/2)
    con += con.mirrorYZ()
    con += con.mirrorXZ()
    m += con
    con = con2040.rotateY(deg(90)).up(dropout_m_axle_pos + side_compartment_height - 38.1/2).left(side_compartment_width/2 - 17.4/2)
    con = con.back(len2020h_rib2 / 2 - 38.1/2)
    con += con.mirrorYZ()
    con += con.mirrorXZ()
    m += con
    
    outer_cover = box(side_compartment_width, side_compartment_height, cover_thickness, center = True).rotateX(deg(90))
    hole = hole.rotateX(deg(90))
    hup = hole.up(side_compartment_height/2 - 10)
    t = hole.left(side_compartment_width/2 - 10)
    t += t.mirrorYZ()
    holes = t.up(side_compartment_height/2 - 10)
    holes += t.up(side_compartment_height/2 - 30)
    holes += hup
    holes += holes.mirrorXY()
    holes += t
    outer_cover -= holes

    outer_cover = outer_cover.up(side_compartment_height/2 + dropout_m_axle_pos + 20)
    outer_cover = outer_cover.back(wheel_arch_width/2 + 40 + cover_thickness/2 + ddt)
    outer_cover += outer_cover.mirrorXZ()
    m += outer_cover

    hotc = htop + 40*2 + ddt*2
    outer_cover = box(side_compartment_width, hotc, cover_thickness, center = True)
    hole = cylinder(hole_d[5]/2, cover_thickness, True)
    holes = hole.forw(hotc/2 - 10).left(side_compartment_width/2 - 10)
    holes += holes.mirrorYZ()
    holes += hole.forw(hotc/2 - 10)
    holes += holes.mirrorXZ()
    holes2 = hole.forw(hotc/2-10-20).left(side_compartment_width/2 - 10)
    holes2 += holes2.mirrorYZ()
    holes2 += holes2.mirrorXZ()
    holes += holes2
    holes2 = hole.left(side_compartment_width/2 - 10)
    holes2 += holes2.mirrorYZ()
    holes += holes2
    outer_cover -= holes
    #to_brep(outer_cover, "vector/ict.brep")
    outer_cover = outer_cover.up(dropout_m_axle_pos + 20 + side_compartment_height + cover_thickness/2)
    m += outer_cover
    
    front_width = wheel_arch_width + 2*ddt + 2*40 + 2*cover_thickness
    front_height = batt_2p_depth + 2 * common_clearance + 20 + 2*cover_thickness
    front_cover = box(front_width, cover_thickness, front_height, center=True)
    #
    cut_width = 20 + cover_thickness
    cut = box(cut_width, cover_thickness, cover_thickness, center=True).up(front_height/2 - cover_thickness/2)
    cut = cut.left(front_width/2 - cut_width/2)
    cut += cut.mirrorYZ()
    front_cover -= cut
    
    cut_width = 20
    cut_height = front_height-40
    cut = box(20, cover_thickness, cut_height, center=True).up(front_height/2 - 40 - cut_height/2)
    cut = cut.left(front_width/2 - cut_width/2)
    cut += cut.mirrorYZ()
    front_cover -= cut
    #
    front_cover = front_cover.rotateZ(deg(90))
    front_cover = front_cover.left(side_compartment_width/2 + cover_thickness/2)
    front_cover = front_cover.up(hv - 10 + front_height/2 - cover_thickness)
    front_cover += front_cover.mirrorYZ()
    m += front_cover
    display(m, color=(0.5, 0.5, 0.5, alpha))

def get_alp2020(len):
    #return alp2020l.scaleZ(len / 1000).up(len / 2)
    return alp2020l.scaleZ(len / 100).up(len / 2)

def get_alp2040(len):
    #return alp2040l.scaleZ(len / 1000).up(len / 2)
    return alp2040l.scaleZ(len / 100).up(len / 2)
    
def get_con2020():
    return con2020

def display_shell_mounts():
    h = len2020v
    m = get_alp2020(h)
    m = m.left(gap_dropout_width/2+10) + m.right(gap_dropout_width/2+10)
    m = m.down(20)

    conl = con2040s
    conr = conl.rotateY(deg(-90))
    dtl = gap_dropout_width/2+20+38.5/2
    conl = conl.left(dtl)
    conr = conr.right(dtl)
    con = conl + conr
    con = con.up(h/2-38.5/2)
    m += con
    m += get_alp2020(len2020_drw).rotateY(deg(90)).up(h / 2 - 10)

    dt_holes_back = 0
    sole_thick = gap_dropout_height - gap_dropout_sole_pos    
    #cov = box(dropout_width + 20*2, cover_thickness, h + 20, center=True)
    dsmc = dmns_shell_mount_cover
    cov = box(dsmc[0], dsmc[1], dsmc[2], center = True)
    
    '''
    d = hole_tap_d[5]
    n = cylinder(d/2, nut_m5_len, True).rotateX(deg(90))
    holes = n.up((h+20)/2 - 10).left((dropout_width+20*2)/2 - 10)
    holes += holes.mirrorYZ()
    holes = holes.down(20) + holes.mirrorXY()

    holes0 = n.up((h+20)/2 - 10).left((dropout_width+20*2)/2 - 30)
    holes0 += holes0.mirrorYZ()
    holes += holes0
    cov -= holes
    cut = box(20, cover_thickness, 20, center=True).up((h+20)/2-10).left((dropout_width + 20*2)/2 - 10)
    cut += cut.mirrorYZ()
    cov -= cut
    '''
    d = hole_d[5]
    n = cylinder(d/2, nut_m5_len, True).rotateX(deg(90))
    holes = n.up((h+20)/2 - 10).left((dropout_width+20*2)/2 - 10)
    holes += holes.mirrorYZ()
    holes += holes.down(20) + holes.mirrorXY()
    cov -= holes

    cov = cov.down(-10)
    cov -= mcm5dropout.get_dropout_holes(HoleType.fasteners).up(gap_dropout_height/2 - mcm5dropout.top_padding_holes - (sole_thick/2+4/2)).back(dt_holes_back)
    cov -= cylinder(gap(mcm5dropout.wheel_axle_big_d/2), 4, True).rotateX(deg(90)).back(dt_holes_back).up((gap_dropout_height-sole_thick-4)/2-dropout_m_axle_pos)

    #to_brep(cov.rotateX(deg(-90)), "vector/smcov.brep")

    cov = cov.down(10+10).back(10 + cover_thickness/2)
    #m += cov

    m = m.down(h/2 - dropout_m_axle_pos - 20)
    m = m.back(wheel_arch_width/2 + gap_dropout_depth - 10)
    m += m.mirrorXZ()
    display(m)
    
    cov = cov.down(h/2 - dropout_m_axle_pos - 20)
    cov = cov.back(wheel_arch_width/2 + gap_dropout_depth - 10)
    cov += cov.mirrorXZ()
    display(cov, color=(0.5, 0.75, 0.5, 0.25))

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

display_wheel()
display_shell_mounts()
#display_shell(0.5)
display_shell(0)
#m = get_alp2040(100)
#display(m)

kgap = 4
len2040v = side_compartment_height - 20*2
len2040h = side_compartment_width
print("2040:\n4 x {}\n4 x {}\n".format(len2040v, len2040h))
len2040 = len2040v * 4 + len2040h * 4
len_gap = 8*kgap
len2040_gap = ceil(len2040 + len_gap)

k2040weight = 0.8
k2040cost = 410
cost2040 = k2040cost * len2040_gap / 1000
weight2040 = k2040weight * len2040

print("length of 2040 = {}\nwith gap = {}\ncost = {}".format(len2040, len2040_gap, cost2040))

print("2020:\n4 x {}\n2 x {}\n2 x {}\n2 x {}\n2 x {}\n".format(len2020v, len2020h_rib, len2020h_rib2, len2020_guid, len2020_drw))
len2020 = len2020v * 4 + len2020h_rib * 2 + len2020h_rib2 * 2 + len2020_guid * 2 + len2020_drw * 2
len_gap = (4 + 2 + 2 + 2 + 2)*kgap
len2020_gap = ceil(len2020 + len_gap)

k2020weight = 0.45
k2020cost = 195
cost2020 = k2020cost * len2020_gap / 1000
weight2020 = k2020weight * len2020

print("length of 2020 = {}\nwith gap = {}\ncost = {}".format(len2020, len2020_gap, cost2020))

cost = cost2040 + cost2020
weight = weight2040 + weight2020
wgtCBS5 = 2+3+1+1 # сухарь, болт, шайба, гровер
wgtCBS4 = 2+2+1+1
weight += (33 + 8*wgtCBS5)*8 # уголки 40x40
weight += (9 + 4*wgtCBS5)*8 # уголки 20x40
weight += (9 + 2*wgtCBS4)*4 # уголки 20x20 с фикс.
weight += (7 + 2*wgtCBS5)*4 # уголки 20x20
weight /= 1000
print("total:\ncost = {}\nweight = {}\n".format(cost, weight))

m = box(batt_2p_width, batt_2p_height, batt_2p_depth, center = True)
m = m.up(dropout_m_axle_pos + 20 + side_compartment_height - batt_2p_depth / 2 - common_clearance)
m1 = box(batt_1p_width, batt_1p_depth, batt_1p_height, center = True)
m1 = m1.up(dropout_m_axle_pos + 20 + 20 + 2 + common_clearance + batt_1p_height / 2)
m1 = m1.back(wheel_arch_width/2 + dcdt + common_clearance + batt_1p_depth / 2)
m += m1

print("dmns_shell_mount_cover: {}".format(dmns_shell_mount_cover))
display(m, color = (0, 0, 1, 0.5))

m = box(ctrl_width, ctrl_depth, ctrl_height, center = True)
m = m.up(dropout_m_axle_pos + 20 + 20 + common_clearance + ctrl_height / 2)
m = m.forw(wheel_arch_width/2 + dcdt + common_clearance + batt_1p_depth / 2)
display(m, color = (0, 0.5, 0, 0.5))

show()
