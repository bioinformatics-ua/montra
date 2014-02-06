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

from .jerboa import *

class PopulationCharacteristic(JerboaFormat):
    """PopulationCharacteristic: This class controls the Jerboa File
    """
    def __init__(self, arg=None):
        super(PopulationCharacteristic, self).__init__(arg)
        self.arg = arg
    
    def last_activity(self):
        pass

    def __to_json(self):
        self._json = import_population_characteristics_data()

    def revisions(self):
        pass

    def submit_new_revision(self):
        path_file = "C:/Users/lbastiao/Projects/TEST_DataProfile_v1.5.6b.txt"
        
        self._json = import_population_characteristics_data(filename=path_file)
        #print self._json
        f = open('jerboaTmp', 'w')
        f.write(self._json)
        f.close()
        json_data = json.loads(self._json)
        try:
            # Create MONGO record
            data_example = jerboa_collection.insert(json_data)
            # get last inserted record
            print jerboa_collection.find_one()
            print "Sucess "
        except OperationFailure:
            print "Failure"

    def get_variables(self, param):
        #db.jerboa_files.distinct( 'values.Var' )
        values =  jerboa_collection.distinct( 'values.' +  param )
        return values

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



    def get_var(self):
        #db.jerboa_files.distinct( 'values.Var' )
        values =  jerboa_collection.distinct( 'values.Var' )
        
        return values

    def get_x_y(self):
        # 
        # 
        # db.jerboa_files.find({"values.Name1": "YEAR", "values.Var":"Active patients"})
        pass
        