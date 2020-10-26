#!/usr/bin/env python3
#coding: utf-8
from zencad import *
from holes import *

common_clearance = 5

gap_dt = 0.2
#gap_dt = 0

#bearing_width = { # ГОСТ 12876-67
#	10: 22
#}

def gap(x, k=1):
	return x + gap_dt * k
