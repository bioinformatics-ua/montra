


from pprint import pprint
from Bio import Entrez



def fetch_by_pmid(pmid):

	Entrez.email = "you@example.com"
	Entrez.tool = "test-tool"
	 
	#pmid = 23225384
	handle = Entrez.efetch(db='pubmed', id=pmid, retmode='xml')
	#print(handle.read())
	record = Entrez.read(handle)
	 
	#pprint(record[0]['PubmedData'])

	#pprint(record[0]['MedlineCitation']['Article']['ArticleTitle'])
	title = record[0]['MedlineCitation']['Article']['ArticleTitle']
	#pprint(record[0]['MedlineCitation']['Article']['Abstract']['AbstractText'])
	abstract = record[0]['MedlineCitation']['Article']['Abstract']['AbstractText']
	abstract_text = ""
	for a in abstract:
		abstract_text += a
	print abstract_text
	return (title, abstract_text)

#pprint(fetch_by_pmid(23225384))
