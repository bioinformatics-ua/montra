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
from django.shortcuts import render, redirect

from django.http import HttpResponse

from emif.models import AdvancedQuery, AdvancedQueryAnswer
from emif.views import results_diff, RequestMonkeyPatch
from emif.models import QueryLog

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def history_defer(request, template_name='history.html'):
    return history(request, '0', 1)

def history_defer_advanced(request, template_name='history.html'):
    return history(request, '1', 1)

def history(request, source, page, page_rows=10, template_name='history.html'):

    if not request.user.is_authenticated():
        return HttpResponse( "Must be logged in to see query history", status=403)

    queries = AdvancedQuery.objects.filter(user=request.user, removed=False).order_by('-date')

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
    
    simple_queries = QueryLog.objects.filter(user=request.user, removed = False).order_by('-created_date')

    myPaginator = Paginator(simple_queries, page_rows)

    myadvancedPaginator = Paginator(queries, page_rows)

    if source == '0':
        try:
            pager_simple =  myPaginator.page(page)
        except PageNotAnInteger, e:
            pager_simple =  myPaginator.page(1)

        pager = myadvancedPaginator.page(1)

    else:

        try:
            pager =  myadvancedPaginator.page(page)
        except PageNotAnInteger, e:
            pager =  myadvancedPaginator.page(1)

        pager_simple = myPaginator.page(1)

    return render(request, template_name, {'request': request, 'source': source, 'breadcrumb': True, 'queries_simple': pager_simple, 'queries': pager, 'page_rows':page_rows})


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

def resultsdiff_historysimple(request, query_id, template_name='history.html'):

    # monkey patch answers into query
    request2 = RequestMonkeyPatch()
    
    request2.method = request.method    
    query = None
    try:
        query = QueryLog.objects.get(id=query_id)
    except:
        print '-- Error: Cant find free text query with id '+str(query_id)
        pass

    # Theres probably a better way to clone and change an httprequest, but i dont know none
    # not could i find them, i needed to create a monkeypatch to send to the results_diff, but this monkey
    # patch had to be like a real httprequest...

    request2.get_post()['query'] = query.query

    request2.set_session(request.session)

    request2.set_user(request.user)

    request2.set_meta(request.META)

    request2.set_cookies(request.COOKIES)

    request2.set_host(request.get_host())

    return results_diff(request2)

def remove(request, query_id):
    if not request.user.is_authenticated():
        raise Http404
        
    try:
        query = AdvancedQuery.objects.get(id=query_id)

        query.removed = True

        query.save()

    except:
        print '-- Error: Cant find advanced query with id '+str(query_id)
        pass

    request.session['deleted_query_id'] = True
    return redirect('advancedsearch.views.history_defer_advanced')

def removesimple(request, query_id):
    if not request.user.is_authenticated():
        raise Http404
        
    try:
        query = QueryLog.objects.get(id=query_id)

        query.removed = True

        query.save()

    except:
        print '-- Error: Cant find free text query with id '+str(query_id)
        pass

    request.session['deleted_query_id'] = True
    return redirect('advancedsearch.views.history_defer')

def remove_all(request):
    if not request.user.is_authenticated():
        raise Http404
        
    queries = AdvancedQuery.objects.filter(user=request.user)

    for query in queries:
        query.removed = True

        query.save()

    request.session['deleted_query_id'] = True
    return redirect('advancedsearch.views.history_defer_advanced')

def remove_allsimple(request):
    if not request.user.is_authenticated():
        raise Http404
        
    queries = QueryLog.objects.filter(user=request.user)

    for query in queries:
        query.removed = True

        query.save()

    request.session['deleted_query_id'] = True
    return redirect('advancedsearch.views.history_defer')
