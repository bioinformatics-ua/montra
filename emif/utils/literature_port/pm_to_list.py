#!/usr/bin/env python
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