#!/usr/bin/env python3
#coding: utf-8

import sys
from math import sqrt, tan, ceil
import metric
from common import *
from shell import *
from mcm5v2dropout import *
#from mcm5dropout import *
import usb

#alp2020l = from_brep('./brep/alp2020l.brep')
alp2020l = from_brep('./brep/alp2020almk.brep').left(47.4).back(75.2)
#alp2040l = from_brep('./brep/alp2040l.brep').left(10)
alp2040l = from_brep('./brep/alp2040almk.brep').back(81.55).left(37.25)
#alp2040l = from_brep('./brep/alp2040almk.brep').back(81.5404).left(37.25)
alp4040con = from_brep('./brep/alp4040con.brep').scaleZ(0.1)
con2020d = from_brep('./brep/con2020d.brep')
con2020 = from_brep('./brep/con2020.brep').left(10).down(6.25).rotateY(deg(-90)).rotateX(deg(180))
con2040 = from_brep('./brep/con2040d.brep').right(38.1/2).back(38.1/2).down(17.4/2)#.rotateZ(deg(-90))
con2040s = from_brep('./brep/con2040s.brep').down(18/2 - 2).left(38.5/2).back(38.5/2).rotateX(deg(90)).rotateY(deg(180))
con4040s = from_brep('./brep/con4040s.brep').down((38.5-3.7)/2).rotateX(deg(90)).left(38.5/2).down(38.5/2)
gx16 = from_brep('./brep/GX16-4.brep').rotateX(deg(90)).rotateZ(deg(90))
power_button = from_brep('./brep/PV2F640xx.brep').rotateX(deg(90)).down(12)
handle = from_brep('./brep/handle108mm.brep').rotateX(deg(90))

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

h_rib += dropout_m_axle_pos
h_rib2 = 10+dropout_m_axle_pos + side_compartment_height
h_icl = h_rib - dropout_m_axle_pos + 10 - 20
h_icr = 20 + common_clearance + ctrl_height
h_icr += 8 - (h_icr-h_icl-18.3)*2 # 8 - размер опорной поверхности под М3.

dmns_shell_mount_cover = (dropout_width + 20*2, cover_thickness, len2020v + 20)

def display_shell(alpha):
    mv = get_alp2040(side_compartment_height - 20*2 - 40).rotateZ(deg(90))
    mh = get_alp2040(side_compartment_width - 20).rotateZ(deg(90)).rotateY(deg(90)).down(side_compartment_height/2 - 10).right(10)
    #m = mv.left(side_compartment_width/2 - 10).down(40/2)
    #m = mv.right(side_compartment_width/2 - 10).down(40/2)
    m = mv.left(side_compartment_width/2 - 10 - 20).down(40/2)
    m += mv.left(side_compartment_width/2 - 10).down(40/2).mirrorYZ()
    #m += m.mirrorYZ()
    m += mh
    
    #m += get_alp2040(side_compartment_width).rotateY(deg(90)).rotateX(deg(90)).up(side_compartment_height/2 - 50)
    #m += get_alp2040(side_compartment_width).rotateY(deg(90)).forw(10).up(side_compartment_height/2 - 20)

    m += get_alp2040(side_compartment_width - 20).rotateY(deg(90)).rotateX(deg(90)).up(side_compartment_height/2 - 50).right(10)
    #t = get_alp2040(side_compartment_width).rotateY(deg(90))
    #t -= box(20, center=True).up(10).left(side_compartment_width/2 - 10)
    #m += t.forw(10).up(side_compartment_height/2 - 20)
    t = get_alp2020(side_compartment_width).rotateY(deg(90))
    m += t.forw(10).up(side_compartment_height/2 - 30)
    t = get_alp2020(side_compartment_width - 20).rotateY(deg(90))
    m += t.forw(10).up(side_compartment_height/2 - 10).right(10)

    #m += get_alp2040(side_compartment_height - 40).rotateX(deg(90)).left(side_compartment_width/2 - 50).down(20)
    #m += get_alp2040(side_compartment_height - 40).forw(10).left(side_compartment_width/2 - 20).down(20)
    m += get_alp2020(side_compartment_height - 40).forw(10).left(side_compartment_width/2 - 10).down(20)
    
    m = m.up(side_compartment_height/2 + dropout_m_axle_pos + 20)
    m = m.back(wheel_arch_width/2 + 20 + ddt)
    m += m.mirrorXZ()

    # нижние и верхние поперечные балки верхнего отсека:
    htop = len2020h_rib
    rib = get_alp2020(htop).rotateX(deg(90)).up(h_rib)
    rib = rib.left(side_compartment_width/2 - 10)
    rib += rib.mirrorYZ()

    rib2t = get_alp2040(len2020h_rib2).rotateX(deg(90)).rotateY(deg(90)).up(h_rib2-10)
    rib2t = rib2t.right(side_compartment_width/2 - 10)
    
    rib2h = get_alp4040con(len2020h_rib2).rotateX(deg(90)).mirrorYZ().up(h_rib2 - 20)
    rib2h = rib2h.left(side_compartment_width/2 - 10-20)

    m += rib + rib2h + rib2t

    guide = get_alp2020(len2020_guid).rotateY(deg(90))
    guide = guide.up(h_rib)
    guide = guide.back(wheel_arch_width/2 - 10 + dcdt)
    guide += guide.mirrorXZ()
    m += guide

    # уголки усиливающие нижнюю часть верхнего отсека:
    con = con2020d.rotateY(deg(90)).up(h_rib).left(side_compartment_inner_width/2 - 18/2).back(wheel_arch_width/2 - 20 - 18/2 + dcdt)
    con += con.mirrorXZ()
    con += con.mirrorYZ()
    m += con
    
    # уголки усиливающие торцевые части верхнего отсека:
    #con = con2020.rotateX(deg(90)).up(h_rib2-10-20).left(side_compartment_width/2 - 20/2).back(wheel_arch_width/2 - 20/2 + ddt)
    con = con2040.rotateY(deg(90)).up(h_rib2-10-40).left(side_compartment_width/2 - 20/2).back(wheel_arch_width/2 - 40/2 + ddt)
    con += con.mirrorXZ()
    con += con.mirrorYZ()
    m += con

    # внутренняя верхняя крышка
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
    #to_brep(inner_cover, "vector/1x_ict.brep")
    inner_cover = inner_cover.up(h_rib - 10 - cover_thickness/2)
    m += inner_cover
    
    # внутренние боковые крышки
    icl = box(side_compartment_width, h_icl, cover_thickness, center = True).rotateX(deg(90))
    hole = cylinder(hole_d[5]/2, cover_thickness, True).rotateX(deg(90))
    holes = hole.up(h_icl/2 - 10).left(side_compartment_width/2 - 10)
    holes += holes.mirrorYZ()
    holes += holes.down(20 + cover_thickness)
    holes += holes.mirrorXY()
    holes += holes + hole.down(h_icl/2 - 10)
    holes += hole.left(side_compartment_width/2 - 10) + hole.right(side_compartment_width/2 - 10)
    t = hole.up(h_icl/2 - 10)
    holes_l = holes + t
    t = t.left(ctrl_width/2 + gap(11.8/2)) # 11.8 - самый большой диаметр шляпки винта М5, что удалось на вскидку найти...
    holes_r = holes + t + t.mirrorYZ()

    icl -= holes_l
    #to_brep(icl.rotateX(deg(90)), "vector/1x_icl.brep")

    icr = box(side_compartment_width, h_icr, cover_thickness, center = True).rotateX(deg(90))
    # отверстия крепления контроллера
    hole_m3 = cylinder(hole_d[3]/2, cover_thickness, True).rotateX(deg(90))
    holes_ctrl = hole_m3.up(h_icr/2 - 18.3)
    holes_ctrl += hole_m3.up(h_icr/2 - 18.3 - 140.3)
    holes_ctrl = holes_ctrl.left(78.7 / 2)
    holes_ctrl += holes_ctrl.mirrorYZ()
    icr -= holes_ctrl
    icr = icr.up((h_icr - h_icl)/2)
    icr -= holes_r
    #to_brep(icr.rotateX(deg(-90)), "vector/1x_icr.brep")
    icl = icl.back(wheel_arch_width/2 - cover_thickness/2 + ddt)
    icr = icr.forw(wheel_arch_width/2 - cover_thickness/2 + ddt)
    icl = icl.up(h_icl/2 + dropout_m_axle_pos + 20)
    icr = icr.up(h_icl/2 + dropout_m_axle_pos + 20)
    inner_cover = icl + icr
    m += inner_cover
    
    # внешние боковые крышки
    '''
    scuh = side_compartment_height - 40 # useful height
    outer_cover = box(side_compartment_width, scuh, cover_thickness, center = True).rotateX(deg(90))
    hole = hole.rotateX(deg(90))
    #hup = hole.up(scuh/2 - 10)
    t = hole.left(side_compartment_width/2 - 10)
    t += t.mirrorYZ()
    holes = t.up(scuh/2 - 10)
    holes += t.up(scuh/2 - 30)
    #holes += hup
    holes += holes.mirrorXY()
    #holes += t
    outer_cover -= holes
    #to_brep(outer_cover.rotateX(deg(90)), "vector/2x_ocs.brep")

    outer_cover = outer_cover.up(scuh/2 + dropout_m_axle_pos + 20)
    outer_cover = outer_cover.back(wheel_arch_width/2 + 40 + cover_thickness/2 + ddt)
    outer_cover += outer_cover.mirrorXZ()
    m += outer_cover # боковые крышки
    '''
    # внешняя верхняя крышка
    hotc = htop + 40*2 + ddt*2
    oc_width = side_compartment_width - 20
    outer_cover = box(oc_width, hotc, cover_thickness, center = True)
    hole = cylinder(hole_d[5]/2, cover_thickness, True)
    holes = hole.forw(hotc/2 - 10).left(oc_width/2 - 10)
    holes += holes.mirrorYZ()
    holes += hole.forw(hotc/2 - 10)
    holes += holes.mirrorXZ()
    holes2 = hole.forw(hotc/2-10-20).left(oc_width/2 - 10)
    holes2 += holes2.mirrorYZ()
    holes2 += holes2.mirrorXZ()
    holes += holes2
    holes2 = hole.left(oc_width/2 - 10)
    holes2 += holes2.mirrorYZ()
    holes += holes2
    hole_btn = cylinder(16/2, cover_thickness, True)
    
    dtc = 32.2 / 2 + common_clearance#9/2 + 18/2
    holes += hole_btn.forw(10 + dtc).left(oc_width/2 - 40 - dtc) + hole_btn.forw(10 + dtc).right(oc_width/2 - 20 - dtc)
    hole_gx16 = hole_btn
    cut = box(16, (16-14.6)/2, cover_thickness, center=True).back(16/2 - (16-14.6)/4)
    cut += cut.mirrorXZ()
    hole_gx16 -= cut
    holes += hole_gx16.back(10 + dtc).left(oc_width/2 - 40 - dtc)
    
    hole_usb = cylinder(25.2/2, cover_thickness, True)
    cut = box(25.2, 25.2-24.5, cover_thickness, center=True).back(25.2/2 - (25.2-24.5)/2)
    cut = cut.mirrorXZ()
    hole_usb -= cut
    holes += hole_usb.back(10 + dtc).right(oc_width/2 - 20 - dtc)#.back(10 + 32.2/4 + 32.2/2).right(side_compartment_width/2 - 20 - 32.2/4 - 32.2/2)
    outer_cover -= holes
    #to_brep(outer_cover, "vector/1x_oct.brep")
    outer_cover += power_button.forw(10 + dtc).left(oc_width/2 - 40 - dtc) + power_button.forw(10 + dtc).right(oc_width/2 - 20 - dtc)
    outer_cover += gx16.back(10 + dtc).left(oc_width/2 - 40 - dtc)
    outer_cover += usb.get_usb().back(10 + dtc).right(oc_width/2 - 20 - dtc)
    outer_cover = outer_cover.up(dropout_m_axle_pos + 20 + side_compartment_height + cover_thickness/2).right(10)
    m += outer_cover # внешняя верхняя крышка
    
    front_width = wheel_arch_width + 2*ddt + 2*40 + 2*cover_thickness
    front_height = batt_2p_depth + 2 * common_clearance + 20 + 2*cover_thickness + 20
    # торцевые верхние крышки
    butt_cover = box(front_width, cover_thickness, front_height, center=True)
    #
    cut_width = 20 + cover_thickness
    cut = box(cut_width, cover_thickness, cover_thickness + 40, center=True).up(front_height/2 - cover_thickness/2 - 40/2)
    cut = cut.left(front_width/2 - cut_width/2)
    cut += cut.mirrorYZ()
    butt_cover -= cut
    
    cut_width = 20 + cover_thickness
    cut_height = front_height - (cover_thickness + 40) - 40
    cut = box(cut_width, cover_thickness, cut_height, center=True).up(front_height/2 - 80 - cut_height/2 - cover_thickness)
    cut = cut.left(front_width/2 - cut_width/2)
    cut += cut.mirrorYZ()
    butt_cover -= cut
    #
    hole = hole.rotateX(deg(90))
    holes = hole.up(front_height/2 - cover_thickness - 10).left(front_width/2 - cover_thickness - 30)
    holes += hole.up(front_height/2 - cover_thickness - 50).left(front_width/2 - cover_thickness - 10)
    holes += hole.up(front_height/2 - cover_thickness - 10).left(front_width/2 - cover_thickness - 50)
    holes += hole.up(front_height/2 - cover_thickness - 70).left(front_width/2 - cover_thickness - 10)
    holes += hole.down(front_height/2 - cover_thickness - 10).left(front_width/2 - cover_thickness - 30)
    holes += hole.down(front_height/2 - cover_thickness - 10).left(front_width/2 - cover_thickness*2 - 50)
    holes += hole.down(front_height/2 - cover_thickness - 10).left(front_width/2 - cover_thickness*2 - 70)
    holes += holes.mirrorYZ()
    butt_cover -= holes
    #to_brep(butt_cover.rotateX(deg(-90)), "vector/2x_bct.brep")

    butt_cover = butt_cover.rotateZ(deg(90))
    butt_cover = butt_cover.left(side_compartment_width/2 + cover_thickness/2)
    butt_cover = butt_cover.up(h_rib - 10 + front_height/2 - cover_thickness)
    butt_cover += butt_cover.mirrorYZ()
    #m += butt_cover # торцевые верхние крышки
    
    han = get_alp2020(oc_width - 40).rotateY(deg(90)).up(dropout_m_axle_pos + 20 + side_compartment_height + cover_thickness + 20/2)
    con = con2020.rotateX(deg(180)).rotateZ(deg(90)).up(dropout_m_axle_pos + 20 + side_compartment_height + cover_thickness + 20/2).left((oc_width)/2 - 20)
    con += con.mirrorYZ()
    han += con
    
    # торцевые нижние накладки
    '''
    bb_width = 40 + 2*cover_thickness
    bb_height = 40;
    butt_cover = box(bb_width, cover_thickness, bb_height, center=True)
    holes = hole.up(bb_height/2 - 10).left(bb_width/2 - cover_thickness - 10)
    holes += holes.mirrorYZ()
    holes += holes.mirrorXY()
    butt_cover -= holes
    #to_brep(butt_cover.rotateX(deg(-90)), "vector/4x_bcb.brep")
    butt_cover = butt_cover.rotateZ(deg(90))
    butt_cover = butt_cover.left(side_compartment_width/2 + cover_thickness/2)
    butt_cover = butt_cover.up(dropout_m_axle_pos + 20 + bb_height/2)
    butt_cover = butt_cover.back(wheel_arch_width/2 + 20 + ddt)
    butt_cover += butt_cover.mirrorXZ()
    butt_cover += butt_cover.mirrorYZ()
    m += butt_cover # торцевые нижние накладки
    '''
    
    han += handle.up(dropout_m_axle_pos+20+side_compartment_height+cover_thickness+20)
    m += han.right(10)
    
    display(m, color=(0.5, 0.5, 0.5, alpha))

def get_alp2020(len):
    return alp2020l.scaleZ(len / 100).up(len / 2)

def get_alp2040(len):
    return alp2040l.scaleZ(len / 100).up(len / 2)

def get_alp4040con(len):
    return alp4040con.scaleZ(len / 100).up(len / 2)
  
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
    cov -= get_dropout_holes(HoleType.fasteners).up(gap_dropout_height/2 - top_padding_holes - (sole_thick/2+4/2)).back(dt_holes_back)
    cov -= cylinder(gap(wheel_axle_big_d/2), 4, True).rotateX(deg(90)).back(dt_holes_back).up((gap_dropout_height-sole_thick-4)/2-dropout_m_axle_pos)

    #to_brep(cov.rotateX(deg(-90)), "vector/2x_smc.brep")

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

    dropout = get_dropout().down(dropout_height/2 - dropout_m_axle_pos)
    display(\
        dropout.back((wheel_arch_width+dropout_depth)/2)+\
        dropout.mirrorXZ().forw((wheel_arch_width+dropout_depth)/2),\
        color=(0.4, 0.4, 0.4, 0.0))


#display(handle.rotateX(deg(90)))
#show()
#sys.exit(0)

#display_wheel()
#display_shell_mounts()
##display_shell(0.5)
display_shell(0)

'''
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
'''
'''
m = box(batt_2p_width, batt_2p_height, batt_2p_depth, center = True)
m = m.up(mcm5dropout.dropout_m_axle_pos + 20 + side_compartment_height - batt_2p_depth / 2 - common_clearance)
m1 = box(batt_1p_width, batt_1p_depth, batt_1p_height, center = True)
m1 = m1.up(mcm5dropout.dropout_m_axle_pos + 20 + 20 + 2 + common_clearance + batt_1p_height / 2)
m1 = m1.back(wheel_arch_width/2 + dcdt + common_clearance + batt_1p_depth / 2)
m += m1
'''

#print("dmns_shell_mount_cover: {}".format(dmns_shell_mount_cover))
#display(m, color = (0, 0, 1, 0.5))

#m = box(ctrl_width, ctrl_depth, ctrl_height, center = True)
#m = m.up(dropout_m_axle_pos + 20 + h_icr - ctrl_height / 2)
#m = m.forw(wheel_arch_width/2 + dcdt + common_clearance + batt_1p_depth / 2)

# скругляющие силиконовые накладки:
'''
pw = side_compartment_width+cover_thickness*2
ph = 40+cover_thickness
pd = 20+cover_thickness
m = box(pw, pd, ph, center=True).fillet(pd-0.1, [(0, -pd/2, ph/2), (-pw/2, 0, 0), (-pw/2, 0, ph/2)]).back(wheel_arch_width/2 + 20 + ddt + pd/2)
#m = m.up(mcm5dropout.dropout_m_axle_pos + 20 + side_compartment_height + cover_thickness - ph/2)
m = m.up(dropout_m_axle_pos + 20 + side_compartment_height + cover_thickness - ph/2)
m += m.mirrorXZ()
display(m, color = (0, 0.2, 0, 0))

pw = side_compartment_height-40
ph = 20+cover_thickness
pd = 20+cover_thickness
m = box(pw, pd, ph, center=True).fillet(pd-0.1, [(0, -pd/2, ph/2)]).rotateY(deg(-90)).back(wheel_arch_width/2 + 20 + ddt + pd/2)
m = m.up(dropout_m_axle_pos + 20 + side_compartment_height / 2 - 20)
m = m.left(side_compartment_width/2 - 10+cover_thickness/2)
m += m.mirrorXZ()
display(m, color = (0, 0.2, 0, 0))
'''
show()
