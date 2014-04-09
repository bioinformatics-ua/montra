import pysolr
import sys
import pickle
import time
from cStringIO import StringIO

host1 = "localhost"
port1 = str(8983)

solr = pysolr.Solr('http://' +host1+ ':'+ port1+'/solr')
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
		sys.exit()

invalidDatabaseIDS = ["e77d9c5fbf034f4f3fd054a848f119a4", "0d348d887bae9e49c673d25fb204d155", "1dc33e09aca64afadb19c0a8bf57c6cf", "9143206be72362cf61a9c6d5b8d5ffb9"] 
solr.delete(q="-database_name_t:*")
for x in invalidDatabaseIDS:
	solr.delete(q="id:"+x)
solr.optimize()

