#### Change the variables here
LOCATION_SQL="/Users/bastiao/GDrive/EMIF/backup.sql"


curl http://localhost:8983/solr/update --data '<delete><query>*:*</query></delete>' -H 'Content-type:text/xml; charset=utf-8'  
curl http://localhost:8983/solr/update --data '<commit/>' -H 'Content-type:text/xml; charset=utf-8'

python emif/utils/import_answers.py

PGDB="emif_dev"
TABLES=`psql $PGDB -t --command "SELECT string_agg(table_name, ',') FROM information_schema.tables WHERE table_schema='public'"`

echo Dropping tables:${TABLES}
psql $PGDB --command "DROP TABLE IF EXISTS ${TABLES} CASCADE"


psql $PGDB < $LOCATION_SQL