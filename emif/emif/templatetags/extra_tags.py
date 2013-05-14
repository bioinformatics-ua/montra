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
    
    objs = Questionnaire.objects.all()
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

