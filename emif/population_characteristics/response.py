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

from django.http import HttpResponse
from django.utils import simplejson

MIMEANY = '*/*'
MIMEJSON = 'application/json'
MIMETEXT = 'text/plain'


def response_mimetype(request):
    """response_mimetype -- Return a proper response mimetype, accordingly to
    what the client accepts, as available in the `HTTP_ACCEPT` header.

    request -- a HttpRequest instance.

    """
    can_json = MIMEJSON in request.META['HTTP_ACCEPT']
    can_json |= MIMEANY in request.META['HTTP_ACCEPT']
    return MIMEJSON if can_json else MIMETEXT


class JSONResponse(HttpResponse):
    """JSONResponse -- Extends HTTPResponse to handle JSON format response.

    This response can be used in any view that should return a json stream of
    data.

    Usage:

        def a_iew(request):
            content = {'key': 'value'}
            return JSONResponse(content, mimetype=response_mimetype(request))

    """
    def __init__(self, obj='', json_opts=None, mimetype=MIMEJSON, *args, **kwargs):
        json_opts = json_opts if isinstance(json_opts, dict) else {}
        content = simplejson.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)
