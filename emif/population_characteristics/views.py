# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response

from .services import *

from .response import JSONResponse, response_mimetype
from .serialize import serialize
    

def jerboa_list_values(request, param, template_name='documents_upload_form.html'):

    pc = PopulationCharacteristic(None)
    values = pc.get_variables(param)
    data = {'values': values}
    response = JSONResponse(data, mimetype="application/json")
    response['Content-Disposition'] = 'inline; filename=files.json'
    return response


def generic_filter(request, param, template_name='documents_upload_form.html'):

    pc = PopulationCharacteristic(None)
    values = pc.generic_filter(param)
    data = {'values': values}
    response = JSONResponse(data, mimetype=response_mimetype(request))
    response['Content-Disposition'] = 'inline; filename=files.json'
    return response

def get_pde_types(self):
    """This function returns the Primary Data Extract type of graphs
    """




def population(request, template_name='piechart.html'):

    xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries", "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
    ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]
    chartdata = {'x': xdata, 'y': ydata}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': False,
            'jquery_on_ready': False,
        }
    }
    return render_to_response('charts.html', data)

def upload_jerboa_request(request, template_name='uploadjerboa.html'):
    """
    This functions is responsabible to handle the upload files of jerboa 
    """
    pass