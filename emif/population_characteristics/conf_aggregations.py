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

from population_characteristics.charts.operations import * 
from population_characteristics.charts.aggregation import *


class ConfAggregations(object):

    def __init__(self):
        # TODO 
        pass

    def read_settings_from_file(self):
        # TODO
        pass

    """ get the default settings to load 
    """
    
    def get_main_settings(self):

        result = []



        ### Overall Patient time per database 
        ###
        a = Aggregation()

        a.var = "Observation time in a year"
        a.operation = Operation.SUM 
        a.field_to_compute = "Count"

        af = AggregationField()
        af.ttype = "slug"
        af.name = "database_name_t"
        af.key = "dbname"
        af.value = "dbname_value"

        af1 = AggregationField()

        af1.ttype = "tsv"
        af1.name = 'YEAR'
        af1.key = 'Name1'
        af1.value = 'Value1'


        fy2 = Filter()
        fy2.name = 'Name1'
        fy2.key = 'Name1'
        fy2.value = 'YEAR'

        a.static_filters = [fy2 ]

        af2 = AggregationField()

        af2.ttype = "tsv"
        af2.name = None
        af2.key = None
        af2.value = 'Gender'
        af2.exclusive = True


        #a.aggregation_fields = [af, af1, af2]
        a.aggregation_fields = [af, af2]
        result.append(a)


        ### Overall Patient time per database (age groups) 
        ###
        a = Aggregation()

        a.var = "Observation time in a year"
        a.operation = Operation.SUM 
        a.field_to_compute = "Count"


        fy2 = Filter()
        fy2.name = 'Name1'
        fy2.key = 'Name1'
        fy2.value = 'YEAR'

        a.static_filters = [fy2 ]

        af = AggregationField()
        af.ttype = "slug"
        af.name = "database_name_t"
        af.key = "dbname"
        af.value = "dbname_value"

        af1 = AggregationField()

        af1.ttype = "tsv"
        af1.name = 'YEAR'
        af1.key = 'Name1'
        af1.value = 'Value1'



        af2 = AggregationField()

        af2.ttype = "tsv"
        af2.name = None
        af2.key = None
        af2.value = 'Gender'
        af2.exclusive = True

        af3 = AggregationField()

        af3.ttype = "tsv"
        af3.name = 'AGE'
        af3.key = 'Name2'
        af3.value = 'Value2'

        #a.aggregation_fields = [af, af1, af2]
        a.aggregation_fields = [af, af1, af2, af3]
        #result.append(a)




        ### Overall Patient time per Location  
        ###

        a = Aggregation()

        a.var = "Observation time in a year"
        a.operation = Operation.SUM 
        a.field_to_compute = "Count"



        fy2 = Filter()
        fy2.name = 'Name1'
        fy2.key = 'Name1'
        fy2.value = 'YEAR'

        a.static_filters = [fy2 ]

        af = AggregationField()
        af.ttype = "slug"
        af.name = "location_t"
        af.key = "location"
        af.value = "location_value"

        af1 = AggregationField()

        af1.ttype = "tsv"
        af1.name = 'YEAR'
        af1.key = 'Name1'
        af1.value = 'Value1'


        af2 = AggregationField()

        af2.ttype = "tsv"
        af2.name = None
        af2.key = None
        af2.value = 'Gender'
        af2.exclusive = True


        #a.aggregation_fields = [af, af1, af2]
        a.aggregation_fields = [af, af2]
        result.append(a)


        ### Overall Patient time per Location (in a) 
        ###

        a1 = Aggregation()
        a1.var = "Observation time in a year"
        a1.operation = Operation.SUM 
        a1.field_to_compute = "Count"

        af = AggregationField()
        af.ttype = "slug"
        af.name = "database_name_t"
        af.key = "dbname"
        af.value = "dbname_value"

        af1 = AggregationField()

        af1.ttype = "tsv"
        af1.name = 'YEAR'
        af1.key = 'Name1'
        af1.value = 'Value1'



        af2 = AggregationField()

        af2.ttype = "tsv"
        af2.name = None
        af2.key = None
        af2.value = 'Gender'
        af2.exclusive = True


        a1.aggregation_fields = [af, af1, af2]


        result.append(a1)


        ### Active Patients per database 
        ###
        a = Aggregation()

        a.var = "Active patients"
        a.operation = Operation.SUM 
        a.field_to_compute = "Count"

        af = AggregationField()
        af.ttype = "slug"
        af.name = "database_name_t"
        af.key = "dbname"
        af.value = "dbname_value"

        af1 = AggregationField()

        af1.ttype = "tsv"
        af1.name = 'YEAR'
        af1.key = 'Name1'
        af1.value = 'Value1'


        fy2 = Filter()
        fy2.name = 'Name1'
        fy2.key = 'Name1'
        fy2.value = 'YEAR'

        a.static_filters = [fy2 ]

        af2 = AggregationField()

        af2.ttype = "tsv"
        af2.name = None
        af2.key = None
        af2.value = 'Gender'
        af2.exclusive = True


        #a.aggregation_fields = [af, af1, af2]
        a.aggregation_fields = [af, af2]
        result.append(a)


        return result

