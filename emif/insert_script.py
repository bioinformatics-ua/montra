import md5
import random




# Make this unique, and don't share it with anybody.
SECRET_KEY = 'j*zdirg7yy9@q1k=c*q!*kovfsd#$FDFfsdfkae#id04pyta=yz@w34m6rvwfe'

def generate_hash():
	hash = md5.new()
	hash.update("".join(map(lambda i: chr(random.randint(0, 255)), range(16))))
	hash.update(SECRET_KEY)
	key = hash.hexdigest()
	return key

import urllib
import urllib2

url = 'http://127.0.0.1:8000/api/insert'

institutionnames = ["Hospital", "Joao", "Porto", "Aveiro", "Lisboa", "Faro", "Portimao"]

location = ["Paris", "Roterdao", 
"Porto", "Aveiro", "Lisboa", "Faro", "Portimao", "Brussels", "London", 
"Barcelona", "Heildeberg", "Stuttgard", "Lens"]

data = {
        'contact_technical_t':'IEETA',
        'created_t':'2013-04-17 12:09:32.334053',
        'location_t':'Aveiro',
        'institution_name_t':'IEETA',
        'contact_scientific_t':'IEETA',
        'contact_administrative_t':'IEETA',
        'type_t':'researchcohorts',
        'id':'a10815736f733d04d8e0aa65fe37',
        'user_t' :'bastiao',
        'text_t': 'ieeta ieeta bastiao emif',
        'database_name_t':'IEETA'}

import pysolr
solr = pysolr.Solr('http://localhost:8983/solr', timeout=10)
for i in range(10):
	data['database_name_t'] = 'IEETA' + str(i)
	data['id'] = generate_hash()
	solr.add([data])
	
	solr.optimize()


#curl -v -H "Accept: application/json" -H "Content-type: application/json" -X POST -d ' {"user":{"first_name":"firstname","last_name":"lastname","email":"email@email.com","password":"app123","password_confirmation":"app123"}}' http://127.0.0.1:8000/api/insert



