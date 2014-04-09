
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

import json 

from population_characteristics.conf_aggregations import *


from searchengine.search_indexes import * 



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
        _ca = ConfAggregations()
        
        # Get the aggregations 
        self.confs = _ca.get_main_settings()
        self.fingerprint_id = fingerprint_id 

        # Doing a pre-processing to become the aggregation task easier
        self.var_pre_process = []
        self.var_pre_process_dict = {}
        for c in self.confs:
            self.var_pre_process.append(c.var)
            self.var_pre_process_dict[c.var] = c

    """ Get the slug value (which going to fingerprint take that value)
    """
    def __get_slug_values(self, slug_name):
        solr = CoreEngine()
        # Get the results
        results = solr.search_fingerprint("fingerprint_id:" + self.fingerprint_id)
        for r in results:
            return r['slug_name']

    """ Get the value from 
    """
    def __get_tsv_values(self, name, var):
        
        # Go to mongodb and ask for the values or ask directly in the values 
        values = []
        for e in self.values:
            if self.values['Var'] == var:
                values.append(self.values['values'][name])
        return values 

    def __get_values(self, agregation_field, aggregation):
        if agregation_field.ttype =="solr":
            return self.__get_slug_values(agregation_field.name)
        elif agregation_field.ttype =="tsv":
            return self.__get_tsv_values(agregation_field.name, aggregation.var)

    # Agregate the entry 
    def __aggregate_entry(self, entry):
        if self.var_pre_process == entry.var: 
            # It is the type of we want to aggregate, so we need to do some calculations 
            pass
            # TODO implement the shit here 

        return entry

    # Loads the previous aggregations if required 
    def __load_previous_values_from_aggregation(self):
        return []

    """ Execute the aggregation""" 
    def run(self):
        
        
        # Load the previous aggregations, if required 
        new_values = self.__load_previous_values_from_aggregation()


        # Run all the values and aggregate them 
        for entry in self.values:
            # Now Let's execute the aggregator task
            new_entry = self.__aggregate_entry(entry)

        return new_values 
        
