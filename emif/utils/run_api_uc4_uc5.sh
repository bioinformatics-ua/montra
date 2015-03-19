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

END_POINT="http://bioinformatics.ua.pt/emif-dev"
FINGERPRINT_ID="9ec67af76878230d46951443d0e3c8d2"
TOKEN="270a6979313c1597c1f49eddd887da6633a12402"

curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Demographics+Sex\":\" Male and Female \" }}" $END_POINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Demographics+Age\":\"12-14\" }}" $END_POINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Demographics+Country\":\" Portugal \" }}" $END_POINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Outcome\":\"Progression\" }}" $END_POINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Outcome\":\"Death\" }}" $END_POINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Outcome\":\"OMS_Score\" }}" $END_POINT/api/metadata
