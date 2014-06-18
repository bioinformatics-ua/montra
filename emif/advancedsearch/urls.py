# -*- coding: utf-8 -*-
# Copyright (C) 2014 Ricardo F. Gonçalves Ribeiro and Universidade de Aveiro
#
# Authors: Ricardo F. Gonçalves Ribeiro <ribeiro.r@ua.pt>
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
   
    # Literature tab, on database info view
    url(r'^history$', 'advancedsearch.views.history_defer'),  
    url(r'^history/(?P<page>[0-9]+)$', 'advancedsearch.views.history'),    
    url(r'^results/(?P<query_id>[0-9]+)$', 'advancedsearch.views.resultsdiff_history'), 
)
