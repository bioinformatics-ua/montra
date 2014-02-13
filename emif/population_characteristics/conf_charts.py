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

from population_characteristics.charts.chart import *


class ConfCharts(object):

    def __init__(self):
        # TODO 
        pass

    def read_settings_from_file(self):
        # TODO
        pass

    def get_main_settings(self):
        # It's hardcoded now 
        c = Chart()
        c.title = Title()
        c.title.operation = Operation.UNIQUE
        c.title.var = "Active patients" 
        c.x_axis = Axis()
        c.x_axis.operation = "unique"
        c.x_axis.var = "Name1"
        c.y_axis = Axis()
        c.y_axis.operation = "unique"
        c.y_axis.var = "Min"
        f1 = Filter()
        f1.name = 'Year'
        f1.var = 'Name1'

        f1 = Filter()
        f1.name = 'Gender'
        f1.var = 'Gender'

        c.filters = [f1]

        c1 = Chart()
        c1.title = Title()
        c1.title.operation = Operation.UNIQUE
        c1.title.var = "Birth in year" 
        c1.x_axis = Axis()
        c1.x_axis.operation = "unique"
        c1.x_axis.var = "Name1"
        c1.y_axis = Axis()
        c1.y_axis.operation = "unique"
        c1.y_axis.var = "Count"
        
        c1.filters = [f1]


        c2 = Chart()
        c2.title = Title()
        c2.title.operation = Operation.UNIQUE
        c2.title.var = "Age at patient start" 
        c2.x_axis = Axis()
        c2.x_axis.operation = "unique"
        c2.x_axis.var = "Name1"
        c2.y_axis = Axis()
        c2.y_axis.operation = "unique"
        c2.y_axis.var = "Count"
        
        c2.filters = [f1]


        c3 = Chart()
        c3.title = Title()
        c3.title.operation = Operation.UNIQUE
        c3.title.var = "Age at patient end" 
        c3.x_axis = Axis()
        c3.x_axis.operation = "unique"
        c3.x_axis.var = "Name1"
        c3.y_axis = Axis()
        c3.y_axis.operation = "unique"
        c3.y_axis.var = "Count"
        
        c3.filters = [f1]


        c4 = Chart()
        c4.title = Title()
        c4.title.operation = Operation.UNIQUE
        c4.title.var = "Age at patient end" 
        c4.x_axis = Axis()
        c4.x_axis.operation = "unique"
        c4.x_axis.var = "Name1"
        c4.y_axis = Axis()
        c4.y_axis.operation = "unique"
        c4.y_axis.var = "Count"
        
        c4.filters = [f1]


        c5 = Chart()
        c5.title = Title()
        c5.title.operation = Operation.UNIQUE
        c5.title.var = "Age at start of year" 
        c5.x_axis = Axis()
        c5.x_axis.operation = "unique"
        c5.x_axis.var = "Name1"
        c5.y_axis = Axis()
        c5.y_axis.operation = "unique"
        c5.y_axis.var = "Count"
        
        c5.filters = [f1]

        c6 = Chart()
        c6.title = Title()
        c6.title.operation = Operation.UNIQUE
        c6.title.var = "Observation time" 
        c6.x_axis = Axis()
        c6.x_axis.operation = "unique"
        c6.x_axis.var = "Name1"
        c6.y_axis = Axis()
        c6.y_axis.operation = "unique"
        c6.y_axis.var = "Count"
        
        c6.filters = [f1]

        c7 = Chart()
        c7.title = Title()
        c7.title.operation = Operation.UNIQUE
        c7.title.var = "Observation time before a year" 
        c7.x_axis = Axis()
        c7.x_axis.operation = "unique"
        c7.x_axis.var = "Name1"
        c7.y_axis = Axis()
        c7.y_axis.operation = "unique"
        c7.y_axis.var = "Count"
        
        c7.filters = [f1]

        c8 = Chart()
        c8.title = Title()
        c8.title.operation = Operation.UNIQUE
        c8.title.var = "Observation time after a year" 
        c8.x_axis = Axis()
        c8.x_axis.operation = "unique"
        c8.x_axis.var = "Name1"
        c8.y_axis = Axis()
        c8.y_axis.operation = "unique"
        c8.y_axis.var = "Count"
        
        c8.filters = [f1]


        c9 = Chart()
        c9.title = Title()
        c9.title.operation = Operation.UNIQUE
        c9.title.var = "Observation time in a year" 
        c9.x_axis = Axis()
        c9.x_axis.operation = "unique"
        c9.x_axis.var = "Name1"
        c9.y_axis = Axis()
        c9.y_axis.operation = "unique"
        c9.y_axis.var = "Count"
        
        c9.filters = [f1]


        print c.to_JSON()
        sc = SetCharst()

        sc.charts = [c,c1, c2, c3, c4, c5, c6, c7, c8, c9]
        sc.charts = [c,c1]

        return sc

