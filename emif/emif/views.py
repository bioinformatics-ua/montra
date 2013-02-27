from django.http import HttpResponse
from django.template.response import TemplateResponse


def index(request, template='index.html'):
    return TemplateResponse(request, template, {})
