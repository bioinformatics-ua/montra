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
        c.y_axis.var = "Count"
        f1 = Filter()
        f1.name = 'Year'
        f1.var = 'Name1'

        f1 = Filter()
        f1.name = 'Age'
        f1.var = 'Name2'

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

        print c.to_JSON()
        sc = SetCharst()
        sc.charts = [c,c1]

        return sc

