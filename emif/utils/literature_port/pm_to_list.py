#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2014 Universidade de Aveiro, DETI/IEETA, Bioinformatics Group - http://bioinformatics.ua.pt/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# numpy and biopython are required -- pip install numpy biopython

from Bio import Entrez
from Bio import Medline
import json
import csv
import sys
import json

print sys.argv

inFile = "/tmp/journal.txt"
outFile = "/tmp/ids.txt"

if len(sys.argv) > 1:
	if sys.argv[1]:
		inFile = sys.argv[1]
	if sys.argv[2]:
		outFile = sys.argv[2]

f = open(inFile, "r")
lines = f.readlines()
f.close()

f0 = open(outFile, 'wb')

outList = []
for pmid in lines:
	doc = {}
	doc["count"] = 1
	doc["list"] = [pmid.strip()]

	outList.append(doc)

st = json.dumps(outList, sort_keys=True, indent=4, separators=(',', ': '))
print st

f0.write(st)
f0.close()

print "QUITTING"
