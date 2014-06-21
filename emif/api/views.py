# -*- coding: utf-8 -*-
# Copyright (C) 2013 Luís A. Bastião Silva and Universidade de Aveiro
#
# Authors: Luís A. Bastião Silva <bastiao@ua.pt>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


from django.http import HttpResponse

from django.contrib.auth.models import User, Group

from questionnaire.models import *
from questionnaire.parsers import *
from questionnaire.views import *
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.authentication import TokenAuthentication

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.utils import simplejson
from django.conf import settings

# import json
import md5
from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import AllowAny, IsAuthenticated

# Import Search Engine 

from searchengine.search_indexes import CoreEngine
from api.models import *

# Import pubmed object
from utils.pubmed import PubMedObject
#from emif.literature import fetch_by_pmid_by_becas

from docs_manager.storage_handler import *
from docs_manager.models import *

import os
import mimetypes

from fingerprint.models import Fingerprint

from public.views import PublicFingerprintShare
from public.services import deleteFingerprintShare, createFingerprintShare

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@api_view(('GET', 'POST', 'PUT', 'OPTIONS', 'HEAD'))
def api_root(request, format=None):
    return Response({
        'search': reverse('search', request=request),
        'getfile': reverse('getfile', request=request),
        'deletefile': reverse('deletefile', request=request),
        'metadata': reverse('metadata', request=request),
        'stats': reverse('stats', request=request),
        'validate': reverse('validate', request=request),
        'pubmed': reverse('pubmed', request=request),
    })


############################################################
##### Search (Extra information) - Web services
############################################################


class SearchView(APIView):
    """
    Class to search and return fingerprint details, like Name, ID and structure
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kw):
        
        # If authenticated
        if request.auth:
            user = request.user
            data = request.DATA
            result = validate_and_get(user, data)
            result['status'] = 'authenticated'
            result['method'] = 'GET'
            result['user'] = str(user)
            print request.DATA
         #if query!=None:
        else:
            result = {'status': 'NOT authenticated', 'method': 'GET'}

        response = Response(result, status=status.HTTP_200_OK)
        # response['Access-Control-Allow-Origin'] = "*"
        # response['Access-Control-Allow-Headers'] = "Authorization"
        #else:
        #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response


############################################################
##### Email Share - Web services
############################################################


class EmailCheckView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)    
    def post(self, request, *args, **kw):
        # first we get the email parameter
        email = request.POST.get('email', '')
        valid = False

        # Verify if it is a valid email
        if not (email == None or email==''):
            # Verify if it is a valid user name
            username = None

            try: 
                username = User.objects.get(email__exact=email)
                valid = True  
            except User.DoesNotExist:
                pass             
               
        result = {
            'email': email,
            'valid': valid
            }
        response = Response(result, status=status.HTTP_200_OK)
        return response

############################################################
##### Get File - Web services
############################################################


class GetFileView(APIView):

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kw):
        if request.user.is_authenticated():
            # first we get the email parameter
            name = request.POST.get('filename', '')
            revision = request.POST.get('revision', '')

            # Verify if we have name and revision
            if not (name == None or name=='' or revision == None or revision == ''):

                print name 
                print revision

                path_to_file = os.path.join(os.path.abspath(PATH_STORE_FILES), revision+name)
                print path_to_file
                return respond_as_attachment(request, path_to_file, name)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)

############################################################
##### Delete File - Web services
############################################################

class DeleteFileView(APIView):

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kw):
        # first we get the email parameter
        name = request.POST.get('filename', '')
        revision = request.POST.get('revision', '')
        fingerprint_id = request.POST.get('fingerprint_id', '')
        success = False

        # Verify if we have name and revision
        if not (fingerprint_id == None or fingerprint_id =='' or 
            name == None or name=='' or revision == None or revision == ''):
            
            user = request.user

            try:
                # We are setting as removed all revisions (not just the last one)
                files = FingerprintDocuments.objects.filter(
                        fingerprint_id=fingerprint_id, 
                        file_name=name)

                # we only allow deleting for the owner of this file, or the administrators
                if files != None and (user.is_superuser or user == files[0].user):

                    for f in files:
                        f.removed = True
                        
                        f.save()
                    
                    success = True

            except FingerprintDocuments.DoesNotExist:
                pass


        return Response({'result': success}, status=status.HTTP_200_OK)

# Ref from https://djangosnippets.org/snippets/1710/

def respond_as_attachment(request, file_path, original_filename):
    fp = open(file_path, 'rb')
    response = HttpResponse(fp.read())
    fp.close()
    type, encoding = mimetypes.guess_type(original_filename)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    response['Content-Length'] = str(os.stat(file_path).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding

    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        filename_header = 'filename=%s' % original_filename.encode('utf-8')
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(original_filename.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response

############################################################
##### Advanced Search - Web services
############################################################


class AdvancedSearchView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)  

    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        get_arg1 = request.GET.get('arg1', None)
        get_arg2 = request.GET.get('arg2', None)

        result = {'myValue': 'lol', 'myValue2': 'lol', }
        response = Response(result, status=status.HTTP_200_OK)
        return response

############################################################
##### AddPublic Link Webservice
############################################################

class AddPublicLinkView(APIView):

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kw):
        if request.user.is_authenticated():
            # first we get the email parameter
            fingerprint_id = request.POST.get('fingerprint_id', '')


            try:
                fingerprint = Fingerprint.objects.get(fingerprint_hash=fingerprint_id)

                # add only if necessary, try to get first...
                share = None
                try:
                    share = PublicFingerprintShare.objects.get(fingerprint=fingerprint, user=request.user)

                except PublicFingerprintShare.DoesNotExist:
                    share = createFingerprintShare(fingerprint_id, request.user)

                return Response({
                                    'hash': str(share.hash),
                                    'id'  : share.id
                                }, status=status.HTTP_200_OK)

            except Fingerprint.DoesNotExist:
                print "-- Error, tried to create link to fingerprint hash that does not exist."

        return Response({}, status=status.HTTP_400_BAD_REQUEST)

############################################################
##### DeletePublic Link Webservice
############################################################

class DeletePublicLinkView(APIView):

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kw):
        if request.user.is_authenticated():
            # first we get the email parameter
            share_id = request.POST.get('share_id', '')

            deleted = deleteFingerprintShare(share_id)

            return Response({'deleted': deleted}, status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)

############################################################
##### Metadata - Managemnt (Extra Information) Web services
############################################################


class MetaDataView(APIView):
    """
    Class to insert or update data values of one fingerprint
    Method POST: to insert a new field and value
    Method PUT: to update a value that already exists
    Note: both methods check if field value already exists and, if exists, it is updated,
    otherwise the field is created and the value added
    """

    # Example request
    # curl -H "Content-Type: application/json" -X POST -d "{\"uid\":12,\"token\":\"asdert\"}" http://192.168.1.3:8000/api/metadata -H "Authorization: Token c6e25981c67ae45f98bdb380b0a9d8164e7ec4d1" -v
    authentication_classes = (TokenAuthentication,SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)  
    # permission_classes = (permissions.AllowAny,)
    # permission_classes = (permissions.IsAuthenticated,)
    parser_classes((JSONParser,))

    def post(self, request, *args, **kw):

        # If authenticated
        if request.auth:
            user = request.user
            data = request.DATA
            result = validate_and_save(user, data)
            result['status'] = 'authenticated'
            result['method'] = 'POST'
            result['user'] = str(user)

        # NOT authenticated
        else:
            result = {'status': 'NOT authenticated', 'method': 'POST'}

        response = Response(result, status=status.HTTP_200_OK)
        return response

    def put(self, request, *args, **kw):

        # If authenticated
        if request.auth:
            user = request.user
            data = request.DATA
            result = validate_and_save(user, data)
            result['status'] = 'authenticated'
            result['method'] = 'PUT'
            result['user'] = str(user)

        # NOT authenticated
        else:
            result = {'status': 'NOT authenticated', 'method': 'PUT'}
        response = Response(result, status=status.HTTP_200_OK)

        return response


class ValidateView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kw):

        database_name = request.GET['name']
        
        c = CoreEngine()
        results = c.search_fingerprint("database_name_t:\"" +database_name+'"')

        contain = len(results) != 0
        # Dirty hack: check if the database name is really equals
        if contain:
            for r in results:
                try:
                    if database_name != r['database_name_t']:
                        contain = False

                except:
                    raise
                    contain = True


        result = {'contains': contain}

        response = Response(result, status=status.HTTP_200_OK)
        return response

    def post(self, request, *args, **kw):
        try:

            print request.POST.items()
            for i in request.POST.items():
                print i[0]
                json_test = json.loads(i[0])
                print json_test

            result = {'test': 'teste2'}
            response = Response(result, status=status.HTTP_200_OK)
        except:
            print("fuck")
            raise
        return response



############################################################
############ Statistics Web services
############################################################


class StatsView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)    
    """
    Class that returns json values of answers to create stats (charts)
    """

    def get(self, request, *args, **kw):
        """
        Method to return values on format json
        :param request:
        :param args:
        :param kw:
        """

        try:
            results = dict()

            # GET Values
            questionnaire_id = int(request.GET['q_id'])
            question_set = int(request.GET['qs_id'])
            slug = request.GET['slug']

            question = Question.objects.filter(questionset_id=question_set, slug_fk__slug1=slug, stats='1',
                                               questionset__questionnaire=questionnaire_id).order_by('number')

            results = self.getResults(question)

            if results:
                #Dump json file
                result = json.dumps(results)
            else:
                result = []
                # print(result)

            response = Response(result, status=status.HTTP_200_OK)
        except:
            print("fuck")
            raise
        return response

    def getResults(self, question):
        """
        Method that returns values to use in charts
        :param question:
        """

        from emif.statistics import Statistic

        results = dict()
        graphs = []
        for q in question:
            try:
                s = Statistic(q)

                graph = s.get_percentage()
                # print graph
                if not graph:
                    # results["values"] = "No"
                    #Return NULL if graph is empty
                    return results
                else:
                    # results["values"] = "Yes"
                    for g in graph:
                        # print g
                        for i in g:
                            graphs_aux = dict()
                            # print i, g[i]
                            graphs_aux['name'] = i
                            graphs_aux['score'] = g[i]
                            graphs.append(graphs_aux)
            except:
                raise

        results["attr1"] = "name"
        results["attr2"] = "score"
        results['charts'] = graphs

        return results



############################################################
############ Publication Web services
############################################################


class PublicationsView(APIView):
    """
    Class that returns the information of a publication 
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, *args, **kw):
        results = dict()
        pmid = request.GET['pmid']
        
        if (pmid==None or pmid==''):
            return Response(results, status=status.HTTP_400_BAD_REQUEST)    
        
        doi_object = PubMedObject(pmid)
        request_status = doi_object.fetch_info()

        if request_status != None:
            results['authors'] =  doi_object.authors
            results['title'] =  doi_object.title
            results['pages'] =  doi_object.pages
            results['pub_year'] =  doi_object.pub_year
            results['journal'] =  doi_object.journal
            results['pubmed_url'] =  doi_object.pubmed_url
            results['volume'] =  doi_object.volume
            return Response(results, status=status.HTTP_200_OK)

        return Response(results, status=status.HTTP_400_BAD_REQUEST)    
            



############################################################
############ Populations Characteristics Web services
############################################################

class PopulationView(APIView):
    """PopulationCharactersticsService
    This web service is responsabible to handle jerboa documents 

    """
    
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)        
    def get(self, request, *args, **kw):
        """
        List the Jerboa documents 
        """
        pass

    def post(self, request, *args, **kw):
        """
        Upload Jerboa files
        """
        pass


############################################################
############ Auxiliar functions ############################
############################################################
def validate_fingerprint(user, fingerprintID):
    """
    Verify if fingerprint belongs to given user
    :param user:
    :param fingerprintID:
    """

    result = False
    c = CoreEngine()
    results = c.search_fingerprint('user_t:' + '"' + user.username + '"')

    for r in results:
        if fingerprintID == r['id']:
            result = True
            break
    return result


def validate_and_save(user, data):
    """
    Verify if json structure is correct and create/update values of fingerprint

    :param user:
    :param data:
    """
    result = {}
    fields_text = ""
    # Verify if json structure is valid
    if 'fingerprintID' in data.keys():
        fingerprintID = data['fingerprintID']

        # Verify if fingerprint belongs to user
        if validate_fingerprint(user, fingerprintID):
            if 'values' in data.keys():
                for f in data['values']:
                    # Check if field already exists
                    if FingerprintAPI.objects.filter(fingerprintID=fingerprintID, field=f):
                        try:
                            fp = FingerprintAPI.objects.get(fingerprintID=fingerprintID, field=f)
                            if str(fp.value) != str(data['values'][f]):
                                # Update value
                                fp.value += ' ' + data['values'][f]
                                fields_text = data['values'][f]
                                fp.save()
                                result[f] = "Updated successfully"
                            else:
                                result[f] = "Not updated"
                        except:
                            # print "Erro a atualizar o registo"
                            result[f] = "Error to update field"
                    # If field does not exist
                    else:
                        try:
                            fingerprint = FingerprintAPI(fingerprintID=fingerprintID, field=f,
                                                         value=data['values'][f], user=user)
                            # Create new field-value
                            fields_text += ' ' + data['values'][f]
                            fingerprint.save()
                            result[f] = "Created successfully"
                        except:
                            # print "Erro a criar o novo registo"
                            result[f] = "Error to create new field"

            # No values key in JSON structure
            else:
                # print "Não tem valores"
                result['error'] = "No values detected"
        else:
            result['error'] = "Error find FingerprintID"
    else:
        # print "Não tem nenhuma chave fingerprint"
        result['error'] = "No fingerprintID detected"

    
    c = CoreEngine()
    results = c.search_fingerprint("id:" + fingerprintID)
    _aux = None
    for r in results:
        _aux = r
        break


    if (_aux!=None):
        _aux['text_t']  = _aux['text_t'] + fields_text  
        c.index_fingerprint_as_json(_aux)

    return result


def validate_and_get(user, data):

    result = {}
    # Verify if json structure is valid
    if 'fingerprintID' in data.keys():
        fingerprintID = data['fingerprintID']

        # Verify if fingerprint belongs to user
        if validate_fingerprint(user, fingerprintID):
            result['fingerprintID'] = fingerprintID
            results = FingerprintAPI.objects.filter(fingerprintID=fingerprintID)
            result['values'] = {}
            for r in results:
                # print str(r.field) + " -> " + str(r.value)
                result['values'][r.field] = r.value

        else:
            result['error'] = "Error find FingerprintID"
    else:
        # print "Não tem nenhuma chave fingerprint"
        result['error'] = "No fingerprintID detected"

    return result
