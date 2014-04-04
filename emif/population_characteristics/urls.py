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
from django.conf.urls.defaults import *
from views import *
from documents import * 

urlpatterns = patterns('',
   
    # Upload Documents to Jerboa
    url(r'^upload$', 'population_characteristics.documents.document_form_view_upload'),
    url(r'^jerboaupload/(?P<fingerprint_id>[^/]+)/$', 'population_characteristics.documents.jerboa_form_view_upload'),
    
    # List Jerboa Files
    url(r'^jerboafiles/(?P<fingerprint>[^/]+)/$', 'population_characteristics.views.list_jerboa_files'),

    # List staff to the charts
    url(r'^jerboalistvalues/(?P<var>[^/]+)/(?P<row>[^/]+)/(?P<fingerprint_id>[^/]+)$', 
        'population_characteristics.views.jerboa_list_values'),
    url(r'^filters/(?P<var>[^/]+)/(?P<fingerprint_id>[^/]+)$', 
        'population_characteristics.views.filters'),
    url(r'^genericfilter/(?P<param>[^/]+)$', 'population_characteristics.views.generic_filter'),

    # Settings
    url(r'^settings/(?P<runcode>[^/]+)/$', 'population_characteristics.views.get_settings'),

    # Parsing Jerboa 
    url(r'^parsejerboa$', 'population_characteristics.documents.parsejerboa'),

    # Comments 
    url(r'^comments$', 'population_characteristics.views.comments'),
    url(r'^comments/(?P<fingerprint_id>[^/]+)/(?P<chart_id>[^/]+)$', 'population_characteristics.views.comments'),
    url(r'^comments/(?P<comment_id>[^/]+)$', 'population_characteristics.views.comments'),

    # Compare
    url(r'^compare$', 'population_characteristics.views.compare'),

    # Just testing URLs:
    url(r'^new/(?P<runcode>[^/]+)/(?P<qs>[-]{0,1}\d+)/$', 'population_characteristics.documents.document_form_view'),
    
    
)
