

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