import logging
import re
from searchengine.models import Nomenclature
from datetime import datetime
from searchengine.search_indexes import CoreEngine
from searchengine.models import Slugs

def convert_text_to_slug(text):
    #TODO: optimize
    return text.replace(' ', '_').replace('?','').replace('.', '').replace(',','')


def clean_value(v):
    if isinstance(v, str):
        logging.debug("Value: " + v)
        print "Value: " + v

        v = re.sub(r"\[|\]", "", v)
        logging.debug("Value after clean: " + v)
    elif isinstance(v, list):
        print "list"
        for v_aux in v:
            v += v_aux + " "
    return v

def convert_date(d):
    new_date = datetime.strptime(d, '%Y-%m-%d %H:%M:%S.%f')
    return new_date.strftime("%Y-%m-%d %H:%M")


def get_nomenclature(institution_name, database_name):
    """
    Get the nomenclature to the database based on institution name 
    """
    value = clean_value(institution_name+"_"+database_name)
    slug = convert_text_to_slug(value)
    return slug



def database_exists(database_name):
    """
    Verify if the nomenclature database name already exists
    """
    results = Nomenclature.objects.filter(name=database_name)
    if len(results)==0:
        return False
    else:
        return True

class Database:
    id = ''
    name = ''
    date = ''
    institution = ''
    location = ''
    email_contact = ''
    number_patients = ''


class Tag:
    tag = ''
    value = ''


def get_database_from_id(id):
    c = CoreEngine()
    results = c.search_fingerprint("id:"+id)
    database_aux = None
    for r in results:
        try:
            database_aux = Database()
            print r['id']
            print r['created_t']
            print r['database_name_t']
            database_aux.id = r['id']
            database_aux.date = convert_date(r['created_t'])
           
            database_aux.name = r['database_name_t']
            
            break
        except:
            pass
    return database_aux

def get_database_from_id_with_tlv(db):
    c = CoreEngine()
    results = c.search_fingerprint('id:'+db.id)
    class Tag:
        tag = ''
        value = ''

    list_values = []
    blacklist = ['created_t', 'type_t', '_version_']
    name = "Not defined"
    
    for result in results:
        for k in result:
            if k in blacklist:
                continue
            t = Tag()
            results = Slugs.objects.filter(slug1=k)
            if len(results)>0:
                text = results[0].description 
            else:
                text = k
            info = text[:75] + (text[75:] and '..')

            t.tag = info

            value = clean_value(str(result[k]))
            value = value[:75] + (value[75:] and '..')
            t.value = value
            if k== "database_name_t":
                name = t.value
            list_values.append(t)
        break
    db.fields = list_values
    return db


WORKSPACE_PATH={'Workspace'}




    