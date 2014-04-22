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
from population_characteristics.charts.chart import *



class ConfCharts(object):

    def __init__(self):
        # TODO 
        pass

    def read_settings_from_file(self):
        # TODO
        pass

    """ get the default settings to load 
    """
    
    def get_main_settings(self):
        



        sc = SetCharst()

        sc.charts = []

        #################################################
        ### Active patients
        #################################################
        c = Chart()
        c.uid = 1
        c.title = Title()
        c.title.operation = Operation.UNIQUE
        c.title.var = "Active patients" 
        c.title.fixed_title = "Active patients" 
        c.x_axis = Axis()
        c.x_axis.operation = "unique"
        c.x_axis.var = "Value1"
        c.x_axis.label = 'Years'
        c.y_axis = Axis()
        c.y_axis.operation = "unique"
        c.y_axis.var = "Count"
        c.y_axis.label = 'Number of patients'
        c.y_axis.multivalue = True


        f1 = Filter()
        f1.name = 'Year'
        f1.key = 'Name1'
        f1.value = 'Value1'

        f2 = Filter()
        f2.name = 'Gender'
        f2.key = None
        f2.value = 'Gender'
        f2.translation = {'M': 'Male', 'F': 'Female', 'T': 'Total',  'ALL': 'Male/Female'}
        f2.comparable = True
        f2.comparable_values = ['M', 'F']

        ss = Scale()
        ss.unit = "Year"
        ss.bins = "10"

        c.filters = [f2]

        sc.charts.append(c)


        #################################################
        ### Birth date
        #################################################

        c1 = Chart()
        c1.uid = 2
        c1.title = Title()
        c1.title.operation = Operation.UNIQUE
        c1.title.var = "Birth in year" 
        c1.title.fixed_title = "Birth date"
        
        c1.x_axis = Axis()
        c1.x_axis.operation = "unique"
        c1.x_axis.var = "Value1"
        c1.x_axis.label = 'Years'
        c1.y_axis = Axis()
        c1.y_axis.operation = "unique"
        c1.y_axis.var = "Count"
        c1.y_axis.label = 'Number of patients'
        c1.y_axis.multivalue = True

        f2 = Filter()
        f2.name = 'Gender'
        f2.key = None
        f2.value = 'Gender'
        f2.translation = {'M': 'Male', 'F': 'Female', 'T': 'Total',  'ALL': 'Male/Female'}
        
        c1.filters = [f2]

        sc.charts.append(c1)


        #################################################
        ### Start date
        #################################################

        c10 = Chart()
        c10.uid = 3
        c10.title = Title()
        c10.title.operation = Operation.UNIQUE
        c10.title.var = "Age at patient start" 
        c10.title.fixed_title = "Start date" 
        c10.x_axis = Axis()
        c10.x_axis.operation = "unique"
        c10.x_axis.var = "Value1"
        c10.x_axis.label = 'Years'
        c10.y_axis = Axis()
        c10.y_axis.operation = "unique"
        c10.y_axis.var = "Count"
        c10.y_axis.label = 'Number of patients'
        c10.y_axis.multivalue = True


        fy1 = Filter()
        fy1.name = 'Name2'
        fy1.key = 'Name2'
        fy1.value = ''

        fy2 = Filter()
        fy2.name = 'Year'
        fy2.key = 'Value2'
        fy2.value = ''

        fy3 = Filter()
        fy3.name = 'Name1'
        fy3.key = 'Name1'
        fy3.value = 'YEAR'


        c10.y_axis.static_filters = [fy1, fy2, fy3]

        f2 = Filter()
        f2.name = 'Gender'
        f2.key = None
        f2.value = 'Gender'
        f2.translation = {'M': 'Male', 'F': 'Female', 'T': 'Total',  'ALL': 'Male/Female'}
        c10.filters = [f2]
        sc.charts.append(c10)


        #################################################
        ### End date
        #################################################

        f2 = Filter()
        f2.name = 'Gender'
        f2.key = None
        f2.value = 'Gender'
        f2.translation = {'M': 'Male', 'F': 'Female', 'T': 'Total',  'ALL': 'Male/Female'}

        c11 = Chart()
        c11.uid = 4
        c11.title = Title()
        c11.title.operation = Operation.UNIQUE
        c11.title.var = "Age at patient end" 
        c11.title.fixed_title = "End date" 
        c11.x_axis = Axis()
        c11.x_axis.operation = "unique"
        c11.x_axis.var = "Value1"
        c11.x_axis.label = 'Years'
        c11.y_axis = Axis()
        c11.y_axis.operation = "unique"
        c11.y_axis.var = "Count"
        c11.y_axis.label = 'Number of patients'
        c11.y_axis.multivalue = True
        fy1 = Filter()
        fy1.name = 'Name2'
        fy1.key = 'Name2'
        fy1.value = ''

        fy2 = Filter()
        fy2.name = 'Value2'
        fy2.key = 'Value2'
        fy2.value = ''

        fy3 = Filter()
        fy3.name = 'Name1'
        fy3.key = 'Name1'
        fy3.value = 'YEAR'


        c11.y_axis.static_filters = [fy1, fy2, fy3]

        c11.filters = [f2]
        sc.charts.append(c11)



        #################################################
        ### Age at patient start
        #################################################


        c2 = Chart()
        c2.uid = 5
        c2.title = Title()
        c2.title.operation = Operation.UNIQUE
        c2.title.var = "Age at start of year" 
        c2.title.fixed_title = "Age at start of year" 

        # X AXIS 
        c2.x_axis = Axis()
        c2.x_axis.operation = "unique"
        c2.x_axis.var = "Value2"
        c2.x_axis.label = "Age (Years)"
        c2.x_axis.categorized = True
        c2.x_axis.sort_func = "int(k[c1.x_axis.var].split('-')[0])"


        c2_filters_x = Filter()
        c2_filters_x.name = 'AGE'
        c2_filters_x.key = 'Name2'
        c2_filters_x.value = 'Value2'
        #c2.x_axis.filters = [c2_filters_x]


        c2.y_axis = Axis()
        c2.y_axis.operation = "unique"
        c2.y_axis.var = "Count"
        c2.y_axis.label = "Number of patients"
        c2.y_axis.multivalue = True

        fy2 = Filter()
        fy2.name = 'Name2'
        fy2.key = 'Name2'
        fy2.value = 'AGE'

        fy3 = Filter()
        fy3.name = 'Name1'
        fy3.key = 'Name1'
        fy3.value = 'YEAR'


        c2.y_axis.static_filters = [fy2, fy3]


        f_year = Filter()
        f_year.name = 'YEAR'
        f_year.key = 'Name1'
        f_year.value = 'Value1'
        #f_year.values = []
        f2 = Filter()
        f2.name = 'Gender'
        f2.key = None
        f2.value = 'Gender'
        f2.translation = {'M': 'Male', 'F': 'Female', 'T': 'Total',  'ALL': 'Male/Female'}
        c2.filters = [f2, f_year]

        sc.charts.append(c2)



        #################################################
        ### Age at patient start
        #################################################


        c4 = Chart()
        c4.uid = 6
        c4.title = Title()
        c4.title.operation = Operation.UNIQUE
        c4.title.var = "Age at patient start" 
        c4.title.fixed_title = "Age at patient start" 
        
        #4X AXIS 
        c4.x_axis = Axis()
        c4.x_axis.operation = "unique"
        c4.x_axis.var = "Value2"
        c4.x_axis.label = "Age (years)"
        c4.x_axis.categorized = True
        c4.x_axis.sort_func = "int(k[c1.x_axis.var].split('-')[0])"


        c4_filters_x = Filter()
        c4_filters_x.name = 'AGE'
        c4_filters_x.key = 'Name2'
        c4_filters_x.value = 'Value2'
        #42.x_axis.filters = [c2_filters_x]


        c4.y_axis = Axis()
        c4.y_axis.operation = "unique"
        c4.y_axis.var = "Count"
        c4.x_axis.label = "Number of patients"
        c4.y_axis.multivalue = True

        fy2 = Filter()
        fy2.name = 'Name2'
        fy2.key = 'Name2'
        fy2.value = 'AGE'

        fy3 = Filter()
        fy3.name = 'Name1'
        fy3.key = 'Name1'
        fy3.value = 'YEAR'


        c4.y_axis.static_filters = [fy2, fy3]


        f_year = Filter()
        f_year.name = 'YEAR'
        f_year.key = 'Name1'
        f_year.value = 'Value1'
        #f_year.values = []
        f2 = Filter()
        f2.name = 'Gender'
        f2.key = None
        f2.value = 'Gender'
        f2.translation = {'M': 'Male', 'F': 'Female', 'T': 'Total',  'ALL': 'Male/Female'}
        c4.filters = [f2, f_year]

        sc.charts.append(c4)



        #################################################
        ### Age at patient end
        #################################################


        c3 = Chart()
        c3.uid = 7
        c3.title = Title()
        c3.title.operation = Operation.UNIQUE
        c3.title.var = "Age at patient end" 
        c3.title.fixed_title = "Age at patient end" 
        
        #3X AXIS 
        c3.x_axis = Axis()
        c3.x_axis.operation = "unique"
        c3.x_axis.var = "Value2"
        c3.x_axis.label = "Age (years)"
        c3.x_axis.categorized = True
        c3.x_axis.sort_func = "int(k[c1.x_axis.var].split('-')[0])"


        c3_filters_x = Filter()
        c3_filters_x.name = 'AGE'
        c3_filters_x.key = 'Name2'
        c3_filters_x.value = 'Value2'
        #c2.x_axis.filters = [c2_filters_x]


        c3.y_axis = Axis()
        c3.y_axis.operation = "unique"
        c3.y_axis.var = "Count"
        c3.y_axis.label = "Number of patients"
        c3.y_axis.multivalue = True


        fy2 = Filter()
        fy2.name = 'Name2'
        fy2.key = 'Name2'
        fy2.value = 'AGE'

        fy3 = Filter()
        fy3.name = 'Name1'
        fy3.key = 'Name1'
        fy3.value = 'YEAR'


        c3.y_axis.static_filters = [fy2, fy3]


        f_year = Filter()
        f_year.name = 'YEAR'
        f_year.key = 'Name1'
        f_year.value = 'Value1'
        #f_year.values = []
        f2 = Filter()
        f2.name = 'Gender'
        f2.key = None
        f2.value = 'Gender'
        f2.translation = {'M': 'Male', 'F': 'Female', 'T': 'Total',  'ALL': 'Male/Female'}
        c3.filters = [f2, f_year]

        sc.charts.append(c3)






        #################################################
        ### Total patient time in a year
        #################################################


        c5 = Chart()
        c5.uid = 8
        c5.title = Title()
        c5.title.operation = Operation.UNIQUE
        c5.title.var = "Observation time in a year" 
        c5.title.fixed_title = "Total patient time in a year" 
        c5.x_axis = Axis()
        c5.x_axis.operation = "unique"
        c5.x_axis.var = "Value1"
        c5.x_axis.label = "Years"
        c5.y_axis = Axis()
        c5.y_axis.operation = "unique"
        c5.y_axis.var = "Count"
        c5.y_axis.transformation = "y / 12"
        c5.y_axis.label = "Sum of the patients observation time (years)"
        c5.y_axis.multivalue = True

        fy2 = Filter()
        fy2.name = 'Name2'
        fy2.key = 'Name2'
        fy2.value = ''

        fy3 = Filter()
        fy3.name = 'Value2'
        fy3.key = 'Value2'
        fy3.value = ''

        c5.y_axis.static_filters = [fy2, fy3]


        f1 = Filter()
        f1.name = 'Year'
        f1.key = 'Name1'
        f1.value = 'Value1'

        f2 = Filter()
        f2.name = 'Gender'
        f2.key = None
        f2.value = 'Gender'
        f2.translation = {'M': 'Male', 'F': 'Female', 'T': 'Total',  'ALL': 'Male/Female'}

        ss = Scale()
        ss.unit = "Year"
        ss.bins = "10"

        c5.filters = [f2]

        sc.charts.append(c5)


        #################################################
        ### Age at patient start - percentiles
        #################################################
        c12 = Chart()
        c12.uid = 9
        c12.title = Title()
        c12.legend = True
        c12.title.operation = Operation.UNIQUE
        c12.title.fixed_title = "Age at patient start - percentiles" 
        c12.title.var = "Age at patient start" 
        c12.x_axis = Axis()
        c12.x_axis.operation = "unique"
        c12.x_axis.var = 'Value1'
        c12.x_axis.label = 'Years'
        

        c12.y_axis = Axis()
        c12.y_axis.multivalue = True
        c12.y_axis.operation = "unique"
        c12.y_axis.var = ["perc25", "Mean", "perc75", "Median"]
        c12.y_axis.static_filters = []
        c12.y_axis.transformation = "y / 12"
        c12.y_axis.label = "Age (years)"

        fy1 = Filter()
        fy1.name = 'Name2'
        fy1.key = 'Name2'
        fy1.value = ''

        fy2 = Filter()
        fy2.name = 'Value2'
        fy2.key = 'Value2'
        fy2.value = ''

        fy3 = Filter()
        fy3.name = 'Name1'
        fy3.key = 'Name1'
        fy3.value = 'YEAR'


        c12.y_axis.static_filters = [fy1, fy2, fy3]


        f1 = Filter()
        f1.name = 'Year'
        f1.key = 'Name1'
        f1.value = 'Value1'

        f2 = Filter()
        f2.name = 'Gender'
        f2.key = None
        f2.value = 'Gender'
        f2.translation = {'M': 'Male', 'F': 'Female', 'T': 'Total',  'ALL': 'Male/Female'}

        c12.filters = [f2]
        sc.charts.append(c12)


        #################################################
        ### Age at patient end - percentiles
        #################################################
        c13 = Chart()
        c13.uid = 10
        c13.title = Title()
        c13.legend = True
        c13.title.operation = Operation.UNIQUE
        c13.title.fixed_title = "Age at patient end - percentiles" 
        c13.title.var = "Age at patient end" 
        c13.x_axis = Axis()
        c13.x_axis.operation = "unique"
        c13.x_axis.var = 'Value1'
        c13.x_axis.label = 'Years'
        
        

        c13.y_axis = Axis()
        c13.y_axis.multivalue = True
        c13.y_axis.operation = "unique"
        c13.y_axis.var = ["perc25", "Mean", "perc75", "Median"]
        c13.y_axis.static_filters = []
        c13.y_axis.transformation = "y / 12"
        c13.y_axis.label = "Age (years)"

        fy1 = Filter()
        fy1.name = 'Name2'
        fy1.key = 'Name2'
        fy1.value = ''

        fy2 = Filter()
        fy2.name = 'Value2'
        fy2.key = 'Value2'
        fy2.value = ''

        fy3 = Filter()
        fy3.name = 'Name1'
        fy3.key = 'Name1'
        fy3.value = 'YEAR'


        c13.y_axis.static_filters = [fy1, fy2, fy3]


        f1 = Filter()
        f1.name = 'Year'
        f1.key = 'Name1'
        f1.value = 'Value1'

        f2 = Filter()
        f2.name = 'Gender'
        f2.key = None
        f2.value = 'Gender'
        f2.translation = {'M': 'Male', 'F': 'Female', 'T': 'Total',  'ALL': 'Male/Female'}

        c13.filters = [f2]
        sc.charts.append(c13)



        #################################################
        ### Age at start of year - percentiles
        #################################################
        c14 = Chart()
        c14.uid = 11
        c14.title = Title()
        c14.legend = True
        c14.title.operation = Operation.UNIQUE
        c14.title.fixed_title = "Age at start of year - percentiles" 
        c14.title.var = "Age at start of year" 
        c14.x_axis = Axis()
        c14.x_axis.operation = "unique"
        c14.x_axis.var = 'Value1'
        c14.x_axis.var = 'Years'
        
        

        c14.y_axis = Axis()
        c14.y_axis.multivalue = True
        c14.y_axis.operation = "unique"
        c14.y_axis.var = ["perc25", "Mean", "perc75", "Median"]
        c14.y_axis.static_filters = []
        c14.y_axis.transformation = "y / 12"
        c14.y_axis.label = "Age (years)"

        fy1 = Filter()
        fy1.name = 'Name2'
        fy1.key = 'Name2'
        fy1.value = ''

        fy2 = Filter()
        fy2.name = 'Value2'
        fy2.key = 'Value2'
        fy2.value = ''

        fy3 = Filter()
        fy3.name = 'Name1'
        fy3.key = 'Name1'
        fy3.value = 'YEAR'


        c14.y_axis.static_filters = [fy1, fy2, fy3]


        f1 = Filter()
        f1.name = 'Year'
        f1.key = 'Name1'
        f1.value = 'Value1'

        f2 = Filter()
        f2.name = 'Gender'
        f2.key = None
        f2.value = 'Gender'
        f2.translation = {'M': 'Male', 'F': 'Female', 'T': 'Total',  'ALL': 'Male/Female'}

        c14.filters = [f2]
        sc.charts.append(c14)



        #################################################
        ### Patient time before a year - percentile
        #################################################
        c14 = Chart()
        c14.uid = 12
        c14.title = Title()
        c14.legend = True
        c14.title.operation = Operation.UNIQUE
        c14.title.fixed_title = "Patient time before a year - percentile" 
        c14.title.var = "Observation time before a year" 
        c14.x_axis = Axis()
        c14.x_axis.operation = "unique"
        c14.x_axis.var = 'Value1'
        c14.x_axis.label = 'Years'
        
        

        c14.y_axis = Axis()
        c14.y_axis.multivalue = True
        c14.y_axis.operation = "unique"
        c14.y_axis.var = ["perc25", "Mean", "perc75", "Median"]
        c14.y_axis.static_filters = []
        c14.y_axis.transformation = "y / 12"
        c14.y_axis.label = "Age (years)"

        fy1 = Filter()
        fy1.name = 'Name2'
        fy1.key = 'Name2'
        fy1.value = ''

        fy2 = Filter()
        fy2.name = 'Value2'
        fy2.key = 'Value2'
        fy2.value = ''

        fy3 = Filter()
        fy3.name = 'Name1'
        fy3.key = 'Name1'
        fy3.value = 'YEAR'


        c14.y_axis.static_filters = [fy1, fy2, fy3]


        f1 = Filter()
        f1.name = 'Year'
        f1.key = 'Name1'
        f1.value = 'Value1'

        f2 = Filter()
        f2.name = 'Gender'
        f2.key = None
        f2.value = 'Gender'
        f2.translation = {'M': 'Male', 'F': 'Female', 'T': 'Total',  'ALL': 'Male/Female'}

        c14.filters = [f2]
        sc.charts.append(c14)


        #################################################
        ### Patient time after a year - percentile
        #################################################
        c14 = Chart()
        c14.uid = 13
        c14.title = Title()
        c14.legend = True
        c14.title.operation = Operation.UNIQUE
        c14.title.fixed_title = "Patient time after a year - percentile" 
        c14.title.var = "Observation time after a year" 
        c14.x_axis = Axis()
        c14.x_axis.operation = "unique"
        c14.x_axis.var = 'Value1'
        c14.x_axis.label = 'Years'
        
        

        c14.y_axis = Axis()
        c14.y_axis.multivalue = True
        c14.y_axis.operation = "unique"
        c14.y_axis.var = ["perc25", "Mean", "perc75", "Median"]
        c14.y_axis.static_filters = []
        c14.y_axis.transformation = "y / 12"
        c14.y_axis.label = "Age (years)"

        fy1 = Filter()
        fy1.name = 'Name2'
        fy1.key = 'Name2'
        fy1.value = ''

        fy2 = Filter()
        fy2.name = 'Value2'
        fy2.key = 'Value2'
        fy2.value = ''

        fy3 = Filter()
        fy3.name = 'Name1'
        fy3.key = 'Name1'
        fy3.value = 'YEAR'


        c14.y_axis.static_filters = [fy1, fy2, fy3]


        f1 = Filter()
        f1.name = 'Year'
        f1.key = 'Name1'
        f1.value = 'Value1'

        f2 = Filter()
        f2.name = 'Gender'
        f2.key = None
        f2.value = 'Gender'
        f2.translation = {'M': 'Male', 'F': 'Female', 'T': 'Total',  'ALL': 'Male/Female'}

        c14.filters = [f2]
        sc.charts.append(c14)


        #################################################
        ### Patient Time
        #################################################
        c = Chart()
        c.uid = 14
        c.title = Title()
        c.title.operation = Operation.UNIQUE
        c.title.var = "Observation time in years" 
        c.title.fixed_title = "Patient time" 
        c.x_axis = Axis()
        c.x_axis.operation = "unique"
        c.x_axis.var = "Value1"
        c.x_axis.label = 'Patient time (years)'
        c.y_axis = Axis()
        c.y_axis.operation = "unique"
        c.y_axis.var = "Count"
        c.y_axis.label = 'Number of patients'
        c.y_axis.multivalue = True
        f1 = Filter()
        f1.name = 'Year'
        f1.key = 'Name1'
        f1.value = 'Value1'

        f2 = Filter()
        f2.name = 'Gender'
        f2.key = None
        f2.value = 'Gender'
        f2.translation = {'M': 'Male', 'F': 'Female', 'T': 'Total',  'ALL': 'Male/Female'}

        ss = Scale()
        ss.unit = "Year"
        ss.bins = "10"

        c.filters = [f2]

        sc.charts.append(c)


        return sc



    ############################################################
    ############################################################
    ############################################################ 

    """ get the compare settings to load 
    """
    ############################################################
    ############################################################
    ############################################################

    def get_compare_settings(self):
        

        sc = SetCharst()

        sc.charts = []

        


        #################################################
        ### Total patient time in a year
        #################################################


        c5 = Chart()
        c5.uid = 8
        c5.title = Title()
        c5.title.operation = Operation.UNIQUE
        c5.title.var = "Observation time in a year" 
        c5.title.fixed_title = "Total Overall patient time in a year"
        c5.stacked = True 
        c5.x_axis = Axis()
        c5.x_axis.operation = "unique"
        c5.x_axis.var = "dbname_value"
        c5.x_axis.label = "Years"
        c5.x_axis.categorized = True
        c5.y_axis = Axis()
        c5.y_axis.operation = "unique"
        c5.y_axis.var = "Count"
        c5.y_axis.transformation = "y / 12 / 1000"
        c5.y_axis.label = "Sum of the patients observation time (years)"
        c5.y_axis.multivalue = True

        fy2 = Filter()
        fy2.name = 'Name1'
        fy2.key = 'Name1'
        fy2.value = ''

        fy3 = Filter()
        fy3.name = 'Value1'
        fy3.key = 'Value1'
        fy3.value = ''

        fy4 = Filter()
        fy4.name = 'dbname'
        fy4.key = 'dbname'
        fy4.value = 'dbname'

        c5.y_axis.static_filters = [fy2, fy3,fy4 ]


        f1 = Filter()
        f1.name = 'Year'
        f1.key = 'Name1'
        f1.value = 'Value1'

        f2 = Filter()
        f2.name = 'Gender'
        f2.key = None
        f2.value = 'Gender'
        f2.translation = {'M': 'Male', 'F': 'Female', 'T': 'Total',  'ALL': 'Male/Female'}


        c5.filters = [f2]

        sc.charts.append(c5)


        #################################################
        ### Total patient time in a year
        #################################################


        c5 = Chart()
        c5.uid = 18
        c5.title = Title()
        c5.title.operation = Operation.UNIQUE
        c5.title.var = "Observation time in a year" 
        c5.title.fixed_title = "Total patient time in a year" 
        c5.stacked = True 
        c5.x_axis = Axis()
        c5.x_axis.operation = "unique"
        c5.x_axis.var = "dbname_value"
        c5.x_axis.categorized = True
        c5.x_axis.label = "Db name"
        c5.y_axis = Axis()
        c5.y_axis.operation = "unique"
        c5.y_axis.var = "Count"
        c5.y_axis.transformation = "y / 12 / 1000"
        c5.y_axis.label = "Sum of the patients observation time (years)"
        c5.y_axis.multivalue = True

        fy2 = Filter()
        fy2.name = 'Name2'
        fy2.key = 'Name2'
        fy2.value = ''

        fy3 = Filter()
        fy3.name = 'Value2'
        fy3.key = 'Value2'
        fy3.value = ''

        c5.y_axis.static_filters = [fy2, fy3]


        f1 = Filter()
        f1.name = 'Year'
        f1.key = 'Name1'
        f1.value = 'Value1'

        f2 = Filter()
        f2.name = 'Gender'
        f2.key = None
        f2.value = 'Gender'
        f2.translation = {'M': 'Male', 'F': 'Female', 'T': 'Total',  'ALL': 'Male/Female'}

        ss = Scale()
        ss.unit = "Year"
        ss.bins = "10"


        f_year = Filter()
        f_year.name = 'YEAR'
        f_year.key = 'Name1'
        f_year.value = 'Value1'

        c5.filters = [f2, f_year]

        sc.charts.append(c5)


        #################################################
        ### Location Total patient time in a year
        #################################################


        c5 = Chart()
        c5.uid = 8
        c5.title = Title()
        c5.title.operation = Operation.UNIQUE
        c5.title.var = "Observation time in a year"
        c5.stacked = True 
        c5.title.fixed_title = "Location Total Overall patient time in a year" 
        c5.x_axis = Axis()
        c5.x_axis.operation = "unique"
        c5.x_axis.var = "location_value"
        c5.x_axis.label = "Location name"
        c5.x_axis.categorized = True
        c5.y_axis = Axis()
        c5.y_axis.operation = "unique"
        c5.y_axis.var = "Count"
        c5.y_axis.transformation = "y / 12 / 1000"
        c5.y_axis.label = "Sum of the patients observation time (years)"
        c5.y_axis.multivalue = True

        fy2 = Filter()
        fy2.name = 'Name1'
        fy2.key = 'Name1'
        fy2.value = ''

        fy3 = Filter()
        fy3.name = 'Value1'
        fy3.key = 'Value1'
        fy3.value = ''


        fy4 = Filter()
        fy4.name = 'location'
        fy4.key = 'location'
        fy4.value = 'location'

        c5.y_axis.static_filters = [fy2, fy3, fy4]


        f1 = Filter()
        f1.name = 'Year'
        f1.key = 'Name1'
        f1.value = 'Value1'

        f2 = Filter()
        f2.name = 'Gender'
        f2.key = None
        f2.value = 'Gender'
        f2.translation = {'M': 'Male', 'F': 'Female', 'T': 'Total',  'ALL': 'Male/Female'}

        ss = Scale()
        ss.unit = "Year"
        ss.bins = "10"

        f_year = Filter()
        f_year.name = 'YEAR'
        f_year.key = 'Name1'
        f_year.value = 'Value1'

        c5.filters = [f2]

        sc.charts.append(c5)

       

        
        #################################################
        ### Active patients
        #################################################
        c = Chart()
        c.uid = 133
        c.title = Title()
        c.title.operation = Operation.UNIQUE
        c.title.var = "Active patients" 
        c.title.fixed_title = "Active patients" 
        c.stacked = True 
        c.x_axis = Axis()
        c.x_axis.operation = "unique"
        c.x_axis.var = "dbname_value"
        c.x_axis.categorized = True
        c.x_axis.label = 'Databases'
        c.y_axis = Axis()
        c.y_axis.operation = "unique"
        c.y_axis.var = "Count"
        c.y_axis.label = 'Number of patients'
        c.y_axis.multivalue = True


        f2 = Filter()
        f2.name = 'Gender'
        f2.key = None
        f2.value = 'Gender'
        f2.translation = {'M': 'Male', 'F': 'Female', 'T': 'Total',  'ALL': 'Male/Female'}
        f2.comparable = False
        f2.comparable_values = ['M', 'F']




        c.filters = [f2]

        sc.charts.append(c)


        return sc

conf = ConfCharts()