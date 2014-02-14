from Bio import Entrez
import json

class PubMedObject:
    #Objects
    
    #fields
    journal = ''
    authors = []
    title = ''
    pages = ''
    pub_year = ''
    volume = ''
    pubmed_url = ''

    def __init__(self, pmid):
        self.pmid = pmid
        self.authors = []

        Entrez.email = "tmgodinho@ua.pt"
        Entrez.tool = "test-tool"
     
    #call this after downloading the object
    def fetch_info(self):
        handle = Entrez.efetch(db='pubmed', id=self.pmid, retmode='xml')
        record = Entrez.read(handle)

        if len(record)>0:
            try:
                self.pubmed_url = "http://www.ncbi.nlm.nih.gov/pubmed/" + record[0]["MedlineCitation"]["PMID"]
            except Exception, e:
                pass

            try:
                self.title = record[0]["MedlineCitation"]["Article"]["ArticleTitle"]
            except Exception, e:
                pass

            try:
                self.journal = record[0]["MedlineCitation"]["Article"]["Journal"]["Title"]
            except Exception, e:
                pass

            try:
                self.pub_year = record[0]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]["Year"]
            except Exception, e:
                pass

            try:
                self.volume = record[0]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["Volume"] 
            except Exception, e:
                pass

            try:
                self.pages = record[0]["MedlineCitation"]["Article"]["Pagination"]["MedlinePgn"]
            except Exception, e:
                pass

            try:
                temp_authors = record[0]["MedlineCitation"]["Article"]["AuthorList"]

                for author in temp_authors:
                    self.authors.append( author["LastName"] +" " +author["Initials"]) 
            except Exception, e:
                pass
                
            # print "Title: " + self.title
            # print "Authors: %s" % ', '.join(self.authors)
            # print "Journal: " + self.journal
            # print "Pub_year: " + self.pub_year
            # print "Volume: " + self.volume
            # print "Pages: " + self.pages
            # print "done"

            return 0
        return None