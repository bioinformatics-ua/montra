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

import json

from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, ListView

from .response import JSONResponse, response_mimetype
from .serialize import serialize
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required

from emif.views import createqsets, get_api_info
from django.shortcuts import render

import os

from django.conf import settings

from .parseJerboaFile import * 
from .services import * 

class HandleFile(object):
    """This class handle with the file upload for multiple backends
    """
    def __init__(self, wrapper):
        self._handler_wrapper = wrapper

    def handle_file(self, f):
        """
        Handle File
        """
        self._handler_wrapper.handle_uploaded_file(f)

        # Store the metadata   


class FileSystemHandleFile(object):
    """Store the file in file system
    """
    def __init__(self):
        pass

    def handle_uploaded_file(self, f):
        """Store the files in file disk 
        """

        with open(os.path.join(os.path.abspath(settings.PROJECT_DIR_ROOT + 'emif/static/files/'), f.name),
                  'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

class MongoDBHandleFile(object):
    """Store the file in MongoDB
    """
    def __init__(self):
        pass

    def handle_uploaded_file(self, f):
        """Store the files in file disk 
        """
        pass


def document_form_view_upload(request, template_name='documents_upload_form.html'):
    """Store the files at the backend 
    """

    # Create the backend to store the file 
    fh = FileSystemHandleFile()
    g_fh = HandleFile(fh)

    files = []
    # Run it for all the sent files (apply the persistence storage)
    if request.FILES:
        for name, f in request.FILES.items():
            # Handle file 
            g_fh.handle_file(f)
            
            # Serialize the response 
            files.append(serialize(f))
    
    data = {'files': files}
    response = JSONResponse(data, mimetype=response_mimetype(request))
    response['Content-Disposition'] = 'inline; filename=files.json'
    return response

def jerboa_form_view_upload(request, template_name='documents_upload_form.html'):
    """ Upload files from Jerboa
    """
    # TODO: for now it is only calling the documents 
    return document_form_view_upload(request, template_name='documents_upload_form.html')

def jerboa_list_values(request, param, template_name='documents_upload_form.html'):

    pc = PopulationCharacteristic(None)
    values = pc.get_variables(param)
    data = {'values': values}
    response = JSONResponse(data, mimetype=response_mimetype(request))
    response['Content-Disposition'] = 'inline; filename=files.json'
    return response



def parsejerboa(request, template_name='documents_upload_form.html'):
    """ Parse files from Jerboa
    """
    path_file = "/Volumes/EXT1/Dropbox/MAPi-Dropbox/EMIF/Jerboa/TEST_DataProfile_v1.5.6b.txt"
    _json = import_population_characteristics_data(filename=path_file)

    pc = PopulationCharacteristic()
    pc.submit_new_revision()
    data = {'data': _json}
    response = JSONResponse(data, mimetype=response_mimetype(request))
    response['Content-Disposition'] = 'inline; filename=files.json'
    return response


def document_form_view(request, runcode, qs, template_name='documents_upload_form.html'):
    
    qsets, name, db_owners, fingerprint_ttype = createqsets(runcode)

    if fingerprint_ttype == "":
        raise "There is missing ttype of questionarie, something is really wrong"

    apiinfo = json.dumps(get_api_info(runcode));
    owner_fingerprint = False
    for owner in db_owners.split(" "):
        print owner
        print request.user.username
        if (owner == request.user.username):
            owner_fingerprint = True
    
    return render(request, template_name, 
        {'request': request, 'qsets': qsets, 'export_bd_answers': True, 
        'apiinfo': apiinfo, 'fingerprint_id': runcode,
                   'breadcrumb': True, 'breadcrumb_name': name.decode('ascii', 'ignore'),
                    'style': qs, 'collapseall': False, 
                    'owner_fingerprint':True,
                    'fingerprint_dump': True,
                    'contains_population': False,
                    'fingerprint_ttype': fingerprint_ttype,
                    })




