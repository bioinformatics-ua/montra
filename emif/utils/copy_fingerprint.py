import pysolr

host1 = "localhost"
port1 = str(8983)


host2 = "localhost"
port2 = str(8080)
solr = pysolr.Solr('http://' +host1+ ':'+ port1+'/solr')
start=0
rows=100
fl=''

query="id:21d11ac0eb3f0bb30c094fb7caf5e28d"
results = solr.search(query,**{
                'rows': rows,
                'start': start,
                'fl': fl
            })
r_aux = None
doc = {}
for r in results:
	r_aux = r
	for k, v in r:
		doc[k] = v
	break
print doc
#print r_aux


#solr2 = pysolr.Solr('http://' +host2+ ':'+ port2+'/solr')
#xml_answer = solr2.add([r_aux])
#print(xml_answer)
#solr2.optimize()