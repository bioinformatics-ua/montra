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
from population_characteristics.conf_charts import *

from fingerprint.models import Fingerprint

class RuleMatcher(object):

    def __init__(self, comp=False, type=None):
        self.comp = comp
        self.ftype = type

    def get_filter(self, var):
        if self.comp:
            charts = conf.get_compare_settings().charts
        else:
            charts = conf.get_main_settings(type=self.ftype).charts
        filters = None
        for c in charts:
            if c.title.fixed_title==var:
                filters = c.filters
                break
        return filters

    def get_chart(self, var):
        if self.comp:
            charts = conf.get_compare_settings().charts
        else:
            charts = conf.get_main_settings(type=self.ftype).charts
        result = None
        for c in charts:
            if c.title.fixed_title==var:
                result= c
                break
        return result


