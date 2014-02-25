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
        



        sc = SetCharst()

        sc.charts = []

        #################################################
        ### Active patients
        #################################################
        c = Chart()
        c.title = Title()
        c.title.operation = Operation.UNIQUE
        c.title.var = "Active patients" 
        c.title.fixed_title = "Active patients" 
        c.x_axis = Axis()
        c.x_axis.operation = "unique"
        c.x_axis.var = "Value1"
        c.y_axis = Axis()
        c.y_axis.operation = "unique"
        c.y_axis.var = "Count"
        f1 = Filter()
        f1.name = 'Year'
        f1.key = 'Name1'
        f1.value = 'Value1'

        f2 = Filter()
        f2.name = 'Gender'
        f2.key = None
        f2.value = 'Gender'

        ss = Scale()
        ss.unit = "Year"
        ss.bins = "10"

        c.filters = [f2]

        sc.charts.append(c)


        #################################################
        ### Birth date
        #################################################

        c1 = Chart()
        c1.title = Title()
        c1.title.operation = Operation.UNIQUE
        c1.title.var = "Birth in year" 
        c1.title.fixed_title = "Birth date"
        
        c1.x_axis = Axis()
        c1.x_axis.operation = "unique"
        c1.x_axis.var = "Value1"
        c1.y_axis = Axis()
        c1.y_axis.operation = "unique"
        c1.y_axis.var = "Count"
        
        c1.filters = [f2]


        c2 = Chart()
        c2.title = Title()
        c2.title.operation = Operation.UNIQUE
        c2.title.var = "Age at patient start" 
        c2.title.fixed_title = "Age at patient start" 
        
        # X AXIS 
        c2.x_axis = Axis()
        c2.x_axis.operation = "unique"
        c2.x_axis.var = "Value2"
        c2.x_axis.categorized = True
        c2_filters_x = Filter()
        c2_filters_x.name = 'AGE'
        c2_filters_x.key = 'Name2'
        c2_filters_x.value = 'Value2'
        c2.x_axis.filters = [c2_filters_x]

        c2.y_axis = Axis()
        c2.y_axis.operation = "unique"
        c2.y_axis.var = "Count"
        f_year = Filter()
        f_year.name = 'YEAR'
        f_year.key = 'Name1'
        f_year.value = 'Value1'
        f_year.values = []
        c2.filters = [f2, f_year]


        c3 = Chart()
        c3.title = Title()
        c3.title.operation = Operation.UNIQUE
        c3.title.var = "Age at patient end" 
        c3.title.fixed_title = "Age at patient end" 
        
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
        c4.title.fixed_title = "Age at patient end" 
        
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
        c5.title.fixed_title = "Age at start of year" 
        
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
        c6.title.fixed_title = "Observation time" 
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
        c7.title.fixed_title = "Observation time before a year" 
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
        c8.title.fixed_title = "Observation time after a year" 
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
        c9.title.fixed_title = "Observation time in a year" 
        c9.x_axis = Axis()
        c9.x_axis.operation = "unique"
        c9.x_axis.var = "Name1"
        c9.y_axis = Axis()
        c9.y_axis.operation = "unique"
        c9.y_axis.var = "Count"
        
        c9.filters = [f1]



        c10 = Chart()
        c10.title = Title()
        c10.title.operation = Operation.UNIQUE
        c10.title.var = "Start date" 
        c10.title.fixed_title = "Start date" 
        c10.x_axis = Axis()
        c10.x_axis.operation = "unique"
        c10.x_axis.var = "Name1"
        c10.y_axis = Axis()
        c10.y_axis.operation = "unique"
        c10.y_axis.var = "Count"
        
        c10.filters = [f1]


        c11 = Chart()
        c11.title = Title()
        c11.title.operation = Operation.UNIQUE
        c11.title.var = "End date" 
        c11.title.fixed_title = "End date" 
        c11.x_axis = Axis()
        c11.x_axis.operation = "unique"
        c11.x_axis.var = "Name1"
        c11.y_axis = Axis()
        c11.y_axis.operation = "unique"
        c11.y_axis.var = "Count"
        
        c11.filters = [f1]


        c12 = Chart()
        c12.title = Title()
        c12.title.operation = Operation.UNIQUE
        c12.title.fixed_title = "Age at patient start - percentiles" 
        c12.title.var = "Age at patient start" 
        c12.x_axis = Axis()
        c12.x_axis.operation = "unique"
        c12.x_axis.var = 'Value1'
        

        c12.y_axis = Axis()
        c12.y_axis.multivalue = True
        c12.y_axis.operation = "unique"
        c12.y_axis.var = ["perc25", "Mean", "perc75", "Median"]
        f1 = Filter()
        f1.name = 'Year'
        f1.key = 'Name1'
        f1.value = 'Value1'

        f2 = Filter()
        f2.name = 'Gender'
        f2.key = None
        f2.value = 'Gender'

        c12.filters = [f2]

        return sc

conf = ConfCharts()