import logging
import re
from searchengine.models import Nomenclature



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
    


WORKSPACE_PATH={'Workspace'}




    