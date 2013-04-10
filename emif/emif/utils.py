import logging
import re




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


    