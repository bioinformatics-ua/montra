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

import datetime
import json
from emif import settings



def clean_value(value):
    return str(value).replace('\n', '').rstrip()


def import_population_characteristics_data(user, fingerprint_id, revision, filename='TEST_DataProfile_v1.5.6b.txt'):
    """
    This function is responsabible to parse Jerboa file

    """

    #_debug=True to not save
    _debug = False
    log = ''

    json_data = ''
    comma = ''
    try:
        f = open(filename)
        log += '\nFile opened %s ' % filename
        data = f.readlines()[1:]
        for line in data:
            file_line_info = {
                'fingerprint_id': fingerprint_id,
                'revision': revision,
                'created_date': datetime.datetime.now().strftime("%Y%m%d-%H%M%S"),
                'author': user.id,
            }
            line_data = {}
            # parse input, assign values to variables
            values = line.split('\t')
            #print len(values)
            if len(values) > 0:
                line_data['Var'] = clean_value(values[0])
            if len(values) > 1:
                line_data['Name1'] = clean_value(values[1])
            if len(values) > 2:
                line_data['Value1'] = clean_value(values[2])
            if len(values) > 2:
                line_data['Name2'] = clean_value(values[3])
            if len(values) > 4:
                line_data['Value2'] = clean_value(values[4])
            if len(values) > 5:
                line_data['Gender'] = clean_value(values[5])
            if len(values) > 6:
                line_data['Min'] = clean_value(values[6])
            if len(values) > 7:
                line_data['Max'] = clean_value(values[7])
            if len(values) > 8:
                line_data['Count'] = clean_value(values[8])
            if len(values) > 9:
                line_data['Mean'] = clean_value(values[9])
            if len(values) > 10:
                line_data['perc25'] = clean_value(values[10])
            if len(values) > 11:
                line_data['Median'] = clean_value(values[11])
            if len(values) > 12:
                line_data['perc75'] = clean_value(values[12])
            if len(values) > 13:
                line_data['SD'] = clean_value(values[13])

            # print line_data
            file_line_info['values'] = line_data
            # print file_line_info
            json_data += comma + json.dumps(file_line_info)
            comma = ', '
        #print json_data
        f.close()
        return "[" + json_data + "]"
    except:
        print "-- ERROR: The file "+str(filename)+" couldn't be open."
        return "[]"

#import_population_characteristics_data()
