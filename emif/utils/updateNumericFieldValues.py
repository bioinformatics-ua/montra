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
import time
from purgeSolr import export_results

solr = pysolr.Solr('http://' + settings.SOLR_HOST+ ':'+ settings.SOLR_PORT+settings.SOLR_PATH)

ticks = time.time()
fileAddr = "/tmp/solr-backup-"+str(ticks)+".pkl"

export_results(solr, fileAddr)

def query(solr, id):
	query="id:"+id
	results = solr.search(query,**{
	                'rows': 10,
	                'start': 0,
	                'fl': ""
	            })

	return results

updateList = [{
        "number_active_patients_jan2012_t": "3.600.000",
        "id": "768185357ce7e4e0aeae6d2e69f6d7e0"
      },
      {
        "number_active_patients_jan2012_t": "1.800.000",
        "id": "2b9291151f7b3f2fd1fed0d876e59b7a"
      },
      {
        "number_active_patients_jan2012_t": "50.000",
        "id": "21d11ac0eb3f0bb30c094fb7caf5e28d"
      },
      {
        "number_active_patients_jan2012_t": "",
        "id": "45b7ccb3aca47bc37f9bd82504f09b3b"
      },
      {
        "number_active_patients_jan2012_t": "900.000",
        "id": "52d4981701f0126d947014244744efea"
      },
      {
        "number_active_patients_jan2012_t": "324.234",
        "id": "66a47f694ffb676bf7676dfde24900e6"
      },
      {
        "number_active_patients_jan2012_t": "",
        "id": "2151825ca52388e960d1ed0728dc38b2"
      },
      {
        "number_active_patients_jan2012_t": "1.800.000",
        "id": "54d8384917b21fb7928ba72a1e72326b"
      },
      {
        "number_active_patients_jan2012_t": "1.000",
        "id": "7b128593480b53409ac83c9582badbb7"
      },
      {
        "number_active_patients_jan2012_t": "150.000",
        "id": "5d8f88d91f1dc3e2806d825f61260b76"
      },
      {
        "number_active_patients_jan2012_t": "5.000.000",
        "id": "cc7f3a8f8af0f6c99f9385c7372c8fe3"
      },
      {
        "number_active_patients_jan2012_t": "500",
        "id": "a201c870db5c30a7371d0c0d4eb11f5f"
      },
      {
        "number_active_patients_jan2012_t": "3.828.859",
        "id": "7a205644571c31bc50965c68d7565622"
      }]

updateDocs = []

for x in updateList:
	print x["id"], x["number_active_patients_jan2012_t"]
	results = query(solr, x["id"])

	for doc in results:
		doc["number_active_patients_jan2012_t"] = x["number_active_patients_jan2012_t"]
		updateDocs.append(doc)

solr.add(updateDocs)
solr.optimize()
sys.exit()







