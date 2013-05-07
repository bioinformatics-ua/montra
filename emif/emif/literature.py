


from Bio import EUtils
from Bio.EUtils import DBIdsClient

doi = "10.1016/j.jmb.2007.02.065"

client = DBIdsClient.DBIdsClient()
result = client.search(doi + "[aid]", retmax = 1)
summary = result[0].summary()

# For a PMID, there's a more direct method:
from Bio import EUtils
from Bio.EUtils import DBIdsClient

PMID = "17238260"
result = DBIdsClient.from_dbids(EUtils.DBIds("pubmed", PMID))
summary = result[0].summary()

"""
>>> from Bio import Entrez
>>> handle = Entrez.esearch(db="nuccore", term="complete", field="title", rettype='xml')
>>> print Entrez.read(handle)[u'QueryTranslation']
complete[Title]"""