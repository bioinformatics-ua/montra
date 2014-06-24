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


