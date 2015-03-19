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


field1 = 'institution_name_t'
field2 = 'Contact_organisation_t'

databases_problem_swap = ['IPCI', 'THIN', 'AUH', 'ARS', 'SCTS', 'SDR', 'EGCUT', 'PEDIANET', 'GePaRD', 'MAAS']
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
    to_swap = False
    for k in r.keys():
        #print k
        #print r[k]
        #if k=='database_name_t':
            #print 'win'
            #print str(r[k])
            #print databases_problem_swap
            #if str(r[k]) in databases_problem_swap:
                #print 'big win'
        if k=='database_name_t' and r[k] in databases_problem_swap:
            try:
                Contact_organisation_t = r['Contact_organisation_t']
                r['Contact_organisation_t'] = r['institution_name_t']
                r['institution_name_t'] = Contact_organisation_t
                print "here"
                i = databases_problem_swap.index(str(r['database_name_t']))
                print i
                del databases_problem_swap[i]
                to_swap = True
            except :
                pass
                #print 'error in ' + str(r[k])
        else:
            #print ' problem with ' + r['id']
            pass

    if to_swap:
        print "SWAPING "
        print databases_problem_swap
        del r['_version_']
        solr.delete(r['id'])
        solr.optimize()
        xml_answer = solr.add([r])
        solr.optimize()

    else:
        pass
        #print "problem swap"
        #print databases_problem_swap
print 'done'
print databases_problem_swap
#from utils import rename_slugs_legacy
