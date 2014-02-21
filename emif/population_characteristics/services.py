# -*- coding: utf-8 -*-
# Copyright (C) 2013 Luís A. Bastião Silva and Universidade de Aveiro
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
        
from emif.settings import jerboa_collection
from pymongo.errors import OperationFailure
from .parseJerboaFile import * 
import json 

from .conf_charts import *
from .charts.rule_matcher import * 


class PopulationCharacteristic(object):
    """PopulationCharacteristic: This class controls the Jerboa File
    """
    def __init__(self, arg=None):
        
        self.arg = arg


    def last_activity(self):
        pass

    def __to_json(self):
        self._json = import_population_characteristics_data()

    def revisions(self):
        pass

    def submit_new_revision(self, fingerprint_id, path_file=None):
        
        #path_file = "C:/Users/lbastiao/Projects/TEST_DataProfile_v1.5.6b.txt"
        #path_file = "/Volumes/EXT1/Dropbox/MAPi-Dropbox/EMIF/Jerboa/TEST_DataProfile_v1.5.6b.txt"        
        self._json = import_population_characteristics_data(fingerprint_id, filename=path_file)
        #print self._json
        #f = open('jerboaTmp', 'w')
        #f.write(self._json)
        #f.close()
        json_data = json.loads(self._json)
        try:
            # Create MONGO record
            data_example = jerboa_collection.insert(json_data)
            # get last inserted record
            #print jerboa_collection.find_one()
            print "Sucess "
        except OperationFailure:
            print "Failure"

    def get_variables(self, var, row, fingerprint_id='abcd'):
        #db.jerboa_files.distinct( 'values.Var' )
        # Need to filter by Fingerprint, otherwise, we're trapped.
        print "get_variables"
        print "var: " + var
        print "row: " + row 
        print "fingerprint_id:" + fingerprint_id

        import pdb
        #pdb.set_trace() 
        vars_that_should_exists = ['Count']

        dict_query = {'fingerprint_id':fingerprint_id, 
            'values.Gender':'M',
            'values.Var': var}
        for ve in vars_that_should_exists:
            dict_query['values.'+ve] = { "$exists" : True }
        print dict_query
        values =  jerboa_collection.find(dict_query )
        #print values 
        #values =  jerboa_collection.find( {'fingerprint_id':'abcd', 
        #    'values.Var': 'Active patients', 
        #    'values.Count': { "$exists" : True }}  )

        
        #values = jerboa_collection.find( {'fingerprint_id':'abcd', 'values.Var': 'Active patients', 'values.Count': { "$exists" : True  }}  )
        results = []
        for v in values:
            print v
            results.append(v[u'values'])

        #print results
        return results

    def get_variables_filter(self, gender=None, name1=None, value1=None, name2=None,
        value2=None, var=None):
        #db.jerboa_files.distinct( 'values.Var' )
        values =  jerboa_collection.distinct( 'values.' +  param )
        return values


    def generic_filter(self, filters):
        
        json_acceptable_string = filters.replace("'", "\"")
        print json_acceptable_string
        d = json.loads(json_acceptable_string)
        print d
        values =  jerboa_collection.find(d)
        r = []
        for v in values:
            v = unicode(v)
            r.append(v);

        return r

    def filters(self, var, fingerprint_id):

        # Go to the rule matcher and ask for the filter for that particular case
        mrules = RuleMatcher()
        filters = mrules.get_filter(var)
        #_filter = charts_conf.
        
        # Should check if any special operation, for now, let's assume: NO!

        for _filter in filters:

            # Generate query
            dict_query = {'fingerprint_id':fingerprint_id, 
                'values.Var': var,
                
                }
            if _filter.key != None:
                dict_query['values.' + _filter.key]  = _filter.value
            
            values =  jerboa_collection.find( dict_query ).distinct('values.' + _filter.value )
            _filter.values = values
        return filters

    def get_var(self):
        values =  jerboa_collection.distinct( 'values.Var' )
        
        return values

    def get_x_y(self):
        pass
    
    def get_settings(self):
        cc = ConfCharts()
        return cc.get_main_settings()
