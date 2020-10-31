#!/usr/bin/python3
#
#

import sys
import re

# usage
if len(sys.argv) < 2:
	print("")
	print(f"USAGE: {sys.argv[0]} COORDS_FILE [WIDTH] [DEPTH]")
	print("")
	print("    COORDS_FILE - path to the profile coordinate file")
	print("    WIDTH of the profile in mm")
	print("    DEPTH thickness in %")
	print("")
	exit(1)

# args
filename = sys.argv[1]
width = 1.0
if len(sys.argv) > 2:
	width = float(sys.argv[2])
depth = None
if len(sys.argv) > 3:
	depth = float(sys.argv[3])

# read file
f = open(filename, "rb")
data = f.read()

# parse data
coords = []
min_y = 1.0
max_y = 0.0
for line in data.split(b"\n"):
	matches = re.match(b"^\s*(-*\d+.\d+)\s*(-*\d+.\d+)\s*$", line)
	if matches:
		x = float(matches[1])
		y = float(matches[2])
		coords.append((x, y))
		if y > max_y:
			max_y = y
		if y < min_y:
			min_y = y

# calc thickness
depth_org = (max_y - min_y) * 100.0

# dxf-header
print("0\nSECTION\n2\nENTITIES")

# dxf-lines
last_x = None
last_y = None
for coord in coords:
	x = coord[0] * width
	y = coord[1] * width
	if depth:
		y = y / depth_org * depth
	if last_x != None:
		print(f"0\nLINE\n8\n0\n10\n{last_x}\n20\n{last_y}\n11\n{x}\n21\n{y}")
	last_x = x
	last_y = y

# dxf-footer
print("0\nENDSEC\n0\nEOF")

