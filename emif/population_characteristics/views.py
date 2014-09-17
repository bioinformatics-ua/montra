# -*- coding: utf-8 -*-
# Copyright (C) 2014 Luís A. Bastião Silva and Universidade de Aveiro
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

from django.shortcuts import render, render_to_response
from .services import *
from .response import JSONResponse, response_mimetype
from .comments import *
from .serialize import serialize
from .comparison import * 

from population_characteristics.models import *

from django.core import serializers

from django.conf import settings

from django.http import *


from dateutil.tz import tzutc

from public.utils import hasFingerprintPermissions

UTC = tzutc()

def serialize_date(dt):
    """
    Serialize a date/time value into an ISO8601 text representation
    adjusted (if needed) to UTC timezone.

    For instance:
    >>> serialize_date(datetime(2012, 4, 10, 22, 38, 20, 604391))
    '2012-04-10T22:38:20.604391Z'
    """
    if dt.tzinfo:
        dt = dt.astimezone(UTC).replace(tzinfo=None)
    return dt.isoformat() + 'Z'


def jerboa_list_values(request, var, row, fingerprint_id, revision, template_name='documents_upload_form.html'):

    if not hasFingerprintPermissions(request, fingerprint_id):
        return HttpResponse("Access forbidden",status=403)

    filters = []

    if request.POST:
        # Get the filters to apply.

        filters = {}
        myRq = dict(request.POST.lists())

        for i in myRq:
            if i == 'publickey':
                continue
            filters[i[8:-3]] = myRq[i]

            filters[i[8:-3]] = myRq[i]

        print filters    
    

    pc = PopulationCharacteristic(None)
    values = pc.get_variables(var, row, fingerprint_id, revision, filters=filters)
    data = {'values': values}
    response = JSONResponse(data, mimetype="application/json")
    response['Content-Disposition'] = 'inline; filename=files.json'
    return response


def comments(request, fingerprint_id=None, chart_id=None, comment_id=None):
    
    if request.method=="POST":
        # Add new comment

        # Extract fingerprint id
        fingerprint_id = request.POST["pc_chart_comment_fingerprint_id"]

        # Extract chart_id
        chart_id = request.POST["pc_chart_comment_id"]

        # Title and Description 
        title = request.POST["pc_chart_comment_name"]
        description = request.POST["pc_chart_comment_description"]

        # Now have the values, send it to the comment manager 
        cm = CommentManager(fingerprint_id)
        c = cm.comment(chart_id, title, description, request.user)

        status = True
        data = {'comments': status, 't_title' : c.title, "description": 
        c.description, "id": c.pk, "latest_date": serialize_date(c.latest_date)}
        response = JSONResponse(data, mimetype="application/json")
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    elif request.method=="GET":
        # List comments
        cm = CommentManager(fingerprint_id)
        comments = cm.get_list_comments(fingerprint_id, chart_id)
        lst_return = []
        for c in comments: 

            data = {'t_title' : c.title, "description": c.description, "id": c.pk, "latest_date": serialize_date(c.latest_date)}
            lst_return.append(data)
        response = JSONResponse(lst_return, mimetype="application/json")
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    elif request.method=="DELETE":

        cm = CommentManager(None)
        cm.delete(comment_id, request.user)
        response = JSONResponse({"sucess": True}, mimetype="application/json")
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
        
    elif request.method=="UPDATE":
        pass
    
    
    # Return bad requests
    return HttpResponseBadRequest()



def filters(request, var, fingerprint_id, template_name='documents_upload_form.html'):

    if not hasFingerprintPermissions(request, fingerprint_id):
        return HttpResponse("Access forbidden",status=403)

    pc = PopulationCharacteristic(None)
    values = pc.filters(var, fingerprint_id)
    _values = []
    for v in values:
        _values.append(v.to_JSON())
    data = {'values': _values}
    response = JSONResponse(data, mimetype=response_mimetype(request))
    response['Content-Disposition'] = 'inline; filename=files.json'
    return response

def generic_filter(request, param, template_name='documents_upload_form.html'):

    pc = PopulationCharacteristic(None)
    values = pc.generic_filter(param)
    data = {'values': values}
    response = JSONResponse(data, mimetype=response_mimetype(request))
    response['Content-Disposition'] = 'inline; filename=files.json'
    return response

def get_settings(request, runcode):
    if not hasFingerprintPermissions(request, runcode):
        return HttpResponse("Access forbidden",status=403)

    if (runcode=="COMPARE/"):
        return get_compare_settings(request)
    pc = PopulationCharacteristic(None)
    values = pc.get_settings()
    data = {'conf': values.to_JSON()}

    response = JSONResponse(data, mimetype=response_mimetype(request))
    response['Content-Disposition'] = 'inline; filename=files.json'
    return response

def list_jerboa_files(request, fingerprint):

    if not hasFingerprintPermissions(request, fingerprint):
        return HttpResponse("Access forbidden",status=403)

    # List the Jerboa files for a particular fingerprint
    jerboa_files = Characteristic.objects.filter(fingerprint_id=fingerprint)
    _data = []    
    for f in jerboa_files:
        _doc = {'name': f.name, 
                'comments': f.description,
                'revision': f.revision,
                'file_name': f.file_name,
                'path': f.path.replace(settings.PROJECT_DIR_ROOT, ''),
                'fingerprint_id': f.fingerprint_id  ,
                'latest_date': serialize_date(f.latest_date),
                }
        _data.append(_doc)

    data = {'conf': _data}
    response = JSONResponse(data, mimetype=response_mimetype(request))
    response['Content-Disposition'] = 'inline; filename=files.json'
    return response

def compare(request):
    return handle_compare(request)

def compare_values(request,  var, row, fingerprint_id):
    return handle_compare_values(request, var, row, fingerprint_id)

