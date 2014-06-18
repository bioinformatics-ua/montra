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

##
#   See user history of queries
##
from django.shortcuts import render

from emif.models import AdvancedQuery, AdvancedQueryAnswer
from emif.views import results_diff, RequestMonkeyPatch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def history_defer(request, template_name='history.html'):
    return history(request, 1)

def history(request, page, page_rows=10, template_name='history.html'):

    queries = AdvancedQuery.objects.filter(user=request.user).order_by('-date')

        ## Paginator ##
    if(request.method == 'POST'):
        try:
            page_rows = int(request.POST.get('paginator_rows', 10))

            request.session['paginator_rows'] = page_rows
        except: 
            pass
    else:
        try:
            page_rows = int(request.session['paginator_rows'])
        except:
            pass
    
    myPaginator = Paginator(queries, page_rows)
    try:
        pager =  myPaginator.page(page)
    except PageNotAnInteger, e:
        pager =  myPaginator.page(1)
    ## End Paginator ##

    return render(request, template_name, {'request': request, 'queries': pager, 'page_rows':page_rows})


def resultsdiff_history(request, query_id, template_name='history.html'):

    # monkey patch answers into query
    request2 = RequestMonkeyPatch()
    
    request2.method = request.method    
    query = None
    try:
        query = AdvancedQuery.objects.get(id=query_id)
    except:
        print '-- Error: Cant find advanced query with id '+str(query_id)
        pass

    this_answers = AdvancedQueryAnswer.objects.filter(refquery=query)

    # Theres probably a better way to clone and change an httprequest, but i dont know none
    # not could i find them, i needed to create a monkeypatch to send to the results_diff, but this monkey
    # patch had to be like a real httprequest...

    request2.get_post()['qid'] = str(query.qid.id)

    request2.get_post()['boolrelwidget-boolean-serialization'] = query.serialized_query

    request2.set_session(request.session)

    request2.set_user(request.user)

    request2.set_meta(request.META)

    request2.set_cookies(request.COOKIES)

    request2.set_host(request.get_host())

    for answer in this_answers:
        request2.get_post()[answer.question] = answer.answer

    return results_diff(request2)
