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

retList = []
MAX_COUNT = 10

#spamwriter = csv.writer(f0, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

i = 1
outList = []
for name in lines:
	TERM = name
	print('Getting {0} publications containing {1}...'.format(MAX_COUNT, TERM))
	Entrez.email = 'A.N.Other@example.com'
	h = Entrez.esearch(db='pubmed', retmax=MAX_COUNT, field="title", term=TERM)
	result = Entrez.read(h)
	print('Total number of publications containing {0}: {1}'.format(TERM, result['Count']))
	ids = {}
	ids["count"] = len(result['IdList'])
	ids["list"] = result['IdList']
	ids["title"] = i
	i=i+1

	outList.append(ids)
    
st = json.dumps(outList, sort_keys=True, indent=4, separators=(',', ': '))
print st

f0.write(st)
f0.close()

print "QUITTING"