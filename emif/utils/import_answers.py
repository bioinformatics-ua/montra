import pysolr

host1 = "localhost"
port1 = str(8983)


solr = pysolr.Solr('http://' +host1+ ':'+ port1+'/solr')
start=0
rows=100
fl=''

import pickle

pkl_file = open('fingerprints.pkl', 'rb')

docs = pickle.load(pkl_file)


pkl_file.close()


xml_answer = solr.add(docs)
print(xml_answer)
solr.optimize()