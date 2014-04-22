pkill mongodb
pkill start.jar

./bin/startmongodb > /dev/null &
./bin/startsolr.sh > /dev/null & 
./bin/startrabbitmq.sh
./bin/startserver 
cd emif 
celery --app=emif.tasks worker -l info

