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
from django.http import HttpResponse, HttpResponseRedirect

from questionnaire.models import *
from django.shortcuts import render_to_response, get_object_or_404
import sys

from searchengine.models import *

from django.conf import settings

import pysolr

solr = pysolr.Solr('http://' + settings.SOLR_HOST+ ':'+ settings.SOLR_PORT+settings.SOLR_PATH)
start=0
rows=100
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
    #print r
    to_append = ""
    import pdb
    #pdb.set_trace()
    if (r.keys()==None):
        continue
    for k in r.keys():
        print k
        #print r[k]
        try:
            if 'yes' in r[k]:
                slugs = Slugs.objects.filter(slug1=k[:-2])
                to_append += slugs[0].question.text
        except Exception, e:
            print e
            pass
    print to_append
    if len(to_append):
        r['text_t'] += ' '+to_append
        del r['_version_']
        docs.append(r)
        solr.delete(r['id'])
        solr.optimize()
        xml_answer = solr.add([r])
        solr.optimize()


