# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response


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
    