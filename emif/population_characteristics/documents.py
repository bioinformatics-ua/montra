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
import json

from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, ListView

from .response import JSONResponse, response_mimetype
from .serialize import serialize
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required

from fingerprint.services import attachPermissions, merge_highlight_results

from emif.views import get_api_info

from questionnaire.services import createqsets, createqset

from questionnaire.models import QuestionSet

from django.shortcuts import render

import os

from django.conf import settings

from .parseJerboaFile import *
from .services import *
from docs_manager.storage_handler import *
from population_characteristics.models import *
from fingerprint.models import Fingerprint, FingerprintSubscription

from docs_manager.views import get_revision
from population_characteristics.tasks import aggregation

from public.models import PublicFingerprintShare

from public.utils import hasFingerprintPermissions

from accounts.models import EmifProfile

from django.core.exceptions import PermissionDenied

from django.http import Http404

def document_form_view_upload(request, fingerprint_id, template_name='documents_upload_form.html'):
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
    chracteristic = Characteristic()
    chracteristic.user = request.user
    chracteristic.fingerprint_id = fingerprint_id
    chracteristic.revision = revision
    chracteristic.path = path_file
    chracteristic.file_name = file_name
    chracteristic.name = request.POST['pc_name']
    chracteristic.description = request.POST['pc_comments']
    chracteristic.save()

    # Parse the Jerboa and insert it in MongoDB
    # The best option will be use django-celery

    #_json = import_population_characteristics_data(request.user, fingerprint_id,filename=path_file)

    pc = PopulationCharacteristic()
    data_jerboa = pc.submit_new_revision(request.user, fingerprint_id, revision, path_file)


    aggregation.apply_async([fingerprint_id, data_jerboa])
    response = JSONResponse(data, mimetype=response_mimetype(request))
    response['Content-Disposition'] = 'inline; filename=files.json'
    return response

def jerboa_form_view_upload(request, fingerprint_id, template_name='documents_upload_form.html'):
    """ Upload files from Jerboa
    """
    # TODO: for now it is only calling the documents
    return document_form_view_upload(request, fingerprint_id, template_name='documents_upload_form.html')

def parsejerboa(request, template_name='documents_upload_form.html'):
    """ Parse files from Jerboa
    """
    path_file = "C:/Users/lbastiao/Projects/TEST_DataProfile_v1.5.6b.txt"
    path_file = "/Volumes/EXT1/Dropbox/MAPi-Dropbox/EMIF/Jerboa/TEST_DataProfile_v1.5.6b.txt"


    _json = import_population_characteristics_data(request.user, filename=path_file)

    pc = PopulationCharacteristic()
    pc.submit_new_revision(request.user, fingerprint_id, revision)
    data = {'data': _json}
    response = JSONResponse(data, mimetype=response_mimetype(request))
    response['Content-Disposition'] = 'inline; filename=files.json'
    return response

def single_qset_view(request, runcode, qsid, template_name='fingerprint_qs.html'):

    if not hasFingerprintPermissions(request, runcode):
        raise PermissionDenied


    h = None
    if "query" in request.session and "highlight_results" in request.session:
        h = request.session["highlight_results"]
    #if "query" in request.session and "highlight_results" in request.session and runcode in request.session["highlight_results"]:
    #    h =  merge_highlight_results(request.session["query"] , request.session["highlight_results"][runcode])
    #   print h["questions"]

    qset, name, db_owners, fingerprint_ttype = createqset(runcode, qsid, highlights=h)

    return render(request, template_name,{'request': request, 'qset': qset, 'fingerprint_id': runcode})


def document_form_view(request, runcode, qs, activetab='summary', readOnly=False, public_key = None,
    template_name='documents_upload_form.html'):

    h = None

    if "query" in request.session and "highlight_results" in request.session:
        h = request.session["highlight_results"]

    # GET fingerprint primary key (for comments)
    fingerprint = None

    try:
        fingerprint = Fingerprint.objects.get(fingerprint_hash=runcode)
        fingerprint_pk = fingerprint.id
    except:
        fingerprint_pk = 0
        raise Http404

    qsets, name, db_owners, fingerprint_ttype = createqsets(runcode, highlights=h)

    if fingerprint_ttype == "":
        raise "There is a missing type of questionnarie, something is really wrong"

    try:
        if (not request.user.is_anonymous()):
            eprofile = EmifProfile.objects.get(user=request.user)

            if eprofile.restricted == True:
                if not eprofile.has_permission(runcode):
                    raise PermissionDenied


    except EmifProfile.DoesNotExist:
        raise "-- ERROR: Couldn't get emif profile for user"


    apiinfo = json.dumps(get_api_info(runcode))
    owner_fingerprint = False

    for owner in db_owners.split(" "):
        #print request.user.username
        if (owner == request.user.username):
            owner_fingerprint = True

    query_old = None
    try:
        query_old = request.session.get('query', "")
    except:
        query_old = None

    name_bc = name
    try:
        name_bc = name.encode('utf-8')
    except:
        pass

    isAdvanced = None

    if(request.session.get('isAdvanced') == True):
        isAdvanced = True
    else:
        isAdvanced = False

    qsets = attachPermissions(runcode, qsets)

    jerboa_files = Characteristic.objects.filter(fingerprint_id=runcode).order_by('-latest_date')


    contains_population = False
    latest_pop = None
    if len(jerboa_files)!=0:
        contains_population = True
        latest_pop = jerboa_files[0]



    # Find if user has public links for this db.

    public_links = None

    if (owner_fingerprint or request.user.is_staff) and fingerprint != None:
        public_links = PublicFingerprintShare.objects.filter(user=request.user, fingerprint=fingerprint)

    # increase database hits
    hits = 0
    if fingerprint != None:
        hits = fingerprint.hits+1
        fingerprint.hits = hits
        fingerprint.save()

    subscription = False

    try:
        if (not request.user.is_anonymous()):
            subs = FingerprintSubscription.objects.get(user = request.user, fingerprint = fingerprint)

            subscription = not subs.removed

    except FingerprintSubscription.DoesNotExist:
        pass

    return render(request, template_name,
        {'request': request, 'qsets': qsets, 'export_bd_answers': True,
        'apiinfo': apiinfo, 'fingerprint_id': runcode,
                    'fingerprint': fingerprint,
                    'fingerprint_pk': fingerprint_pk,
                    'fingerprint_fill': int(round(fingerprint.fill)),
                   'breadcrumb': True, 'breadcrumb_name': name_bc.decode('utf-8'),
                    'style': qs, 'collapseall': False,
                    'owner_fingerprint':owner_fingerprint,
                    'owners': db_owners,
                    'owner_obj': fingerprint.owner,
                    'shared_obj': fingerprint.shared,
                    'fingerprint_dump': True,
                    'contains_population': contains_population,
                    'latest_pop': latest_pop,
                    'hide_add': True,
                    'fingerprint_ttype': fingerprint_ttype,
                    'search_old': query_old,
                    'isAdvanced': isAdvanced,
                    'activetab': activetab,
                    'readOnly': readOnly,
                    'public_link': public_links,
                    'public_key': public_key,
                    'hits': hits,
                    'subscription': subscription,
                    })




