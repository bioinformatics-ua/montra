 if [ -z "$SOLR_PATH" ] 
then
    SOLR_PATH="/usr/local/solr-4.1.0/example"
    SOLR_PATH="/Users/bastiao/Desktop/solr-4.7.0/example"
fi
cd $SOLR_PATH
java -jar "start.jar"
