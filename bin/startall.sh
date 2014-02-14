pkill mongodb
pkill start.jar

./bin/startmongodb > /dev/null &
./bin/startsolr.sh > /dev/null & 
./bin/startserver 
