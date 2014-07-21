#!/usr/bin/python

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
