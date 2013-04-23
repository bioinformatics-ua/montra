#!/usr/bin/env python
# -*- coding: utf-8 -*- 

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

institutionnames = ["Hospital", "Medical Department", "Research Center", "Pharmacy", "Hopital", "Ziekenhuis" ]

databasenames =["heartattack", "cardiomyopathy", "Coronary heart disease", "Valvular heart disease", "Peripheral arterial disease"]

location = ["Paris", "Roterdao", 
"Porto", "Aveiro", "Lisboa", "Faro", "Portimao", "Brussels", "London", 
"Barcelona", "Heildeberg", "Stuttgard", "Lens"]

data = {
        'contact_technical_t':'IEETA',
        'created_t':'2013-04-17 12:09:32.334053',
        'location_t':'Aveiro',
        'institution_name_t':'IEETA',
        'contact_scientific_t':'jlo@ua.pt',
        'contact_administrative_t':'jlo@ua.pt',
        'type_t':'researchcohorts',
        'id':'a10815736f733d04d8e0aa65fe37',
        'user_t' :'bastiao',
        'text_t': 'ieeta ieeta bastiao emif cardiomyopathy Coronary heart attack',
        'total_number_subjects_t': '20000',
        'ethical_committee_t': '[No]',
        'publically_doc_procedure_t': '[No]',
        'ethical_committee_t': '[No]',
        'number_active_patients_jan2012_t': '200',
        'average_time_follow_up_t': '130',
        'assess_prevalence_prevalence_t': 'Brufen Beneron',
        'literature_papers_t': "Luis A. Bastiao Silva, Carlos Costa, Jose Luis Olveira. A Secure PACS Cloud Archive in CARS 2011, Berlin, Germany ",
        'population_description_t':'Fat, Headcache'}

import pysolr
import random
solr = pysolr.Solr('http://localhost:8983/solr', timeout=10)
for i in range(10):
        index_db = random.randint(1, len(databasenames))
        index_institutionnames = random.randint(1, len(institutionnames))
        index_locations = random.randint(1, len(location))

	data['database_name_t'] = institutionnames[index_institutionnames-1] + " " + location[index_locations-1] + " " +databasenames[index_db-1]
        data['location_t'] = location[index_locations]
	data['id'] = generate_hash()
	solr.add([data])
	
	solr.optimize()


#curl -v -H "Accept: application/json" -H "Content-type: application/json" -X POST -d ' {"user":{"first_name":"firstname","last_name":"lastname","email":"email@email.com","password":"app123","password_confirmation":"app123"}}' http://127.0.0.1:8000/api/insert



