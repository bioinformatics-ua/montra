#!python
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

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import SearchView
from api.views import SearchDatabasesView
from api.views import EmailCheckView
from api.views import RemovePermissionsView
from api.views import PopulationCheckView
from api.views import GetFileView
from api.views import DeleteFileView
from api.views import MetaDataView
from api.views import StatsView
from api.views import ValidateView
from api.views import PublicationsView
from api.views import PopulationView
from api.views import NotifyOwnerView
from api.views import AddPublicLinkView
from api.views import DeletePublicLinkView
from api.views import SearchSuggestionsView
from api.views import NotificationsView
from api.views import ReadNotificationView
from api.views import RemoveNotificationView
from api.views import RequestAnswerView

from api.views import ToggleSubscriptionView

from dashboard.api import *

urlpatterns = patterns('api.views',
    url(r'^root/$', 'api_root'),
    url(r'^emailcheck$', EmailCheckView.as_view(), name='emailcheck'),
    url(r'^removePermissions$', RemovePermissionsView.as_view(), name='removepermissions'),
    url(r'^populationcheck$', PopulationCheckView.as_view(), name='populationcheck'),
    url(r'^getfile$', GetFileView.as_view(), name='getfile'),
    url(r'^deletefile$', DeleteFileView.as_view(), name='deletefile'),
    url(r'^search$', SearchView.as_view(), name='search'),
    url(r'^metadata', MetaDataView.as_view(), name='metadata'),
    url(r'^stats$', StatsView.as_view(), name='stats'),
    url(r'^validate$', ValidateView.as_view(), name='validate'),
    url(r'^pubmed$', PublicationsView.as_view(), name='pubmed'),
    url(r'^population$', PopulationView.as_view(), name='population'),
    url(r'^notify_owner$', NotifyOwnerView.as_view(), name='notify_owner'),
    url(r'^addpubliclink$', AddPublicLinkView.as_view(), name='addpubliclink'),
    url(r'^deletepubliclink$', DeletePublicLinkView.as_view(), name='addpubliclink'),
    url(r'^searchsuggestions$', SearchSuggestionsView.as_view(), name='searchsuggestions'),

    url(r'^notifications$', NotificationsView.as_view(), name='notifications'),
    url(r'^readnotification$', ReadNotificationView.as_view(), name='readnotification'),
    url(r'^removenotification$', RemoveNotificationView.as_view(), name='removenotification'),
    url(r'^requestanswer$', RequestAnswerView.as_view(), name='requestanswer'),

    url(r'^togglesubscription$', ToggleSubscriptionView.as_view(), name='togglesubscription'),

    # search databases services
    url(r'^searchdatabases$', SearchDatabasesView.as_view(), name='searchdatabases'),

    # dashboard widgets services
    url(r'^dbtypes$', DatabaseTypesView.as_view(), name='dbtypes'),
    url(r'^userstats$', UserStatsView.as_view(), name='userstats'),
    url(r'^mostviewed$', MostViewedView.as_view(), name='mostviewed'),
    url(r'^mostviewedfingerprint$', MostViewedFingerprintView.as_view(), name='mostviewedfingerprint'),
    url(r'^lastusers$', LastUsersView.as_view(), name='lastusers'),
    url(r'^feed$', FeedView.as_view(), name='feed'),
    url(r'^tagcloud$', TagCloudView.as_view(), name='tagcloud'),
    url(r'^topusers$', TopUsersView.as_view(), name='topusers'),
    url(r'^recommendations$', RecommendationsView.as_view(), name='recommendations'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
