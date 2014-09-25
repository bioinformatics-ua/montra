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

from emif.settings import jerboa_collection, jerboa_aggregation_collection
from pymongo.errors import OperationFailure
from .parseJerboaFile import * 
import json 

from .conf_charts import *
from .charts.rule_matcher import * 

import json

from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, ListView

from .response import JSONResponse, response_mimetype
from .serialize import serialize
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required

from emif.views import createqsets, createqset, get_api_info, merge_highlight_results
from django.shortcuts import render

import os

from django.conf import settings

from .parseJerboaFile import * 
from .services import * 
from docs_manager.storage_handler import *
from population_characteristics.models import *

from docs_manager.views import get_revision


"""
This code is only made to the comparison between databases
"""

def handle_compare(request, template_name="compare_populations.html"):

    filters = []
    fingerprint_ids = []

    if request.POST:
        # Get the filters to apply.
        
        filters = {}
        print request.POST
        myRq = dict(request.POST.lists())
        for i in myRq:
            if "chks_" in i:
                fingerprint_ids.append(i.replace("chks_", ""))
                continue
            filters[i[0:-2]] = myRq[i]

        
        print "Filters" + str(filters)
        
        
        

    cp = ComparisonPopulation(None)
    # Only hard coded for testing 
    #fingerprint_ids = ["66a47f694ffb676bf7676dfde24900e6", "3dc3d622130eac4d092786afb9a0ec76", "2e303fd12bc5e5fd03a54651dd8d6334"]
    var = "Active patients"
    row = "Count"
    print cp.get_variables(var, row, fingerprints_id=fingerprint_ids, filters=filters)

    return render(request, template_name, {'request': request,  
        'owner_fingerprint':False,
        'compare': True,
        'fingerprint_ids' : fingerprint_ids,
        'contains_population': True }) 


def handle_compare_values(request, var, row, fingerprint_id, revision, template_name="compare_populations.html"):

    filters = []
    fingerprint_ids = []
    if request.POST:
        # Get the filters to apply.
        
        filters = {}
        #print request.POST
        myRq = dict(request.POST.lists())
        
        for i in myRq:
            if i == 'publickey':
                continue

            #if "chks_" in i:
            #    fingerprint_ids.append(i.replace("chks_", ""))
            #    continue
            if "fingerprint_i" in i:
                fingerprints_transf = request.POST[i].replace("\n", "")
                fps = fingerprints_transf.split(" ")
                for fp in fps:
                    fingerprint_ids.append(fp)
                continue
            filters[i[8:-3]] = myRq[i]


        print "----"
        print "var:"+var
        print "row:"+row
        print "Filters" + str(filters)
        print fingerprint_ids
        print "----"

    cp = ComparisonPopulation(None)
    # Only hard coded for testing 
    #fingerprint_ids = ["66a47f694ffb676bf7676dfde24900e6", "3dc3d622130eac4d092786afb9a0ec76", "2e303fd12bc5e5fd03a54651dd8d6334"]
    
    values = cp.get_variables(var, row, fingerprints_id=fingerprint_ids, filters=filters, revision=revision)
    data = {'values': values}
    response = JSONResponse(data, mimetype="application/json")
    response['Content-Disposition'] = 'inline; filename=files.json'
    return response

def get_compare_settings(request):

    cc = ConfCharts()
    values = cc.get_compare_settings()

    data = {'conf': values.to_JSON()}

    response = JSONResponse(data, mimetype=response_mimetype(request))
    response['Content-Disposition'] = 'inline; filename=files.json'
    return response

class ComparisonPopulation(object):
    """PopulationCharacteristic: This class controls the Jerboa File
    """
    def __init__(self, arg=None):
        
        self.arg = arg

    # Get the list of fingerprints
    def __fingerprints_to_mongo_query(self, fingerprints_id):
        filter_fp = []
        for fid in fingerprints_id:
            if fid != None and len(fid) > 0:
                _filter_fp = {"fingerprint_id": fid}
                

                revision = '-1'
                try:
                    latest_jerboa = Characteristic.objects.filter(fingerprint_id=fid).order_by('-latest_date')[0]
                    revision = latest_jerboa.revision
                except:
                    print "-- Error retrieving last revision for fingerprint "+str(fid)

                _filter_fp['revision'] = revision

                filter_fp.append(_filter_fp)

        return filter_fp



    def get_variables(self, var, row, fingerprints_id=[], filters=[], revision=-1, vars_that_should_exists=[]):
        
        # Sometimes there are rude files. According to Marius (from Erasmus MC)
        # This variable should exist always.
        vars_that_should_exists = ['Count']

        # Get the Rule Matcher 
        mrules = RuleMatcher( comp=True)
        __filters = mrules.get_filter(var)

        c1 = mrules.get_chart(var)

        dict_query = {'$or': self.__fingerprints_to_mongo_query(fingerprints_id), 
            'values.Var': c1.title.var}

        
        for ve in vars_that_should_exists:
            dict_query['values.'+ve] = { "$exists" : True }

        for _f in c1.y_axis.static_filters:
            dict_query['values.'+_f.key] = _f.value

        #print "filters"
        #print filters
        # Apply filters in the query 
        dict_query_general=[]
        
        for ve in filters:
            
            if  isinstance(filters[ve], list):
                #if not "$or" in dict_query:
                _or_dict_query = {}
                _or_dict_query["$or"] = [ ]
                for _aux in filters[ve]:
                    _or_dict_query2 = {ve: _aux}
                    _or_dict_query["$or"].append(_or_dict_query2)
                dict_query_general.append(_or_dict_query)    
            else:
                dict_query[ve] = filters[ve]
                
                
        if dict_query_general != []:
            dict_query["$and"]= dict_query_general
        print dict_query
        values =  jerboa_aggregation_collection.find(dict_query )
        

        results = []

        def transform(v, transformation, values):
            if not type(v) is list:

                y = float(values[v])
                new_y = eval(transformation)
                values[v] = new_y
            else:
                for _v in v:
                    y = float(values[_v])
                    new_y = eval(transformation)
                    values[_v] = new_y
                    print values[_v]
            return values
        values_app = None
        for v in values:


            if c1.y_axis.transformation != None:
                try:
                    values_app = transform(c1.y_axis.var, c1.y_axis.transformation,v[u'values'])
                    #y = float(v[u'values'][c1.y_axis.var])
                    #new_y = eval(c1.y_axis.transformation)
                    #v[u'values'][c1.y_axis.var] = new_y
                    v[u'values'] = values_app

                except:
                    print "bastard x error %s, %s " % (c1.y_axis.var, str(v[u'values']))
            v[u'values']['fingerprint_id'] = v[u'fingerprint_id']
            results.append(v[u'values'])

        vorder = c1.x_axis.var
        if c1.x_axis.sort_func!=None:
            vorder = c1.x_axis.var
            results = sorted(results, key=lambda k: eval(c1.x_axis.sort_func))
        return results
