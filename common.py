#!/usr/bin/env python3
#coding: utf-8
from zencad import *
import metric
from enum import Enum

common_clearance = 5
batt_1p_width = 140
batt_1p_height = 203
batt_1p_depth = 26
batt_2p_width = 140
batt_2p_height = 80
batt_2p_depth = 75
ctrl_width = 89
ctrl_height = 170
ctrl_depth = 26
tire_diameter_inch = 14
tire_thickness_inch = 2.125
# distance between dropauts:
wheel_arch_width = 93

dropout_width = 44.8
dropout_height = 113.6
dropout_depth = 21.7
dropout_m_axle_pos = 24.5
dropout_p_axle_pos = 40.2
dropout_sole_size = 51.8
dropout_sole_pos = 88

cover_thickness = 2

side_compartment_width = 250#batt_1p_width + common_clearance*2 + 20*2 + 2*2
side_compartment_inner_width = side_compartment_width - 20*2
#side_compartment_height = 250#tire_diameter_inch*12.7 - dropout_m_axle_pos + 20 + 20 + batt_2p_height + 2 * common_clearance + 2*2
side_compartment_height = tire_diameter_inch*12.7 - dropout_m_axle_pos + 20 + batt_2p_depth + 2 * common_clearance
side_compartment_inner_depth = 62.5
side_compartment_depth = 66.65
side_compartment_bottom_thickness = side_compartment_top_thickness = 2.5

cable_protection_width = dropout_width
cable_protection_height = 43+5*2
cable_protection_depth = 19-1+4

top_width = side_compartment_width-5.5*2
top_height = side_compartment_depth-5.5-23.4786
top_depth = 4

class HoleType(Enum):
	tap = 1
	threaded = 2
	fasteners = 3

hole_d = {
    3:  3.2,
	5:	5.3,
	10:	10.5,
	20: 21,
	24:	25
}

hole_tap_d = {
	5:	4.2
}

bearing_width = { # ГОСТ 12876-67
	10: 22
}

nut_m5_len = dropout_depth
nut_m5 = metric.metric_nut(5, 0.8, nut_m5_len, False).rotateX(deg(90)).forw(nut_m5_len/2)

gap_dt = 0.2
#gap_dt = 0

def gap(x, k=1):
	return x + gap_dt * k
