#!/bin/bash

PROJECT_ROOT="/projects_dev/"
DIR_NAME="emif-test"
VIRTUAL_ENV_ROOT="/opt_dev/" 
DB_NAME="emif_test"
DB_USER="emif_test"
DB_PASSWORD=""
BRANCH="dev"
LOCATION_SQL=""
SOLR_CONFIG=""

set -e

echo "Clone the project from github.."
cd $PROJECT_ROOT
#git clone git@github.com:bioinformatics-ua/emif-fb.git -b $BRANCH $DIR_NAME
echo "Done." 


echo "Create the virtual enviroment " 
cd $DIR_NAME

cd $VIRTUAL_ENV_ROOT

#virtualenv "$DIR_NAME-env"


echo "Done."

echo "Loading virtualenviroment "

echo "$VIRTUAL_ENV_ROOT$DIR_NAME-env/bin/activate" 

source "$VIRTUAL_ENV_ROOT$DIR_NAME-env/bin/activate"


cd $PROJECT_ROOT
cd $DIR_NAME

# pip install -r requirements.txt

echo "drop all the old tables " 


PGDB=$DB_NAME

TABLES=`psql $PGDB -t --command "SELECT string_agg(table_name, ',') FROM information_schema.tables WHERE table_schema='public'"`
echo Dropping tables:${TABLES}
#psql $PGDB --command "DROP TABLE IF EXISTS ${TABLES} CASCADE"


echo "restoring the backup " 
#psql $PGDB < $LOCATION_SQL 

echo "reset the staff" 

echo "create the uwsgi file " 


echo "create commands to update solr" 





echo "create commands to index all the staff " 


echo "commands to update the urls in fingerprint browser" 
#python manage.py set_urls http://bioinformatics.ua.pt/emif-dev/static/ http://bioinformatics.ua.pt/emif-dev/

echo "Successefully deployed EMIF Catalogue"



