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

from django.shortcuts import render

from django.core import serializers
from django.conf import settings
from django.http import *
from django.http import Http404

from geopy import geocoders

from fingerprint.listings import get_databases_from_solr
from emif.models import City

from geolocation.services import *

from questionnaire.models import Questionnaire

from constance import config

def geo(request, template_name='geo.html'):
    # get_locations returns the coordinates for the DB locations
    return render(request, template_name, get_locations(request))
