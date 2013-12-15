# -*- coding: utf-8 -*-

# Copyright (C) 2013 Luís A. Bastião Silva and Universidade de Aveiro
#
# Authors: Luís A. Bastião Silva <bastiao@ua.pt>
#          Rui D. A. Mendes <ruidamendes@ua.pt>
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
import datetime
import json
from emif import settings


def import_population_characteristics_data(filename='TEST_DataProfile_v1.5.6b.txt'):
    """
    To-Do

    """

    #_debug=True to not save
    _debug = False
    log = ''

    json_data = ''
    comma = ''

    f = open(r'C:/' + filename)
    log += '\nFile opened %s ' % filename
    print r'C:/' + filename
    data = f.readlines()[1:]
    for line in data:
        file_line_info = {
            'fingerprint_id': 'abcd',
            'created_date': datetime.datetime.now().strftime("%Y%m%d-%H%M%S"),
            'author': 'rui',
        }
        line_data = {}
        # parse input, assign values to variables
        values = line.split('\t')
        print len(values)
        if len(values) > 0:
            line_data['Var'] = str(values[0]).replace('\n', '')
        if len(values) > 1:
            line_data['Name1'] = str(values[1]).replace('\n', '')
        if len(values) > 2:
            line_data['Value1'] = str(values[2]).replace('\n', '')
        if len(values) > 2:
            line_data['Name2'] = str(values[3]).replace('\n', '')
        if len(values) > 4:
            line_data['Value2'] = str(values[4]).replace('\n', '')
        if len(values) > 5:
            line_data['Gender'] = str(values[5]).replace('\n', '')
        if len(values) > 6:
            line_data['Min'] = str(values[6]).replace('\n', '')
        if len(values) > 7:
            line_data['Max'] = str(values[7]).replace('\n', '')
        if len(values) > 8:
            line_data['Count'] = str(values[8]).replace('\n', '')
        if len(values) > 9:
            line_data['Mean'] = str(values[9]).replace('\n', '')
        if len(values) > 10:
            line_data['perc25'] = str(values[10]).replace('\n', '')
        if len(values) > 11:
            line_data['Median'] = str(values[11]).replace('\n', '')
        if len(values) > 12:
            line_data['perc75'] = str(values[12]).replace('\n', '')
        if len(values) > 13:
            line_data['SD'] = str(values[13]).replace('\n', '')

        # print line_data
        file_line_info['values'] = line_data
        # print file_line_info
        json_data += comma + json.dumps(file_line_info)
        comma = ', '
    print json_data
    f.close()

import_population_characteristics_data()
