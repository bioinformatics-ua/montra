/**********************************************************************
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

***********************************************************************/

function TransformFilter(filters){

    this.filters = filters;

    this.genre = function() {
        if (!Object.prototype.hasOwnProperty.call(this.filters, 'values.Gender'))
            return this.filters;
        var maleSelected = this.filters['values.Gender'].indexOf('M') >= 0;
        var femaleSelected =  this.filters['values.Gender'].indexOf('F') >= 0;
        var compare =  this.filters['values.Gender'].indexOf('ALL') >= 0;
        if (maleSelected &femaleSelected )
        {
            this.filters['values.Gender'] = ['T'];
        }
        if (compare)
        {
            this.filters['values.Gender'] = ['T', 'M', 'F'];
        }

        return this.filters;

    };
    this.transform = function() {
        this.filters = this.genre();
        return this.filters;
    };
};




