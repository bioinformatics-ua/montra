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
from population_characteristics.charts.chart import *
import json

class JsonChartReader:
    def __processTitle(self, title):
        t = Title()

        if 'operation' in title:
            t.operation = title['operation']

        if 'var' in title:
            t.var = title['var']

        if 'fixed_title' in title:
            t.fixed_title = title['fixed_title']

        return t

    def __processAxis(self, axis):
        a = Axis()

        if 'operation' in axis:
            a.operation = axis['operation']

        if 'var' in axis:
            a.var = axis['var']

        if 'scale' in axis:
            a.scale = axis['scale']

        if 'filters' in axis:
            a.filters = self.__processFilters(axis['filters'])

        if 'static_filters' in axis:
            a.static_filters = self.__processFilters(axis['static_filters'])

        if 'categorized' in axis:
            a.categorized = axis['categorized']

        if 'multivalue' in axis:
            a.multivalue = axis['multivalue']

        if 'transformation' in axis:
            a.transformation = axis['transformation']

        if 'sort_func' in axis:
            a.sort_func = axis['sort_func']

        if 'label' in axis:
            a.label = axis['label']

        if 'legend' in axis:
            a.legend = axis['legend']

        if 'stacked' in axis:
            a.stacked = axis['stacked']

        return a

    def __processFilters(self, filters):
        fs = []

        for filter in filters:
            f = Filter()

            if 'name' in filter:
                f.name = filter['name']

            if 'key' in filter:
                f.key = filter['key']

            if 'value' in filter:
                    f.value = filter['value']


            if 'values' in filter:
                f.values = filter['values']

            if 'translation' in filter:
                f.translation = filter['translation']

            if 'comparable' in filter:
                f.comparable = filter['comparable']

            if 'comparable_values' in filter:
                f.comparable_values = filter['comparable_values']

            if 'show' in filter:
                f.show = filter['show']

            fs.append(f)

        return fs

    def __processChart(self, entry):
        c = Chart()
        if 'title' in entry:
            c.title = self.__processTitle(entry['title'])
        if 'hint' in entry:
            c.hint = entry['hint']

        if 'tooltip' in entry:
            c.tooltip = entry['tooltip']

        if 'x_axis' in entry:
            c.x_axis = self.__processAxis(entry['x_axis'])

        if 'y_axis' in entry:
            c.y_axis =self.__processAxis(entry['y_axis'])

        if 'filters' in entry:
            c.filters = self.__processFilters(entry['filters'])

        if 'uid' in entry:
            c.uid = entry['uid']

        return c

    def read(self, path):
        try:
            with open(path) as json_data:
                d = json.loads(json_data.read())

                sc = SetCharst()
                sc.charts = []

                for entry in d['initial_settings']:
                    c = self.__processChart(entry)

                    sc.charts.append(c)

                json_data.close()

                return sc
        except IOError:
            return None
