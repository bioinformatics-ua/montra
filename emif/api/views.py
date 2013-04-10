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
from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import status


# Import Search Engine 

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@api_view(('GET',))
def api_root(request, format=None):
    
    return Response({
        'search': reverse('search', request=request),
        
    })
    if request.method == 'GET':
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchView(APIView):
    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        query = request.GET.get('query', None)

        for param in request.GET:
            print(param)
            print(request.GET.get(param))

        if query!=None:

            result = {'myValue': 'lol', 'myValue2': 'lol', }
            response = Response(result, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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



