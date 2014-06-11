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

from django.shortcuts import render, render_to_response

from django.core import serializers
from django.conf import settings
from django.http import *


def fingerprint_list(request, template_name='fingerprints.html'):

    print request.user

    links = []
    #links = PublicFingerprintShare.objects.filter(user=)

    return render(request, template_name, {'request': request, 'links': links})

def fingerprint(request, fingerprint_id, template_name='templates/fingerprint_summary.html'):

    return render(request, template_name, {'request': request})