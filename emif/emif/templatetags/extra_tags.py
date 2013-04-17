from django import template
from django.template.defaultfilters import stringfilter

from questionnaire.models import Questionnaire

register = template.Library()

@register.filter(name='removeh1')
@stringfilter
def removeh1(value):
    return value.replace('h1. ','')


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
