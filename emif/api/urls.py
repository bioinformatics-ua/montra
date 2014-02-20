#!python
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

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import SearchView
from api.views import MetaDataView
from api.views import StatsView
from api.views import ValidateView
from api.views import PublicationsView
from api.views import PopulationView

urlpatterns = patterns('api.views',
    url(r'^root/$', 'api_root'),
    url(r'^search$', SearchView.as_view(), name='search'),
    url(r'^metadata', MetaDataView.as_view(), name='metadata'),
    url(r'^stats$', StatsView.as_view(), name='stats'),
    url(r'^validate$', ValidateView.as_view(), name='validate'),
    url(r'^pubmed$', PublicationsView.as_view(), name='pubmed'),
    url(r'^population$', PopulationView.as_view(), name='population'),

)

urlpatterns = format_suffix_patterns(urlpatterns)
