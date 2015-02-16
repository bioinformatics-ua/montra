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
from django.conf import settings

import pysolr
import sys
import pickle
import time
from cStringIO import StringIO


solr = pysolr.Solr('http://' + settings.SOLR_HOST+ ':'+ settings.SOLR_PORT+settings.SOLR_PATH)
ticks = time.time()
fileAddr = "/tmp/solr-backup-"+str(ticks)+".pkl"

def export_results(solr, file):
	start=0
	rows=100000
	fl=''

	query="*:*"
	results = solr.search(query,**{
                'rows': rows,
                'start': start,
                'fl': fl
            })
	r_aux = None
	docs = []
	for r in results:
	    docs.append(r)

	output = open(file, 'wb')
	# Pickle dictionary using protocol 0.
	pickle.dump(docs, output)
	output.close()

export_results(solr, fileAddr)

if len(sys.argv) == 2:
	if sys.argv[1] == "all":
		solr.delete(q="*:*")
		solr.optimize()
		sys.exit()

#invalidDatabaseIDS = ["e77d9c5fbf034f4f3fd054a848f119a4", "0d348d887bae9e49c673d25fb204d155", "1dc33e09aca64afadb19c0a8bf57c6cf", "9143206be72362cf61a9c6d5b8d5ffb9"]
invalidDatabaseIDS = ["c4b8a7b97520e645685deea61fc45487",
						"0d4917a4c4e2c93818a9a2a813e24c7e",
						"f623378e2cfb4bdf204977d2ae3632eb",
						"0bac64ad881077730a1598375bdea15a",
						"856f2c968b9fe351d3f78b13d330ce74"
					]
solr.delete(q="-database_name_t:*")
for x in invalidDatabaseIDS:
	solr.delete(q="id:"+x)
solr.optimize()

