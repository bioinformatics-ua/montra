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

from emif.settings import jerboa_collection, jerboa_aggregation_collection
from pymongo.errors import OperationFailure
from .parseJerboaFile import *
import json

from .conf_charts import *
from .charts.rule_matcher import *

#import pdb


class PopulationCharacteristic(object):
    """PopulationCharacteristic: This class controls the Jerboa File
    """
    def __init__(self, arg=None, type=None):

        self.arg = arg
        self.type = type


    def last_activity(self):
        pass

    def __to_json(self):
        self._json = import_population_characteristics_data()

    def revisions(self):
        pass

    def submit_new_revision(self, user, fingerprint_id, revision, path_file=None):

        #path_file = "C:/Users/lbastiao/Projects/TEST_DataProfile_v1.5.6b.txt"
        #path_file = "/Volumes/EXT1/Dropbox/MAPi-Dropbox/EMIF/Jerboa/TEST_DataProfile_v1.5.6b.txt"
        self._json = import_population_characteristics_data(user, fingerprint_id, revision, filename=path_file)
        #print self._json
        #f = open('jerboaTmp', 'w')
        #f.write(self._json)
        #f.close()
        json_data = json.loads(self._json)
        try:
            if len(json_data) > 0:
                # Create MONGO record
                data_example = jerboa_collection.insert(json_data)
                # get last inserted record
                #print jerboa_collection.find_one()
                print "Success "
        except OperationFailure:
            print "Failure"
        return json_data


    def get_variables(self, var, row, fingerprint_id='abcd', revision='-1', filters=[], vars_that_should_exists=[]):
        #db.jerboa_files.distinct( 'values.Var' )
        # Need to filter by Fingerprint, otherwise, we're trapped.

        #pdb.set_trace()
        vars_that_should_exists = ['Count']

        mrules = RuleMatcher(type=Fingerprint.objects.get(fingerprint_hash=fingerprint_id).questionnaire.id)
        __filters = mrules.get_filter(var)
        c1 = mrules.get_chart(var)

        dict_query = {'fingerprint_id':fingerprint_id, 'revision': revision,
            'values.Var': c1.title.var}


        # Comparable
        #comparable = True
        #values_compare = ["M", "F"]

        for ve in vars_that_should_exists:
            dict_query['values.'+ve] = { "$exists" : True }

        for _f in c1.y_axis.static_filters:
            dict_query['values.'+_f.key] = _f.value

        #print "filters"
        #print filters
        # Apply filters in the query
        dict_query_general=[]



        for ve in filters:
            #print "ve"
            #print ve

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
        #print dict_query
        values =  jerboa_collection.find(dict_query )


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
                    #print values[_v]
            return values
        values_app = None
        for v in values:
            if c1.y_axis.transformation != None:
                try:
                    #print "transformation"
                    values_app = transform(c1.y_axis.var, c1.y_axis.transformation,v[u'values'])
                    #y = float(v[u'values'][c1.y_axis.var])
                    #new_y = eval(c1.y_axis.transformation)
                    #v[u'values'][c1.y_axis.var] = new_y
                    v[u'values'] = values_app
                    #print values_app
                except:
                    #raise
                    print "bastard x error %s, %s " % (c1.y_axis.var, str(v[u'values']))
            results.append(v[u'values'])

        vorder = c1.x_axis.var
        if c1.x_axis.sort_func!=None:
            vorder = c1.x_axis.var
            results = sorted(results, key=lambda k: eval(c1.x_axis.sort_func))
        return results

    def get_variables_filter(self, gender=None, name1=None, value1=None, name2=None,
        value2=None, var=None):
        #db.jerboa_files.distinct( 'values.Var' )
        values =  jerboa_collection.distinct( 'values.' +  param )
        return values


    def generic_filter(self, filters):

        json_acceptable_string = filters.replace("'", "\"")
        #print json_acceptable_string
        d = json.loads(json_acceptable_string)
        #print d
        values =  jerboa_collection.find(d)
        r = []
        for v in values:
            v = unicode(v)
            r.append(v);

        return r




    def filters(self, var, fingerprint_id):

        # Go to the rule matcher and ask for the filter for that particular case
        comp = False
        if fingerprint_id=="COMPARE":
            comp=True
        mrules = RuleMatcher(comp=comp)
        filters = mrules.get_filter(var)
        chart = mrules.get_chart(var)
        #_filter = charts_conf.

        # Should check if any special operation, for now, let's assume: NO!

        for _filter in filters:

            # Generate query

            dict_query = {'fingerprint_id':fingerprint_id,
                'values.Var': chart.title.var,

                }
            if comp:
                dict_query = {'values.Var': chart.title.var,}
            if _filter.key != None:
                dict_query['values.' + _filter.key]  = _filter.name
            #print _filter
            #print _filter.value
            #print dict_query
            if comp:
                print dict_query
                print 'values.' + _filter.value
                values =  jerboa_aggregation_collection.find( dict_query ).distinct('values.' + _filter.value )#
            else:
                values =  jerboa_collection.find( dict_query ).distinct('values.' + _filter.value )#

            values = sorted(values)

            #values =  jerboa_collection.find( dict_query ).distinct('values.' + _filter.value )
            #print values
            _filter.values = values
        return filters

    def get_var(self):
        values =  jerboa_collection.distinct( 'values.Var' )
        # Go to the rule matcher and ask for the filter for that particular case
        comp = False
        if fingerprint_id=="COMPARE":
            comp=True
        mrules = RuleMatcher(comp=comp)
        filters = mrules.get_filter(var)
        chart = mrules.get_chart(var)


        # Generate the filters here.
        for _filter in filters:

            # Generate query

            dict_query = {'fingerprint_id':fingerprint_id,
                'values.Var': chart.title.var,

                }
            if comp:
                dict_query = {'values.Var': chart.title.var,}
            if _filter.key != None:
                dict_query['values.' + _filter.key]  = _filter.name


        if comp:
            values =  jerboa_aggregation_collection.find( dict_query ).distinct('values.' + _filter.value )#
        else:
            values =  jerboa_collection.find( dict_query ).distinct('values.' + _filter.value )#

        values = sorted(values)

        _filter.values = values


        return filters
        return values

    def get_xs(self):
        pass

    def get_x_y(self):
        pass

    def get_settings(self):
        cc = ConfCharts()
        return cc.get_main_settings(type=self.type)
