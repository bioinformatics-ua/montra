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
                    self.authors.append( author["ForeName"] + " "+ author["LastName"] ) 
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

    def get_formatted(self):
        new_file = ''
        new_file += ('\t<tr>\n\t\t<td valign="top" class="resourcesICO">')
        new_file +=     ('<a href="%s" target="_blank"><img src="../../image/ico_sitelink.gif" width="24" height="24" /></a></td>\n') % (self.external_url)
        new_file += ('\t\t<td><a href="%s" target="_blank">%s</a><br />\n') % (self.external_url, self.title)
        new_file += ('\t\t%s<br />\n') % (', '.join(self.authors))
        new_file += ('\t\t<em>%s, %s, %s, %s.</em></td>\n') % (self.journal, self.pub_year, self.volume, self.pages)
        new_file += ('\t</tr>\n')
        return new_file