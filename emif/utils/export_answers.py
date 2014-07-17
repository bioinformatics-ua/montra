
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
    
    docs.append(r)

import pickle
from cStringIO import StringIO

output = open('/tmp/fingerprints.pkl', 'wb')

# Pickle dictionary using protocol 0.
pickle.dump(docs, output)


output.close()