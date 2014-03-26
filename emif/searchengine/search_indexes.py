# -*- coding: utf-8 -*-
# Copyright (C) 2013 Luís A. Bastião Silva and Universidade de Aveiro
#
# Authors: Luís A. Bastião Silva <bastiao@ua.pt>
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

"""A module for Python index

.. moduleauthor:: Luís A. Bastião Silva <bastiao@ua.pt>
"""

from __future__ import print_function
import pysolr

from questionnaire.models import RunInfoHistory

from django.db.models.signals import post_save
from django.dispatch import receiver

from questionnaire.models import *
from searchengine.models import Slugs

from django.db.models.signals import post_save
from django.dispatch import receiver

import logging
import ast

import md5
import random

from django.conf import settings


from django.template.defaultfilters import slugify

import datetime
logger = logging.getLogger()

def generate_hash():
    hash = md5.new()
    hash.update("".join(map(lambda i: chr(random.randint(0, 255)), range(16))))
    hash.update(settings.SECRET_KEY)
    key = hash.hexdigest()
    return key

class CoreEngine:
    """It is responsible for index the documents and search over them
    It also connects to SOLR
    """
    
    CONNECTION_TIMEOUT_DEFAULT = 10
    def __init__(self, timeout=CONNECTION_TIMEOUT_DEFAULT):
        # Setup a Solr instance. The timeout is optional.
        self.solr = pysolr.Solr('http://' +settings.SOLR_HOST+ ':'+ settings.SOLR_PORT+'/solr', timeout=timeout)




    def index_fingerprint(self, doc):
        """Index fingerprint 
        """
        # index document
        self.index_fingerprint_as_json(doc)
    
    def index_fingerprint_as_json(self, d):
        """Index fingerprint as json
        """
        # index document
        
        xml_answer = self.solr.add([d])
        print(xml_answer)
        self.optimize()

    def optimize(self):
        """This function optimize the index. It improvement the search and retrieve documents subprocess.
        However, it is a hard tasks, and call it for every index document might not be a good idea.
        """
        self.solr.optimize()

    def update(self, doc):
        """Update the document
        """
        # Search  and identify the document id

        self.solr.add([doc])


    def delete(self, id_doc):


        """Delete the document
        """
        self.solr.delete(id=id_doc)

    def search_fingerprint(self, query, start=0, rows=100, fl='', sort=''):
        """search the fingerprint
        """
        # Later, searching is easy. In the simple case, just a plain Lucene-style
        # query is fine.

        results = self.solr.search(query,**{
                'rows': rows,
                'start': start,
                'fl': fl,
                'sort': sort
                })
        return results

    def search_highlight(self, query, start=0, rows=100, fl='', sort='', hlfl=""):
        """search the fingerprint
        """
        #hl=true&hl.fl=text_t
        results = self.solr.search(query,**{
                'rows': rows,
                'start': start,
                'fl': fl,
                'sort': sort,
                'hl':"true",
                'hl.fl': hlfl, "hl.fragsize":0
                })
        return results

    def highlight_questions(self, query, start=0, rows=1000, fl='id', sort='', hlfl="*"):
        """search the fingerprint
        """
        #hl=true&hl.fl=text_t
        query = "qs_all:"+query
        print(query)
        results = self.solr.search(query,**{
                'rows': rows,
                'start': start,
                'fl': fl,
                'sort': sort,
                'hl':"true",
                'hl.fl': hlfl
                })
        return results

    def more_like_this(self, id_doc):
        similar = self.solr.more_like_this(q='id:doc_2', mltfl='text')
        return similar


def convert_text_to_slug_old(text):
    #TODO: optimize
    text_aux = text.replace(' ', '_').replace('?','').replace('.', '').replace(',','')
    if text_aux[:-1] == '_':
        text_aux = text_aux[:-1]
    return text_aux

def convert_text_to_slug(text):
    return slugify(text)

def clean_answer(answer):
    #TODO: optimize
    return answer


def get_slug_from_choice(v, q):
    choice = Choice.objects.filter(question=q).filter(value=v)
    if (len(choice)>0):
        print(choice[0].text)
        print(choice[0].value)



def index_answeres_from_qvalues(qvalues, questionnaire, subject, fingerprint_id, extra_fields=None, created_date=None):
    
    c = CoreEngine()
    d = {}
    
    text = ""
    slugs_objs = Slugs.objects.all()
    slugs = []
    for s in slugs_objs:
        slugs.append(s.description)
    appending_text = ""
    slugs_objs = None
    now = datetime.datetime.now()

    for qs_aux, qlist in qvalues:
        for question, qdict in qlist:

            try:
                choices = None
                value = None
                choices_txt = None
                if qdict.has_key('value'):
                    value = qdict['value']

                    if "yes" in qdict['value']:
                        appending_text += question.text

                elif qdict.has_key('choices'):
                    #import pdb
                    #pdb.set_trace()     
                    choices = qdict['choices']
                    qv = ""
                    try:
                        qv = qdict['qvalue']

                    except:
                        # raise
                        pass

                    value = qv
                    
                    do_again = False
                    try:
                        if len(choices[0])==3:
                            for choice, unk, checked  in choices:
                                if checked == " checked":
                                    value = value + "#" + choice.value   
                                    
                        elif len(choices[0])==4:
                            for choice, unk, checked, _aux  in choices:
                                if checked == " checked":
                                    if _aux != "":
                                        value = value + "#" + choice.value + "{" + _aux +"}"
                                    else:
                                        value = value + "#" + choice.value
                                    

                        elif len(choices[0])==2:
                            for checked, choice  in choices:
                                # print("checked" + str(checked))
                                if checked:
                                    value = value + "#" + choice.value
                                    
                    except:
                        do_again = True

                    if do_again:
                        for checked, choice  in choices:
                            # print("checked" + str(checked))
                            if checked:
                                
                                value = value + "#" + choice.value
                                

                    # print("choice value " + value)

                    '''
                    TO-DO
                    Verify if symbols || (separator) is compatible with solr
                    '''
                    #Save in case of extra field is filled
                    if qdict.has_key('extras'):
                        extras = qdict['extras']
                        # print("EXTRAS: " + str(extras))
                        for q, val in extras:
                            # print("VAL: " + str(q) + " - " + str(val))
                            if val:
                                value = value + "||" + val

                
                else:
                    #print("continue")
                    pass


                # print(value)
                slug = question.slug_fk.slug1
                #slug = question.slug
                # slug_aux = ""
                # if len(slug)>2:
                #     slug = question.slug
                # else:
                #     slug = convert_text_to_slug(question.text)
                slug_final = slug+"_t"
                #results = Slugs.objects.filter(description=question.text)
                
                #if slugs_dict==None or len(results)==0:
                # if question.text not in slugs:
                #     slugsAux = Slugs()
                #     slugsAux.slug1 = slug_final
                #     slugsAux.description = question.text
                #     slugsAux.question = question
                #     slugsAux.save()

                d[slug_final] = value
                if value!=None:
                    text += value + " " 
            except:
                # raise
                pass
                
    # print("Indexing...")
    results = c.search_fingerprint("id:"+fingerprint_id)
    if (len(results)>0):
        c.delete(results.docs[0]['id'])


    d['id']=fingerprint_id

    d['type_t']=questionnaire.name.replace(" ", "").lower()
    if created_date==None:
        d['created_t']= now.strftime('%Y-%m-%d %H:%M:%S.%f')
    else:
        d['created_t'] = created_date
    d['date_last_modification_t']= now.strftime('%Y-%m-%d %H:%M:%S.%f')
    d['user_t']= subject
    d['text_t']= text + " " + appending_text

    if extra_fields!=None:
        d = dict(d.items() + extra_fields.items())
        
    c.index_fingerprint_as_json(d)


def convert_answers_to_solr(runinfo):
    c = CoreEngine()
    
    runid = runinfo.runid
    answers = Answer.objects.filter(runid=runid)

    print(answers)
    d = {}
    text = ""
    for a in answers:
        print("Answer text: " + a.answer)
        print("Q: " + a.question.text)
        print("Slug:" + a.question.slug_fk.slug1)
        #print("Slug:" + a.question.slug)

        #slug = a.question.slug
        slug = a.question.slug_fk.slug1 
        
        slug_aux = ""
        #if len(slug)>2:
        slug = a.question.slug_fk.slug1
        #slug = a.question.slug
        #else:
        #    slug = convert_text_to_slug(a.question.text)
        slug_final = slug+"_t"

        results = Slugs.objects.filter(description=a.question.text)
        
        if results==None or len(results)==0:
            slugs = Slugs()
            slugs.slug1 = slug_final
            slugs.description = a.question.text
            slugs.question = a.question
            slugs.save()

        text_aux = ""
        print(a.question.get_type() )
        # Verify the question type

        if a.question.get_type() == "open" or \
        a.question.get_type() == "open-button" \
        or a.question.get_type() == "open-textfield" :
            x = ast.literal_eval(a.answer)
            text_aux = x[0]

        elif a.question.get_type() == "choice-yesnocomment" or \
        a.question.get_type() == "choice-yesnodontknow" or \
        a.question.get_type() == "choice" or \
        a.question.get_type() == "choice-freeform" or \
        a.question.get_type() == "choice-multiple" or \
        a.question.get_type() == "choice-multiple-freeform" or \
        a.question.get_type() == "comment":

            x = None 
            if (len(text_aux)>0):
                x = ast.literal_eval(text_aux)
       
                continue
            if not x is None:
                for v in x:
                    print(get_slug_from_choice(v, a.question))
                    text_aux += v + " "
            
        else:
            text_aux = a.answer

        d[slug_final] = text_aux
        text += text_aux + " " 
    print(d)
    d['id']=runid
    d['type_t']=runinfo.questionnaire.name.replace(" ", "").lower()

    d['created_t']=str(runinfo.completed)
    text += text_aux + runid + " " +str(runinfo.completed)
    d['text_t']= text
    c.index_fingerprint_as_json(d)


@receiver(post_save, sender=RunInfoHistory)
def index_handler(sender, **kwargs):
    # Check if it is advanced search or not.
    # If it is advanced search, it is not necessary to index
    # Otherwise the index will be necessary

    print("#### Indexing now ###############")
    logger.debug(sender)
    for key in kwargs:
        logger.debug("another keyword arg: %s: %s" % (key, kwargs[key]))
    runinfo = kwargs["instance"]
    try:
        convert_answers_to_solr(runinfo)
    except:
        print("Error, go here")
        raise

