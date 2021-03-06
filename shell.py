#!/usr/bin/env python3
#coding: utf-8
from zencad import *
# для расчета корпуса возмем старые значения
import mcm5dropout

common_clearance = 5
batt_1p_width = 203
batt_1p_height = 140
batt_1p_depth = 26
batt_2p_width = 203
batt_2p_height = 80
batt_2p_depth = 75
ctrl_width = 89
ctrl_height = 170
ctrl_depth = 26
# для расчета корпуса возмем старые значения
tire_diameter_inch = 14
tire_thickness_inch = 2.125

# distance between dropauts:
wheel_arch_width = 92

#cover_thickness = 2
cover_thickness = 1.5

#side_compartment_width = 250
side_compartment_width = 356
side_compartment_inner_width = side_compartment_width - 20*2
side_compartment_height = tire_diameter_inch*12.7 - mcm5dropout.dropout_m_axle_pos + 20 + batt_2p_depth + 2 * common_clearance + 20
side_compartment_inner_depth = 62.5
side_compartment_depth = 66.65
side_compartment_bottom_thickness = side_compartment_top_thickness = 2.5

top_width = side_compartment_width-5.5*2
top_height = side_compartment_depth-5.5-23.4786
top_depth = 4

h_rib = tire_diameter_inch*12.7 + 10 + 20 - mcm5dropout.dropout_m_axle_pos

# в посчитанное впихнём новое колесо:
tire_diameter_inch = 16
tire_thickness_inch = 3