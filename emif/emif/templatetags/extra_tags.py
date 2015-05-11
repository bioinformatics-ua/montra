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
import re

from django.contrib.auth.models import Group

from django.template.loader import render_to_string

from django import template
from django.template.defaultfilters import stringfilter

from questionnaire.models import Questionnaire
from fingerprint.models import AnswerRequest

import hashlib

from django.conf import settings

from accounts.models import Profile

from newsletter.models import Newsletter, Subscription

from djangosaml2.conf import config_settings_loader
from djangosaml2.utils import available_idps

register = template.Library()




@register.filter(name='removeh1')
@stringfilter
def removeh1(value):

    return value.replace('h1. ','')

@register.filter(name='clean')
@stringfilter
def clean(value):
    return value.replace('//','')

@register.filter(name='escapedots')
@stringfilter
def escapedots(value):
    print value.replace('.','\\\\.')
    return value.replace('.','\\\\.')


@register.filter(name='replaceplicas')
@stringfilter
def replaceplicas(value):
    return value.replace('"',"'")



@register.filter(name='removehs')
@stringfilter
def removehs(value):
    value = value.replace('h0. ','')
    value = value.replace('h1. ','')
    value = value.replace('h2. ','')
    value = value.replace('h3. ','')
    value = value.replace('h4. ','')
    value = value.replace('h5. ','')
    value = value.replace('h6. ','')
    value = value.replace('h7. ','')

    return value

@register.simple_tag()
def ans_requested(question, requests, *args, **kwargs):
    try:
        question_requests = requests.filter(question = question)

        if len(question_requests) > 0:
            return render_to_string('answer_requests.html', { "requests": question_requests })

    except AnswerRequest.DoesNotExist:
        pass

    return ""

@register.filter(name='datehhmm')
@stringfilter
def datehhmm(value):

    value = value[:-10]

    return value

@register.filter(name='trim')
@stringfilter
def trim(value):
    value = value.strip()

    return value

@register.filter(name='esc')
@stringfilter
def esc(value):
    return re.escape(value)

@register.filter(name='removedots')
@stringfilter
def removedots(value):
    value = value.replace('.','')

    return value

@register.filter(name='isnumber')
@stringfilter
def isnumber(value):
    return value.isdigit()


@register.filter(name='geths')
@stringfilter
def geths(value):
    value = value[0:2]
    return value


@register.filter(name='removespaces')
@stringfilter
def removespaces(value):
    value = value.replace('h1. ','')
    value = value.replace(',','')
    value = value.replace('/','')
    result = value.replace(' ','')

    return result

@register.filter(name='hash')
@stringfilter
def hash(value):
    return hashlib.sha224(value).hexdigest()

@register.filter(name='truncate')
@stringfilter
def truncate(value):
    result = value[:30]

    return result

@register.filter(name='captioned')
@stringfilter
def captioned(value):
    exclusion_list = ['publication', 'choice', 'choice-freeform','choice-multiple','choice-multiple-freeform','choice-multiple-freeform-options']

    return value not in exclusion_list

@register.filter(name='is_usecase')
@stringfilter
def is_usecase(value):

    return bool(re.match('use', value, re.I))

@register.filter
def whitespacesplit(str):
    words = []

    for m in re.finditer(r'"(.*?)"', str):
        words.append(m.group(1))
        str = str.replace(m.group(0), "")

    words = words + str.strip().split()

    return words

@register.filter(name='commasplit')
@stringfilter
def commasplit(str):
    words = []

    words = words + str.strip().split(',')

    return words

@register.filter
def ellipsis(str, size):
    if(len(str) > size):
        return str[:size]+"..."

    return str

@register.filter
def isDataCustodian(profiles):
    try:
        dc = Profile.objects.get(name="Data Custodian")

        if dc in profiles:
            return True
    except Profile.DoesNotExist:
        pass

    return False

@register.filter
def isResearcher(profiles):
    try:
        rs = Profile.objects.get(name="Researcher")

        if rs in profiles:
            return True
    except Profile.DoesNotExist:
        pass

    return False

def fingerprints_list():

    try:
        objs = Questionnaire.objects.filter(disable=False)
    except:
        pass
    results = {}
    for q in objs:
        results[q.id] = q.name


    return results

def fingerprints_list_user(user, use_slugs=False):

    interests = user.get_profile().interests.all()
    quests = []

    try:
        for inter in interests:
            if inter.disable==False:
                quests.append(inter)
    except:
        pass

    results = {}
    for q in quests:
        if use_slugs:
            results[q.slug] = q.name
        else:
            results[q.id] = q.name

    return results

def profiles_list_user(user):
    profiles = user.get_profile().profiles.all()
    results = {}
    for p in profiles:
        results[p.id] = p.name

    return results

def show_profiles(user):

    return {'profiles':profiles_list_user(user)}
register.inclusion_tag('reusable_blocks/menu_ttags_profiles.html')(show_profiles)

def show_fingerprints_interests_profile(user):

    return {'fingerprints':fingerprints_list_user(user)}
register.inclusion_tag('reusable_blocks/menu_ttags_interests.html')(show_fingerprints_interests_profile)

def show_fingerprints_interests(user):

    return {'fingerprints':fingerprints_list_user(user)}
register.inclusion_tag('reusable_blocks/menu_ttags.html')(show_fingerprints_interests)

@register.simple_tag
def show_subscription(user):
    link = None
    label = None
    try:
        newsl = Newsletter.objects.get(slug='emif-catalogue-newsletter')

        link="newsletter/"+newsl.slug+"/subscribe"
        label="Subscribe Newsletter"

        # create subscription
        user_sub = None
        try:
            subscription = Subscription.objects.get(user=user,  newsletter=newsl)

            if not subscription.unsubscribed:
                link = "newsletter/"+newsl.slug+"/unsubscribe"
                label = "Unsubscribe Newsletter"
        except:
            pass


    except Newsletter.DoesNotExist:
        print "Problem finding default newsletter"

    return '<a href="'+str(link)+'" class="navbar-link"><i class="fa fa-rss"></i>&nbsp;'+str(label)+'</a>'

def show_fingerprints():

    return {'fingerprints':fingerprints_list()}
register.inclusion_tag('reusable_blocks/menu_ttags.html')(show_fingerprints)


def show_fingerprints_for_search(user):

    return {'fingerprints':fingerprints_list_user(user)}
register.inclusion_tag('reusable_blocks/menu_ttags_for_search.html')(show_fingerprints_for_search)

def show_fingerprints_dropdown(user, sort_params):

    return {'fingerprints':fingerprints_list_user(user, use_slugs=True), 'sort_params': sort_params}
register.inclusion_tag('reusable_blocks/selectfdropdown.html')(show_fingerprints_dropdown)


def show_fingerprints_for_statistics():

    return {'fingerprints':fingerprints_list()}
register.inclusion_tag('reusable_blocks/menu_ttags_for_statistics.html')(show_fingerprints_for_statistics)



class GlobalVariable( object ):

    def __init__( self, varname, varval ):
        self.varname = varname
        self.varval  = varval

    def name( self ):
        return self.varname

    def value( self ):
        return self.varval

    def set( self, newval ):
        self.varval = newval


class GlobalVariableSetNode( template.Node ):

    def __init__( self, varname, varval ):
        self.varname = varname
        self.varval  = varval

    def render( self, context ):
        gv = context.get( self.varname, None )
        if gv:
            gv.set( self.varval )
        else:
            gv = context[self.varname] = GlobalVariable( self.varname, self.varval )
        return ''


def setglobal( parser, token ):
    try:
        tag_name, varname, varval = token.contents.split(None, 2)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires 2 arguments" % token.contents.split()[0])
    return GlobalVariableSetNode( varname, varval )

register.tag( 'setglobal', setglobal )


class GlobalVariableGetNode( template.Node ):

    def __init__( self, varname ):
        self.varname = varname

    def render( self, context ):
        try:
            return context[self.varname].value()
        except AttributeError:
            return ''

@register.simple_tag()
def multiply(a, b, *args, **kwargs):
    # you would need to do any localization of the result here
    return a * b

def getglobal( parser, token ):
    try:
        tag_name, varname = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
    return GlobalVariableGetNode( varname )


register.tag( 'getglobal', getglobal )

class GlobalVariableIncrementNode( template.Node ):
  def __init__( self, varname ):
    self.varname = varname
  def render( self, context ):
    gv = context.get( self.varname, None )
    if gv is None:
      return ''
    gv.set( int(gv.value()) + 1 )
    return ''
def incrementglobal( parser, token ):
  try:
    tag_name, varname = token.contents.split(None, 1)
  except ValueError:
    raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
  return GlobalVariableIncrementNode(varname)

register.tag( 'incrementglobal', incrementglobal )

class VersionNode( template.Node ):
  def __init__( self, varname ):
    self.varname = varname
  def render( self, context ):
    return get_version()

def get_version():
    return settings.VERSION + " " + settings.VERSION_DATE

def get_version_tag(parser, token):
    return VersionNode('')
register.tag( 'get_version', get_version_tag )


@register.simple_tag
def slogan():
    return "Discover the right data for your research"


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

@register.simple_tag
def idps_dropdown():
    return render_to_string('reusable_blocks/idp_dropdowns.html',
        {
            "idps": available_idps(config_settings_loader()).items(),
            "base": settings.BASE_URL
        })
