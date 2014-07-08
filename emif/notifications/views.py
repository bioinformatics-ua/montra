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
from django.http import HttpResponse
from notifications.models import Notification
from emif.views import define_rows
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def see_notifications_defer_all(request, template_name='notifications.html'):
    return see_notifications(request, '0', 1, template_name=template_name)

def see_notifications_defer_page(request, source, template_name='notifications.html'):
    return see_notifications(request, source, 1, template_name=template_name)

def see_notifications(request, source, page, template_name='notifications.html'):

    if not request.user.is_authenticated():
        return HttpResponse("Must be logged in to see notifications", status=403)

    rows = define_rows(request)

    notifications = Notification.objects.filter(destiny=request.user, type=Notification.SYSTEM, 
                                                removed=False).order_by('-created_date')

    notifications_unread = notifications.filter(read=False)
    notifications_read = notifications.filter(read=True)

    myPaginator = Paginator(notifications, rows)
    myPaginator_unread = Paginator(notifications_unread, rows)
    myPaginator_read = Paginator(notifications_read, rows)

    pager=pager_unread=pager_read=None

    if source == '0' :
        try:
            pager =  myPaginator.page(page)
        except PageNotAnInteger, e:
            pager =  myPaginator.page(1)

        pager_unread = myPaginator_unread.page(1)
        pager_read = myPaginator_read.page(1)

    elif source == '1' :
        try:
            pager_unread =  myPaginator_unread.page(page)
        except PageNotAnInteger, e:
            pager_unread =  myPaginator_unread.page(1)

        pager = myPaginator.page(1)
        pager_read = myPaginator_read.page(1) 
    elif source == '2' :
        try:
            pager_read =  myPaginator_read.page(page)
        except PageNotAnInteger, e:
            pager_read =  myPaginator_read.page(1)

        pager = myPaginator.page(1)
        pager_unread = myPaginator_unread.page(1)          

    return render(request, template_name, 
        {   'request': request, 
            'notifications': pager,
            'notifications_unread': pager_unread,
            'notifications_read': pager_read,
            'breadcrumb': True,
            'page_rows': rows,
            'source': source
        })
