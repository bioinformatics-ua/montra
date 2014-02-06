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

class Operation:
    SUM = 'sum'
    UNIQUE = 'unique'


class Scale(object):
    def __init__(self):
        self.fixed_title = 'None'
        self.operation = None
        self.var = None
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Filter(object):
    def __init__(self):
        self.fixed_title = 'None'
        self.operation = None
        self.var = None
        
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



### Age starts at 
c = Chart()
c.title = Title()
c.title.operation = Operation.UNIQUE
c.title.var = "Var" 
c.x_axis = Axis()
c.x_axis.operation = "unique"
c.x_axis.var = "Age"
c.y_axis = Axis()
c.y_axis.operation = "unique"
c.y_axis.var = "Age"

print c.to_JSON()