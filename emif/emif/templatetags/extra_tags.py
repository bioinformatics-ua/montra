from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='removeh1')
@stringfilter
def removeh1(value):
    return value.replace('h1. ','')


register.filter('removeh1', removeh1)
