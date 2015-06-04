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



        fy2 = Filter()
        fy2.name = 'Name1'
        fy2.key = 'Name1'
        fy2.value = 'YEAR'

        fy3 = Filter()
        fy3.name = 'Name2'
        fy3.key = 'Name2'
        fy3.value = ''


        fy4 = Filter()
        fy4.name = 'Value2'
        fy4.key = 'Value2'
        fy4.value = ''

        a.static_filters = [fy2, fy3, fy4 ]


        af = AggregationField()
        af.ttype = "slug"
        af.name = "database_name_t"
        af.key = "dbname"
        af.value = "dbname_value"



        af2 = AggregationField()

        af2.ttype = "tsv"
        af2.name = None
        af2.key = None
        af2.value = 'Gender'
        af2.exclusive = True


        a.aggregation_fields = [af, af2]
        #a.aggregation_fields = [af, af2]
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

        fy3 = Filter()
        fy3.name = 'Name2'
        fy3.key = 'Name2'
        fy3.value = 'AGE'


        a.static_filters = [fy2, fy3 ]

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

        fy3 = Filter()
        fy3.name = 'Name2'
        fy3.key = 'Name2'
        fy3.value = ''


        fy4 = Filter()
        fy4.name = 'Value2'
        fy4.key = 'Value2'
        fy4.value = ''

        a.static_filters = [fy2, fy3,fy4 ]

        af = AggregationField()
        af.ttype = "slug"
        af.name = "location_t"
        af.key = "location"
        af.value = "location_value"



        af2 = AggregationField()

        af2.ttype = "tsv"
        af2.name = None
        af2.key = None
        af2.value = 'Gender'
        af2.exclusive = True


        #a.aggregation_fields = [af, af1, af2]
        a.aggregation_fields = [af, af2]
        result.append(a)





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

        fy3 = Filter()
        fy3.name = 'Name2'
        fy3.key = 'Name2'
        fy3.value = ''


        fy4 = Filter()
        fy4.name = 'Value2'
        fy4.key = 'Value2'
        fy4.value = ''


        fy2 = Filter()
        fy2.name = 'Name1'
        fy2.key = 'Name1'
        fy2.value = 'YEAR'


        a.static_filters = [fy2, fy3, fy4 ]

        af2 = AggregationField()

        af2.ttype = "tsv"
        af2.name = None
        af2.key = None
        af2.value = 'Gender'
        af2.exclusive = True


        #a.aggregation_fields = [af, af1, af2]
        a.aggregation_fields = [af, af2]
        result.append(a)

        ### Active Patients per database (age groups)
        ###
        a = Aggregation()

        a.var = "Observation time in a year"
        a.operation = Operation.SUM
        a.field_to_compute = "Count"


        fy2 = Filter()
        fy2.name = 'Name1'
        fy2.key = 'Name1'
        fy2.value = 'YEAR'

        fy3 = Filter()
        fy3.name = 'Name2'
        fy3.key = 'Name2'
        fy3.value = 'AGE'

        a.static_filters = [fy3, fy2]

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



        a.aggregation_fields = [af, af1, af2, af3]
        result.append(a)


        ### Birth year per database
        ###
        a2 = Aggregation()

        a2.var = "Birth in year"
        a2.operation = Operation.SUM
        a2.field_to_compute = "Count"

        fy2 = Filter()
        fy2.name = 'Name1'
        fy2.key = 'Name1'
        fy2.value = 'YEAR'

        a2.static_filters = [fy2]

        af = AggregationField()
        af.ttype = "slug"
        af.name = "database_name_t"
        af.key = "dbname"
        af.value = "dbname_value"

        af2 = AggregationField()

        af2.ttype = "tsv"
        af2.name = None
        af2.key = None
        af2.value = 'Gender'
        af2.exclusive = True

        af1 = AggregationField()

        af1.ttype = "tsv"
        af1.name = 'YEAR'
        af1.key = 'Name1'
        af1.value = 'Value1'


        a2.aggregation_fields = [af, af2, af1]
        result.append(a2)

        ### Age at start of year
        ###
        a3 = Aggregation()

        a3.var = "Age at start of year"
        a3.operation = Operation.SUM
        a3.field_to_compute = "Count"


        fy2 = Filter()
        fy2.name = 'Name1'
        fy2.key = 'Name1'
        fy2.value = 'YEAR'

        fy3 = Filter()
        fy3.name = 'Name2'
        fy3.key = 'Name2'
        fy3.value = 'AGE'

        a3.static_filters = [fy2, fy3]

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



        a3.aggregation_fields = [af, af1, af2, af3]
        result.append(a3)

        ### All Patients per database
        ###
        a = Aggregation()

        a.var = "Age at patient start"
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

        fy3 = Filter()
        fy3.name = 'Name2'
        fy3.key = 'Name2'
        fy3.value = ''


        fy4 = Filter()
        fy4.name = 'Value2'
        fy4.key = 'Value2'
        fy4.value = ''


        fy2 = Filter()
        fy2.name = 'Name1'
        fy2.key = 'Name1'
        fy2.value = 'YEAR'


        a.static_filters = [fy2, fy3, fy4 ]

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

