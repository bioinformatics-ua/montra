import pysolr
import pickle
import sys
import json

#Local
host1 = "localhost"
port1 = str(8983)

#DEV
#host1 = "biodatacenter.ieeta.pt"
#port1 = str(9297)


def main(f_id, file_path):

    solr = pysolr.Solr('http://' +host1+ ':'+ port1+'/solr')
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
