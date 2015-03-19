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
import pickle
import sys
import json

#Local

#DEV
#host1 = "biodatacenter.ieeta.pt"
#port1 = str(9297)


def main(f_id, file_path):

    solr = pysolr.Solr('http://' + settings.SOLR_HOST+ ':'+ settings.SOLR_PORT+settings.SOLR_PATH)
    start=0
    rows=10000
    fl=''

    fingerprint = f_id
    inFile = open(file_path, 'rb')

    jsonData = inFile.readlines()
    jsonData = "".join(jsonData)
    data = json.loads(jsonData)
    jsonData = json.dumps(data)

    query="id:"+fingerprint
    results = solr.search(query,**{
                    'rows': rows,
                    'start': start,
                    'fl': fl
                })

    if len(results) != 1:
    	print "Could not find id"
    	sys.exit(-2)


    for doc in results:
    	doc["Publications_t"] = jsonData

    xml_answer = solr.add(results)
    print(xml_answer)
    solr.optimize()
