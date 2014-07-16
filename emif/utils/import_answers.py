from django.conf import settings

import pysolr

solr = pysolr.Solr('http://' + settings.SOLR_HOST+ ':'+ settings.SOLR_PORT+settings.SOLR_PATH)
start=0
rows=100
fl=''

import pickle

pkl_file = open('fingerprints.pkl', 'rb')

docs = pickle.load(pkl_file)


pkl_file.close()

for d in docs:
    del d['_version_']

xml_answer = solr.add(docs)
print(xml_answer)
solr.optimize()
