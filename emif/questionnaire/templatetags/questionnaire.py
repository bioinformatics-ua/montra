#!/usr/bin/python
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

from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

register = template.Library()


@register.filter(name="dictget")
def dictget(thedict, key):
    "{{ dictionary|dictget:variableholdingkey }}"
    return thedict.get(key, None)


@register.filter(name="spanclass")
def spanclass(string):
    l = 2 + len(string.strip()) // 6
    if l <= 4:
        return "span-4"
    if l <= 7:
        return "span-7"
    if l < 10:
        return "span-10"
    return "span-%d" % l

@register.filter(name="qtesturl")
def qtesturl(question):
    qset = question.questionset

    return "/admin/questionnaire/questionset/"+str(qset.id)+"/"

    '''
        This reverse stopped worked for some reason, we are keeping the url manually
        but will have to take a look at this with more time at a later date.

    return reverse("admin:questionset",
        args=("test:%s" % qset.questionnaire.id,
         qset.sortid))
    '''

@register.filter(name="rangeleft")
def rangeleft(value):
    returnable = None

    if value.startwith('[') and value.endwith(']'):
        value = value.replace('[', '')
        value = value.replace(']', '')

        broken = value.split(" TO ")

        if len(broken) == 2:
            returnable=broken[0].trim()

    return returnable

@register.filter(name="rangeright")
def rangeright(value):
    returnable = None

    if value.startwith('[') and value.endwith(']'):
        value = value.replace('[', '')
        value = value.replace(']', '')

        broken = value.split("TO")

        if len(broken) == 2:
            returnable=broken[1].trim()

    return returnable
