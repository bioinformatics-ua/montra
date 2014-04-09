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

        a = Aggregation()

        a.var = "Observation time in a year"
        a.key = "Name3"
        a.value = None
        a.values = None

        af = AggregationField()
        af.ttype = "slug"
        af.name = "database_name_t"

        f1 = Filter()
        f1.name = 'Year'
        f1.key = 'Name1'
        f1.value = 'Value1'

        
        af1 = AggregationField()
        af1.ttype = "tsv"
        af1.filters = [f1]
        a.operation = Operation.SUM 

        a.aggregation_fields = [af, af1]


        result.append(a)

        return result

