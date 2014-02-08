# -*- coding: utf-8 -*-
# Copyright (C) 2014 Luís A. Bastião Silva and Universidade de Aveiro
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

def get_settings(request, runcode):
    pc = PopulationCharacteristic(None)
    values = pc.get_settings()
    data = {'conf': values.to_JSON()}

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