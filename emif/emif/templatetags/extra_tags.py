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
#
import re
from django import template
from django.template.defaultfilters import stringfilter

from questionnaire.models import Questionnaire

register = template.Library()

@register.filter(name='removeh1')
@stringfilter
def removeh1(value):
    
    return value.replace('h1. ','')


@register.filter(name='removehs')
@stringfilter
def removehs(value):
    value = value.replace('h1. ','')
    value = value.replace('h2. ','')
    value = value.replace('h3. ','')
    value = value.replace('h4. ','')
    value = value.replace('h5. ','')
    value = value.replace('h6. ','')
    value = value.replace('h7. ','')

    return value



@register.filter(name='removedots')
@stringfilter
def removedots(value):
    value = value.replace('.','')
    
    return value


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
    result = value.replace(' ','')

    return result


@register.filter(name='truncate')
@stringfilter
def truncate(value):
    result = value[:30]

    return result


# def fingerprints_list():

#     objs = Questionnaire.objects.all()
#     results = {}
#     for q in objs:
#         results[q.id] = q.name
#     print results

#     return results

def fingerprints_list():
    
    try:
        objs = Questionnaire.objects.filter(disable=False)
    except:
        pass
    results = {}
    for q in objs:
        results[q.id] = q.name
    

    return results


def show_fingerprints():
    
    return {'fingerprints':fingerprints_list()}
register.inclusion_tag('menu_ttags.html')(show_fingerprints)


def show_fingerprints_for_search():
    
    return {'fingerprints':fingerprints_list()}
register.inclusion_tag('menu_ttags_for_search.html')(show_fingerprints_for_search)


def show_fingerprints_for_statistics():

    return {'fingerprints':fingerprints_list()}
register.inclusion_tag('menu_ttags_for_statistics.html')(show_fingerprints_for_statistics)



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