

from django.http import HttpResponse, HttpResponseRedirect

from questionnaire.models import *
from django.shortcuts import render_to_response, get_object_or_404
import sys

from searchengine.models import *


import pysolr

host1 = "localhost"
port1 = str(8983)

solr = pysolr.Solr('http://' +host1+ ':'+ port1+'/solr')
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
        #print k
        #print r[k]
        try:
            if 'yes' in r[k]:
                slugs = Slugs.objects.filter(slug1=k)
                to_append += slugs[0].question.text

        except: 
            pass
    print to_append
    r['text_t'] += ' '+to_append 
    del r['_version_']
    docs.append(r)
    solr.delete(r['id'])
    solr.optimize()
    xml_answer = solr.add([r])
    solr.optimize()


