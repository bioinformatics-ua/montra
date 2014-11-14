# Create your views here.
# -*- coding: utf-8 -*-
# Copyright (C) 2014 Ricardo F. Gonçalves Ribeiro and Universidade de Aveiro
#
# Authors: Ricardo F. Gonçalves Ribeiro <ribeiro.r@ua.pt>
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

from django.shortcuts import render

from django.core import serializers
from django.conf import settings
from django.http import *
from django.http import Http404

from geopy import geocoders

from fingerprint.listings import get_databases_from_solr
from emif.models import City

from geolocation.services import *

from questionnaire.models import Questionnaire

def geo(request, template_name='geo.html'):

    query = None
    isAdvanced = False
    if(request.session.get('isAdvanced') == True):
        query = request.session.get('query')
        if query == None:
            query = "*:*"

        isAdvanced = True
    else:
        if(request.session.get('query') != None):
            query = "'"+re.sub("['\"']","\\'",request.session.get('query'))+"'"
            query = "text_t:"+query

        else:
            query = "*:*"

    #print "query@" + query
    list_databases = get_databases_from_solr(request, query)

    list_locations = []
    _long_lats = []
    # since the geolocation is now adding the locations, we no longer need to look it up when showing,
    # we rather get it directly
    db_list = {}
    questionnaires_ids = {}
    qqs = Questionnaire.objects.all()
    for q in qqs:
        questionnaires_ids[q.slug] = (q.pk, q.name)
    for database in list_databases:

        if database.location.find(".")!= -1:
            _loc = database.location.split(".")[0]
        else:
            _loc = database.location

        city=None
        g = geocoders.GeoNames(username='bastiao')

        if _loc!= None and g != None and len(_loc)>1:
            #try:
            #    place, (lat, lng) = g.geocode(_loc)
            #except:
            #    continue
            try:
                city = City.objects.filter(name=_loc.lower())[0]

            # if dont have this city on the db
            except:
                print "-- Error: The city " + _loc + " doesnt exist on the database. Maybe too much requests were being made when it happened ? Trying again..."

                #obtain lat and longitude
                city = retrieve_geolocation(_loc.lower())

                if city != None:
                    #print city

                    city.save()

                else:
                    print "-- Error: retrieving geolocation"
                    continue

            _long_lats.append(str(city.lat) + ", " + str(city.long))
            import pdb
            #pdb.set_trace()
            def __cleanvalue(v):
                return v.encode('ascii', 'ignore').strip().replace('\n', ' ').replace('\r', ' ')


            def db_ready(database, city):
                return {    'name': database.name,
                            'location': __cleanvalue(database.location),
                            'institution': __cleanvalue(database.institution),
                            'contact': __cleanvalue(database.email_contact),
                            'number_patients': __cleanvalue(database.number_patients),
                            'ttype': __cleanvalue(database.type_name),
                            'id' : database.id,
                            'admin_name': __cleanvalue(database.admin_name),
                            'admin_address': __cleanvalue(database.admin_address),
                            'admin_email': __cleanvalue(database.admin_email),
                            'admin_phone': __cleanvalue(database.admin_phone),
                            'scien_name': __cleanvalue(database.scien_name),
                            'scien_address': __cleanvalue(database.scien_address),
                            'scien_email': __cleanvalue(database.scien_email),
                            'scien_phone': __cleanvalue(database.scien_phone),
                            'tec_name': __cleanvalue(database.tec_name),
                            'tec_address': __cleanvalue(database.tec_address),
                            'tec_email': __cleanvalue(database.tec_email),
                            'tec_phone': __cleanvalue(database.tec_phone),
                            'lat' : str(city.lat),
                            'long': str(city.long),
                        }

            if((city.lat, city.long) in db_list):
                db_list[(city.lat, city.long)].append(db_ready(database, city))
            else:
                db_list[(city.lat, city.long)] = [db_ready(database, city)]

        list_locations.append(_loc)

    return render(request, template_name, {'request': request, 'db_list' : db_list,
                                           'search_old': request.session.get('query',''),
                                           'list_cities': list_locations,
                                           'lats_longs': _long_lats,
                                           'breadcrumb': True, 'isAdvanced': isAdvanced})
