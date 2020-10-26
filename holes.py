#!/usr/bin/env python3
#coding: utf-8
from enum import Enum

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
