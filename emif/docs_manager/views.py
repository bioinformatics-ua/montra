# -*- coding: utf-8 -*-
# Copyright (C) 2014 Universidade de Aveiro, DETI/IEETA, Bioinformatics Group - http://bioinformatics.ua.pt/
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
from docs_manager.services import *
from population_characteristics.response import JSONResponse, response_mimetype
from population_characteristics.serialize import serialize

from docs_manager.models import *

from django.core import serializers

from django.conf import settings
from docs_manager.storage_handler import *

import uuid

from dateutil.tz import tzutc

UTC = tzutc()
from django.db.models import Max

from public.utils import hasFingerprintPermissions

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


def get_revision():
    r = uuid.uuid1()
    r = str(r)
    r.replace("-","")
    return r


def upload_document(request, fingerprint_id, template_name='documents_upload_form.html'):
    """Store the files at the backend
    """

    # compute revision
    revision = get_revision()

    # Create the backend to store the file
    fh = FileSystemHandleFile()
    g_fh = HandleFile(fh)

    files = []
    # Run it for all the sent files (apply the persistence storage)
    path_file = None
    file_name = None
    if request.FILES:
        for name, f in request.FILES.items():
            # Handle file
            path_file = g_fh.handle_file(f, revision=revision)
            file_name = f.name
            # Serialize the response
            files.append(serialize(f))


    data = {'files': files}

    # Store the metadata in the database
    fd = FingerprintDocuments()
    fd.user = request.user
    fd.fingerprint_id = fingerprint_id
    fd.revision = revision
    fd.path = path_file
    fd.file_name = file_name
    fd.name = request.POST['pc_name']
    fd.description = request.POST['pc_comments']
    fd.save()

    response = JSONResponse(data, mimetype=response_mimetype(request))
    response['Content-Disposition'] = 'inline; filename=files.json'
    return response

def upload_file(request, fingerprint_id, template_name='documents_upload_form.html'):
    """ Upload files from Jerboa
    """
    # TODO: for now it is only calling the documents
    return upload_document(request, fingerprint_id, template_name='documents_upload_form.html')


def list_fingerprint_files(request, fingerprint):

    if not hasFingerprintPermissions(request, fingerprint):
        return HttpResponse("Access forbidden",status=403)

    # List the Jerboa files for a particular fingerprint
    jerboa_files = FingerprintDocuments.objects.filter(
            fingerprint_id=fingerprint,
            removed=False
        )

    files_latest_version = jerboa_files.values('file_name').annotate(latest=Max('latest_date'))

    file_records = []
    for file in files_latest_version:
        #print file['file_name']
        file_records.append(jerboa_files.get(file_name = file['file_name'], latest_date = file['latest']))

    #print file_records

    _data = []

    for f in file_records:
        _doc = {'name': f.name,
                'comments': f.description,
                'revision': f.revision,
                'file_name': f.file_name,
                #'path': f.path.replace(settings.PROJECT_DIR_ROOT, ''),
                'fingerprint_id': f.fingerprint_id  ,
                'latest_date': serialize_date(f.latest_date),
                }
        _data.append(_doc)

    data = {'conf': _data}
    response = JSONResponse(data, mimetype=response_mimetype(request))
    response['Content-Disposition'] = 'inline; filename=files.json'
    return response
