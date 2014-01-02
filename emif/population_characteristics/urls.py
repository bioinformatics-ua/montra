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
    url(r'^$',
            population, name='population'),
    # url(r'^csv/(?P<qid>\d+)/$',
    #         export_csv, name='export_csv'),
    # url(r'^(?P<runcode>[^/]+)/progress/$',
    #         get_async_progress, name='progress'),
    # url(r'^(?P<runcode>[^/]+)/(?P<qs>[-]{0,1}\d+)/$',
    #         questionnaire, name='questionset'),
    # url(r'^(?P<runcode>[^/]+)/$',
    #         questionnaire, name='questionnaire'),
)
