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

from bson.objectid import ObjectId
from emif.settings import jerboa_collection, jerboa_aggregation_collection
from pymongo.errors import OperationFailure
import copy
import json
import pprint

from population_characteristics.conf_aggregations import *


from searchengine.search_indexes import *
import itertools
from sets import Set


# Aux functions
def verify_if_combination_matches_aggregation_field(comb, aggr, entry):
    result = False
    k = 0
    for af in aggr.aggregation_fields:

        if af.ttype == "tsv":
            #print "entry " + entry['values'][af.value]
            #print "combo " + comb[k]
            if entry['values'][af.value] == comb[k] and not result:
                result = True
            else:
                result = False

        k = k + 1
    return result



"""
This class do the aggregations from data comming from Jerboa
Marius and Peter from Erasmus MC has developed an R script to perform this task
This class will a translation of their script
This will be a task asynchonous executed through the celery (background tasks)
to scale the solution
"""

class AggregationPopulationCharacteristics(object):
    """
    @param values data parsed comming from Jerboa
    """
    def __init__(self, values, fingerprint_id, revision=None):
        self.values = values
        #print self.values
        _ca = ConfAggregations()
        #print _ca
        # Get the aggregations
        self.confs = _ca.get_main_settings()
        self.fingerprint_id = fingerprint_id

        # Doing a pre-processing to become the aggregation task easier
        self.var_pre_process_dict = {}
        #print self.confs
        for c in self.confs:

            if c.var in self.var_pre_process_dict:
                self.var_pre_process_dict[c.var].append(c)
            else:
                self.var_pre_process_dict[c.var] = [c]

        self.index_new_values = {}

    """ Get the slug value (which going to fingerprint take that value)
    """
    def __get_slug_values(self, slug_name):
        solr = CoreEngine()
        # Get the results
        results = solr.search_fingerprint("id:" + self.fingerprint_id)
        r = "None"
        for r in results:
            try:
                r =[r[slug_name]]
            except:
                r = "None"
            break
        return r

    """ Get the value from
    """
    def __get_tsv_values(self, name, var):

        # Go to mongodb and ask for the values or ask directly in the values
        values = Set([])

        for e in self.values:

            if e['values']['Var'] == var:
                values.add(e['values'][name])
            #else:
                #print e['values'][name]
                #print e['values']['Var']
        return list(values)

    def __get_values(self, agregation_field, aggregation):
        # TODO: this process can be cached!
        # Optimization++
        if agregation_field.ttype =="slug":
            agregation_field.values = self.__get_slug_values(agregation_field.name)
            return agregation_field.values
        elif agregation_field.ttype =="tsv":
            agregation_field.values = self.__get_tsv_values(agregation_field.value, aggregation.var)
            return agregation_field.values


    def __verify_static_filters(self, entry, agg):
        result = True

        # If it does not have filters, it pass this condition.
        if agg.static_filters == None or agg.static_filters == []:
            return result

        # If it is have filter, we need to check if the fields
        # matches the criterias
        for f in agg.static_filters:
            if entry['values'][f.key] != f.value:
                return False
        return result
    # Agregate the entry
    def __aggregate_entry(self, entry):
        try:

            if entry['values']['Var'] in self.var_pre_process_dict:
                # It is the type of we want to aggregate, so we need to do some calculations
                for aggregation in self.var_pre_process_dict[entry['values']['Var']]:
                    # Get Aggregation Field

                    # verify if it has operations
                    has_operations = self.__verify_static_filters(entry, aggregation)

                    arr_values = []
                    for af in aggregation.aggregation_fields:
                        if (af.values==None):
                            value = self.__get_values(af, aggregation)
                            af.values = value

                        arr_values.append(af.values)
                    if arr_values!=[]:
                        for combination in itertools.product(*arr_values, repeat=1):

                            # Discard combination
                            if not verify_if_combination_matches_aggregation_field(combination, aggregation, entry):
                                continue

                            #print (entry['values']['Var'],combination )

                            if (entry['values']['Var'],combination) in self.index_new_values:
                                _entry = self.index_new_values[(entry['values']['Var'],combination)]
                                # TODO: Check the operation
                                # For now, only sums

                                _entry['values'][aggregation.field_to_compute] = float(_entry['values'][aggregation.field_to_compute])  +  float(entry['values'][aggregation.field_to_compute])

                            else:

                                _entry = copy.deepcopy(entry)
                                if has_operations:
                                    _entry['values']['Name1'] = ''
                                    _entry['values']['Name2'] = ''
                                    _entry['values']['Value1'] = ''
                                    _entry['values']['Value2'] = ''

                                _entry['values'][aggregation.field_to_compute] = _entry['values'][aggregation.field_to_compute]
                                i = 0
                                for af in aggregation.aggregation_fields:

                                    if af.ttype == "slug":
                                        _entry['values'][af.value] = combination[i]
                                        _entry['values'][af.key] = af.key
                                    elif af.ttype == "tsv":

                                        _entry['values'][af.value] = str(combination[i])
                                        if (af.key!=None) and _entry['values'][af.value] != '':
                                            # Should works, why not?
                                            #_entry['values'][af.key] = entry['values'][af.name]
                                            _entry['values'][af.key] = af.name
                                    else:
                                        raise "Error, type is not defined"
                                    i = i + 1

                                self.index_new_values[(entry['values']['Var'],combination)] = _entry
                                self.new_values.append(_entry)

                    #print "end combination"
            #else:
                #print "no"

        except:
            print "Exception!!!!!!!"
            import traceback
            traceback.print_exc()


    # Loads the previous aggregations if required
    def __load_previous_values_from_aggregation(self):
        return []

    """ Execute the aggregation"""
    def run(self):

        # Load the previous aggregations, if required
        self.new_values = self.__load_previous_values_from_aggregation()

        # Run all the values and aggregate them
        for entry in self.values:
            #print "entry"
            #print entry
            # Now Let's execute the aggregator task
            #print "self.__aggregate_entry(entry)"
            self.__aggregate_entry(entry)

        try:
            #Create MONGO record
            #print "Create MONGO record"
            for doc in self.new_values:
                # Workaround to put it working
                doc['_id'] = ObjectId()
                jerboa_aggregation_collection.insert(doc)

            print "Sucess "
            #print self.index_new_values.keys()
        except OperationFailure as e:
            print "Failure"
            print e
            import traceback
            traceback.print_exc()
        print "finishing aggregation"
        #pprint.pprint(self.index_new_values)
        return self.new_values

