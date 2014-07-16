
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json
import csv
import sys

from utils.pubmed import PubMedObject

def pm_to(inFile, outFile):
    print "RUNNING"
    def get(pmid):
        results = dict()
        
        if (pmid==None or pmid==''):
            results["pmid"] = ""
            results['authors'] = ""
            results['title'] =  ""
            results['pages'] =  ""
            results['year'] =  ""
            results['journal'] = "" 
            results['volume'] =  ""
            return results    
        
        doi_object = PubMedObject(pmid)
        request_status = doi_object.fetch_info()

        if request_status != None:
            results["pmid"] = pmid
            results['authors'] =  doi_object.authors
            results['title'] =  doi_object.title
            results['pages'] =  doi_object.pages
            results['year'] =  doi_object.pub_year
            results['journal'] =  doi_object.journal
            results['volume'] =  doi_object.volume
            return results

        results["pmid"] = ""
        results['authors'] = ""
        results['title'] =  ""
        results['pages'] =  ""
        results['year'] =  ""
        results['journal'] = "" 
        results['volume'] =  ""

        return results

    f = open(inFile, "r")
    lines = f.readlines()
    idList = json.loads("".join(lines))
    f.close()

    f0 = open(outFile, 'wb')

    retList = []
    MAX_COUNT = 10
    
    outList = []
    for entry in idList:
        count = entry["count"]
        if count > 0:    
            res = get(entry["list"][0])
        else:
            res = get(None)
        outList.append(res)

    st = json.dumps(outList, sort_keys=True, indent=4, separators=(',', ': '))
    print st

    f0.write(st)
    f0.close()

    print "QUITTING"