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

from django.contrib.auth.models import User
from questionnaire.models import *
from questionnaire.parsers import *
from questionnaire.views import *
from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json
import md5
from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import AllowAny, IsAuthenticated

# Import Search Engine 

from searchengine.search_indexes import CoreEngine


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@api_view(('GET', 'POST', 'OPTIONS'))
def api_root(request, format=None):
    return Response({
        'search': reverse('search', request=request),
        'insert': reverse('insert', request=request),
        'stats': reverse('stats', request=request),
        'validate': reverse('validate', request=request),

    })


class SearchView(APIView):
    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        #query = request.GET.get('query', None)

        for param in request.GET:
            print(param)
            print(request.GET.get(param))
        response = None
        #if query!=None:

        result = {'myValue': 'lol', 'myValue2': 'lol', }
        response = Response(result, status=status.HTTP_200_OK)
        #else:
        #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response


class AdvancedSearchView(APIView):
    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        get_arg1 = request.GET.get('arg1', None)
        get_arg2 = request.GET.get('arg2', None)

        result = {'myValue': 'lol', 'myValue2': 'lol', }
        response = Response(result, status=status.HTTP_200_OK)
        return response


class InsertView(APIView):
    def get(self, request, *args, **kw):
        result = {'myV22222alue': 'lol', 'myValue2': 'lol'}
        response = Response(result, status=status.HTTP_200_OK)

        return response

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        # query = request.POST.get('myValue2', None)
        # print (query)
        # print(json.loads(request.POST.get('_content')).get('myValue'))
        print request.POST
        # for param in request.POST:
        #     print(param)
        #     print(request.POST.get(param))
        #print "dasd"
        #print request.POST.items()
        #for i in request.POST.items():
        #    print i[0]
        #    json_test = json.loads(i[0])
        #    print json_test
        #data = JSONParser().parse(request)


        #c = CoreEngine()
        #print request.content_type
        #print request
        #print(json.loads(request.POST.get('_content')))

        #c.index_fingerprint_as_json(json.loads(request.POST.get('_content')))

        result = {'myValue': 'lol', 'myValue2': 'lol'}
        response = Response(result, status=status.HTTP_200_OK)

        return response


class ValidateView(APIView):
    def get(self, request, *args, **kw):

        database_name = request.GET['name']
        c = CoreEngine()
        results = c.search_fingerprint("database_name_t:" + database_name)
        result = {'contains': len(results) != 0}

        response = Response(result, status=status.HTTP_200_OK)
        return response


    def post(self, request, *args, **kw):
        try:

            print request.POST.items()
            for i in request.POST.items():
                print i[0]
                json_test = json.loads(i[0])
                print json_test

            #database_name = request.POST['database_name']
            # c = CoreEngine()
            #results = c.search_fingerprint("database_name_t:"+database_name)
            #result = {'contains': len(results)==0}
            result = {'test': 'teste2'}
            response = Response(result, status=status.HTTP_200_OK)
        except:
            print("fuck")
            raise
        return response


class StatsView(APIView):
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
            for i in request.POST.items():
                print i

            # GET Values
            questionnaire_id = request.GET['q_id']
            question_set = request.GET['qs_id']
            slug = request.GET['slug']
            type = request.GET['type']

            question = Question.objects.filter(questionset_id=question_set, slug=slug).order_by('number')

            print "QUESTIONS: " + str(question.__len__())

            #Chart PIECHART
            if type == 'piechart':
                results = self.piechart(question, slug)

            print(results)
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

    def piechart(self, question, slug):
        """
        Method that returns values to use in piechart
        :param question:
        :param slug:
        """

        from emif.statistics import Statistic

        results = dict()
        graphs = []
        for q in question:
            try:
                s = Statistic(q)
                if s.question.slug == slug:
                    graph = s.get_percentage()
                    if not graph:
                        # results["values"] = "No"
                        #Return NULL if graph is empty
                        return results
                    else:
                        # results["values"] = "Yes"
                        print graph
                        for g in graph:
                            graphs_aux = dict()
                            for i in g:
                                graphs_aux['name'] = i
                                graphs_aux['score'] = g[i]
                                graphs.append(graphs_aux)
            except:
                raise

        results["charttype"] = "piechart"
        results["attr1"] = "name"
        results["attr2"] = "score"
        results['charts'] = graphs

        return results