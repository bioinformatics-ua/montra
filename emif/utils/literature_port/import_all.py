

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


