import urllib
import urllib2
import shutil
import urlparse
import os
import sys
import re
import string
import unicodedata
import traceback

class PubMedObject:
    doi = ''
    pmid = False
    pubmed_url = ''
    external_url = ''
    local_file = ''
    html_file = ''

    journal = ''
    authors = []
    title = ''
    pages = ''
    pub_year = ''
    volume = ''

    def __init__(self, doi_or_pmid):
        doi_or_pmid = doi_or_pmid.strip()
        self.pmid = (doi_or_pmid[:4] == 'pmid')

        #initialize URL for downloading
        if self.pmid:
            self.doi = doi_or_pmid[5:]
            self.pubmed_url = 'http://www.ncbi.nlm.nih.gov/pubmed/' + self.doi
            self.external_url = 'http://www.ncbi.nlm.nih.gov/pubmed/' + self.doi
        else:
            self.doi = doi_or_pmid
            self.pubmed_url = 'http://www.ncbi.nlm.nih.gov/pubmed/?term=' + self.doi
            self.external_url = 'http://dx.doi.org/' + self.doi

        #initialize name of local file
        self.local_file = "/tmp" + getproperfilename(urllib.quote_plus(self.doi)) + '.html'

        #delete the local file if it already exists
        if os.path.isfile(self.local_file):
            os.remove(self.local_file)

    #call this before using anything in the object
    def download(self):
        response = urllib2.urlopen(urllib2.Request(self.pubmed_url))
        try:
            with open(self.local_file, 'wb') as f:
                self.html_file = response.read()
                f.write(self.html_file)
                f.close()
                #shutil.copyfileobj(response, f)

            #self.html_file = open(self.local_file,'r').read()
        except:
            print "Tried to download " + self.pubmed_url + ", but got this error."
            print sys.exc_info()[0]
        finally:
            response.close()

    #auths is the string that has the list of authors to return
    def get_authors(self, auths):
        result = []
        authors = re.sub(r'<[^<]+?>', '', auths[:-1]).split(', ')
        for author in authors:
            lname, name = author.split(' ')
            #add periods after each letter in the first name
            fname = ''
            for c in name:
                fname += c + '.'
            result.append(lname + ', ' + fname)
        self.authors = result
        return self.authors

    #call this after downloading the object
    def fill_data(self):
        try:
            matches = re.search('<div class="rprt_all"><div class="rprt abstract"><div class="cit">' +
                                '<a.*>(?P<journal>.*)</a> (?P<bib_year>\d{4}).*?;(?P<bib_volume>.*?):' +
                                '(?P<bib_pages>.*?)\..*</div><h1>(?P<title>.*?)</h1><div class="auths">(?P<auths>.*?)</div>' +
                                '<div class="aff">.*<p>(?P<aff>.*?)</p></div>', self.html_file)

            self.title = matches.group('title')
            #print "Title: " + self.title
            self.get_authors(matches.group('auths'))
            #print "Authors: %s" % ', '.join(self.authors)
            self.journal = matches.group('journal')
            #print "Journal: " + self.journal
            self.pub_year = matches.group('bib_year')
            #print "Pub_year: " + self.pub_year
            self.volume = matches.group('bib_volume')
            #print "Volume: " + self.volume
            self.pages = matches.group('bib_pages')
            #print "Pages: " + self.pages
        except AttributeError as e:
            print "Not enough information was found for\n\t" + self.pubmed_url
            pass

    def get_formatted(self):
        new_file = ''
        new_file += ('\t<tr>\n\t\t<td valign="top" class="resourcesICO">')
        new_file +=     ('<a href="%s" target="_blank"><img src="../../image/ico_sitelink.gif" width="24" height="24" /></a></td>\n') % (self.external_url)
        new_file += ('\t\t<td><a href="%s" target="_blank">%s</a><br />\n') % (self.external_url, self.title)
        new_file += ('\t\t%s<br />\n') % (', '.join(self.authors))
        new_file += ('\t\t<em>%s, %s, %s, %s.</em></td>\n') % (self.journal, self.pub_year, self.volume, self.pages)
        new_file += ('\t</tr>\n')
        return new_file


def getproperfilename(s):
    validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in s if c in validFilenameChars)    

def process_doi(doi):
    doi_object = PubMedObject(doi)
    try:
        #print "Downloading " + doi_object.pubmed_url + "..."
        doi_object.download()
        doi_object.fill_data()
        return doi_object.get_formatted()
    except urllib2.HTTPError:
        print "Skipping " + doi_object.pubmed_url + "..."
        return ''

def main2(args):
    try:
        # program's main code here
        # You can also enter a PubMed id using the syntax pmid:xxxxxxxx
        print "Enter the doi to process.  Leave blank to use the dois.txt file."
        print "You can also enter a PubMed id using the syntax pmid:xxxxxxxx"
        doi = raw_input()
        if doi == '':
            with open('dois.txt','r') as doi_file:
                for doi in doi_file:
                    with open('simple.html','a') as sum_file:
                        sum_file.write(process_doi(doi))
                doi_file.close()
        else:
            print process_doi(doi)

    except BaseException as e:
        print traceback.format_exc()
        print "Error: %s %s" % (sys.exc_info()[0], e.args)
        return 1
    except:
        # error handling code here
        print "Error: %s" % sys.exc_info()[0]
        return 1  # exit on error
    else:
        return 0  # exit errorlessly

def main(args):
    doi_object = PubMedObject("pmid:"+str(22875554))
    try:
        #print "Downloading " + doi_object.pubmed_url + "..."
        doi_object.download()
        doi_object.fill_data()
        print doi_object.authors
        print doi_object.journal
        print doi_object.title
        print doi_object.pages
        print doi_object.pub_year
        print doi_object.volume

        #return doi_object.get_formatted()
    except urllib2.HTTPError:
        print "Skipping " + doi_object.pubmed_url + "..."
        return ''


#if __name__ == '__main__':
#    sys.exit(main(sys.argv))
