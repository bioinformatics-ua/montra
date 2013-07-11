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
#
from django import template
from django.template.defaultfilters import stringfilter

from questionnaire.models import Questionnaire

register = template.Library()

@register.filter(name='removeh1')
@stringfilter
def removeh1(value):
    
    return value.replace('h1. ','')

@register.filter(name='removespaces')
@stringfilter
def removespaces(value):
    value = value.replace('h1. ','')
    value = value.replace(',','')
    result = value.replace(' ','')

    return result

def fingerprints_list():

    objs = Questionnaire.objects.all()
    results = {}
    for q in objs:
        results[q.id] = q.name
    print results

    return results

def fingerprints_list():
    
    objs = Questionnaire.objects.filter(disable=False)
    results = {}
    for q in objs:
        results[q.id] = q.name
    print results

    return results


def show_fingerprints():
    
    return {'fingerprints':fingerprints_list()}
register.inclusion_tag('menu_ttags.html')(show_fingerprints)


def show_fingerprints_for_search():
    
    return {'fingerprints':fingerprints_list()}
register.inclusion_tag('menu_ttags_for_search.html')(show_fingerprints_for_search)


def show_fingerprints_for_statistics():

    return {'fingerprints':fingerprints_list()}
register.inclusion_tag('menu_ttags_for_statistics.html')(show_fingerprints_for_statistics)
