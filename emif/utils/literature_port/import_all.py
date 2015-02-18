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
import pm_import
import sys
import os
import os.path

map_fingerprint_ids={'768185357ce7e4e0aeae6d2e69f6d7e0': 'ARS_json_done.json',
                    '45b7ccb3aca47bc37f9bd82504f09b3b': 'GePARD_json_done.json',
                    '52d4981701f0126d947014244744efea': 'HSD CSD LPD_json_done.json',
                    '54d8384917b21fb7928ba72a1e72326b': 'IPCI_json_done.json',
                    '7b128593480b53409ac83c9582badbb7': 'MAAS_json_done.json',
                    '5d8f88d91f1dc3e2806d825f61260b76':'PEDIANET_json_done.json',
                    '7a205644571c31bc50965c68d7565622': 'THIN_done.json',

}

ROOT_PATH = sys.argv[1]

pm_import.host1 = str(sys.argv[2])
pm_import.port1 = str(sys.argv[3])

for f_id in map_fingerprint_ids:
    file_path = map_fingerprint_ids[f_id]
    full_path = os.path.join(ROOT_PATH, file_path)
    print "ID " + str(f_id) + " with file path: " + str(file_path)
    pm_import.main(f_id, str(full_path))
    print "F id: "  + str(f_id) + " has been completed sucessfully"


print "task has been done"


