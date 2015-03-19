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
#
#### Change the variables here
ROOT_BACKUP=$1
LOCATION_SQL=`ls $ROOT_BACKUP/home/sysadmin/backups_emif/backup*.sql`
echo $LOCATION_SQL
cp "$ROOT_BACKUP/tmp/fingerprints.pkl" emif/utils/


# Also important staff to do:
# cat ~/.pgpass
# localhost:5432:*:bastiao:emif

curl http://localhost:8983/solr/update --data '<delete><query>*:*</query></delete>' -H 'Content-type:text/xml; charset=utf-8'
curl http://localhost:8983/solr/update --data '<commit/>' -H 'Content-type:text/xml; charset=utf-8'

python emif/utils/import_answers.py

PGDB="emif_dev"
TABLES=`psql $PGDB -t --command "SELECT string_agg(table_name, ',') FROM information_schema.tables WHERE table_schema='public'"`

echo Dropping tables:${TABLES}
psql $PGDB --command "DROP TABLE IF EXISTS ${TABLES} CASCADE"


psql $PGDB < $LOCATION_SQL


