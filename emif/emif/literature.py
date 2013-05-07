


from pprint import pprint
from Bio import Entrez
 
Entrez.email = "you@example.com"
Entrez.tool = "test-tool"
 
pmid = 23225384
handle = Entrez.efetch(db='pubmed', id=pmid, retmode='xml')
#print(handle.read())
record = Entrez.read(handle)
 
pprint(record[0]['PubmedData'])

pprint(record[0]['MedlineCitation']['Article']['ArticleTitle'])
pprint(record[0]['MedlineCitation']['Article']['Abstract'])
