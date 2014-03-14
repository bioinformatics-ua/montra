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

json.dumps = simplejson.dumps

"""
The goal of this class is to generate the configurations files/templates
for the charts library
"""


class Operation:
    SUM = 'sum'
    UNIQUE = 'unique'
    LIST = 'list'
    MIN = 'min'
    MAX = 'max'
    COUNT = 'count'
    MEAN = 'mean'
    PERC25 = 'Perc25'
    PERC75 = 'Perc75'
    SD = 'SD'
    CONCAT = 'concat'

class Scale(object):
    def __init__(self):
        self.unit = None
        self.bins = None
        self.start = 0
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Filter(object):
    def __init__(self):
        self.name = None
        self.key = None
        self.value = None
        self.values = None
        self.translation = None
        self.comparable = False
        self.comparable_values = None

        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Title(object):
    def __init__(self):
        self.fixed_title = 'None'
        self.operation = None
        self.var = None
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Axis(object):
    def __init__(self):
        self.operation = None
        self.var = None
        self.scale = None
        self.filters = None
        self.static_filters = []
        self.categorized = False
        self.multivalue = False
        self.transformation = None
        self.sort_func = None
        self.label = None
        self.legend = False
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Chart(object):
    def __init__(self):
        self.title = None
        self.x_axis = None
        self.y_axis = None
        self.filters = None

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
class SetCharst(object):
    def __init__(self):
        self.charts = None
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)



# Active patients
# Birth in year
# Age at patient start
# Age at patient end
# Age at start of year
# Observation time
# Observation time before a year
# Observation time after a year
# Observation time in a year

### Active patients  
c = Chart()
c.title = Title()
c.title.operation = Operation.UNIQUE
c.title.var = "Var" 
c.x_axis = Axis()
c.x_axis.operation = "unique"
c.x_axis.var = "Name1"
c.y_axis = Axis()
c.y_axis.operation = "unique"
c.y_axis.var = "Count"
f1 = Filter()
f1.name = 'Year'
f1.var = 'Name1'

f1 = Filter()
f1.name = 'Age'
f1.var = 'Name2'

c.filters = [f1]

print c.to_JSON()
sc = SetCharst()
sc.charts = [c,c]
print sc.to_JSON()


### Age starts at 
c = Chart()
c.title = Title()
c.title.operation = Operation.UNIQUE
c.title.var = "Var" 
c.x_axis = Axis()
c.x_axis.operation = "unique"
c.x_axis.var = "Name1"
c.y_axis = Axis()
c.y_axis.operation = "unique"
c.y_axis.var = "Count"
f1 = Filter()
f1.name = 'Sex'
f1.var = 'Name2'
c.filters = [f1]

print c.to_JSON()

c = Chart()
c.title = Title()
c.title.operation = Operation.UNIQUE
c.title.var = "Var" 
c.x_axis = Axis()
c.x_axis.operation = "unique"
c.x_axis.var = "Name1"
c.y_axis = Axis()
c.y_axis.operation = "unique"
c.y_axis.var = "Count"
f1 = Filter()
f1.name = 'Sex'
f1.var = 'Name2'
c.filters = [f1]