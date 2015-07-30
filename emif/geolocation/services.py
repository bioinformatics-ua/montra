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
# Adds a city to the internal database of cities with his location (if it doesnt exist yet)
# receives as input a qlist

from emif.models import City
from geopy import geocoders
from constance import config
from fingerprint.listings import get_databases_from_solr
from questionnaire.models import Questionnaire


def get_locations(request):
    if not config.geolocation:
        raise Http404

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

    return ( {'request': request, 'db_list' : db_list,
                                           'search_old': request.session.get('query',''),
                                           'list_cities': list_locations,
                                           'lats_longs': _long_lats,
                                           'breadcrumb': True,
                                           'isAdvanced': isAdvanced})

def add_city(qlist_general):
    # iterate until we find the location field (City or location fields)
    for qs_aux, qlist in qlist_general:
        for question, qdict in qlist:

            if question.text == 'Location' or question.text == 'City':
                city_name = qdict['value'].lower()
                # check if the city is on the db
                try:
                    city = City.objects.get(name=city_name)

                    #print "-- City already is on the db."
                # if dont have this city yet on the db
                except City.DoesNotExist:
                    #print "City "+qdict['value'].lower()+" is not on the db yet"

                    #obtain lat and longitude
                    city = retrieve_geolocation(city_name)

                    if city != None:
                        print city

                        city.save()
                        return True

                    else:
                        print "-- Error: retrieving geolocation"
                        return False


    #print "-- No city found at all on questionary"
    return False

def retrieve_geolocation(city_name):

    try:
        #g = geocoders.GeoNames(username='bastiao')
        g = geocoders.GoogleV3()

        if g == None:
            return None

        place, (lat, lng) = g.geocode(city_name)

        # add to the db
        city = City(name=city_name, lat=lat, long=lng)

        return city

    except:
        return None
