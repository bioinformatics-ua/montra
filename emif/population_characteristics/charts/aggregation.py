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

import json

from django.utils import simplejson
from population_characteristics.charts.operations import * 


json.dumps = simplejson.dumps

"""
The goal of this class is to generate the configurations files/templates
for the charts library@aggretaion level
"""

class AggregationField:
    def __init__(self):
        self.ttype = "slug" # slug or tsv
        self.name = None # columns of tsv or name of slug
        self.filters = []
        self.operation = None # choose one of the operations 
        self.key = None
        self.transformation = None

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Aggregation(object):
    def __init__(self):

        self.var = None
        self.key = None
        self.value = None
        self.values = None
        self.translation = None
        self.filters = None
        self.static_filters = None 
        self.aggregation_fields = None 
        self.operation = None # choose one of the operations 
        

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
