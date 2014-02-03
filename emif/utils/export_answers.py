


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
    
    docs.append(r)

import pickle
from cStringIO import StringIO

output = open('/tmp/fingerprints.pkl', 'wb')

# Pickle dictionary using protocol 0.
pickle.dump(docs, output)


output.close()