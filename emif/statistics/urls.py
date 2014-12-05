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


urlpatterns = patterns('',

    # Statististics
    url(r'^statistics/(?P<questionnaire_id>[0-9]+)$', 'statistics.views.database_stats_qs'),


    # statistics
    # /statistics/<fingerprint_schema_id>/total/databases
    # /statistics/<fingerprint_schema_id>/total/users
    # /statistics/<fingerprint_schema_id>/total/filled/question
    # /statistics/<fingerprint_schema_id>/total/filled/questionsets

    # /statistics/<fingerprint_schema_id>/avg/filled/question

    # /statistics/<fingerprint_id>/<question_id>/distribution

    url(r'^statistics/(?P<fingerprint_id>[^/]+)/$', TopNavigatorsView.as_view(), name='topnavigators'),
    url(r'^statistics/(?P<questionnaire_id>[0-9]+)/$', TopNavigatorsView.as_view(), name='topnavigators'),


)
