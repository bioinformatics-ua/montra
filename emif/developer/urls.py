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
from django.conf.urls.defaults import *
from views import *

from api import *

urlpatterns = patterns('',
    # developer list view
    url(r'^$', DeveloperListView.as_view()),
    url(r'^add$', DeveloperAddView.as_view()),
    url(r'^save/$', DeveloperPluginSaveView.as_view()),

    url(r'^docs$', DeveloperDocsView.as_view()),

    url(r'^(?P<plugin_hash>[^/]+)$', DeveloperDetailView.as_view(), name='developer-detail'),
    url(r'^(?P<plugin_hash>[^/]+)/(?P<version>[0-9]+)$', DeveloperVersionView.as_view(), name='developer-version'),
    url(r'^(?P<plugin_hash>[^/]+)/(?P<version>[0-9]+)/deps$', DeveloperDepsView.as_view(), name='developer-deps'),
    url(r'^(?P<plugin_hash>[^/]+)/add$', DeveloperVersionView.as_view(), name='developer-version-add'),

    #live preview
    url(r'^live/(?P<version_id>[0-9]+)/$',
        DeveloperLiveAdminView.as_view(), name='developer-live-admin'),

    url(r'^live/(?P<plugin_hash>[^/]+)/(?P<version>[0-9]+)$',
        DeveloperLiveView.as_view(), name='developer-live'),

    # API urls
    url(r'^checkname/$', CheckNameView.as_view()),
    url(r'^deletedep/$', DeleteDepView.as_view()),


    # Globalproxy
    url(r'^api/databaseSchemas/$', DatabaseSchemasView.as_view()),
    url(r'^api/getProfileInformation/$', getProfileInformationView.as_view()),
    url(r'^api/getFingerprints/$', getFingerprintsView.as_view()),
    url(r'^api/getFingerprints/(?P<quest_slug>[^/]+)$', getFingerprintsView.as_view()),

    # FingerprintProxy
    url(r'^api/getFingerprintUID/(?P<fingerprint>[^/]+)$', getFingerprintUIDView.as_view()),
    url(r'^api/getAnswers/(?P<fingerprint>[^/]+)$', getAnswersView.as_view()),

    # datastore
    url(r'^api/store/getExtra/(?P<fingerprint>[^/]+)$', getExtraView.as_view()),

    url(r'^api/store/getDocuments/(?P<fingerprint>[^/]+)$', getDocumentsView.as_view()),
    url(r'^api/store/putDocuments/(?P<fingerprint>[^/]+)$', putDocumentsView.as_view()),

    url(r'^api/store/getPublications/(?P<fingerprint>[^/]+)$', getPublicationsView.as_view()),

    url(r'^api/store/getComments/(?P<fingerprint>[^/]+)$', getCommentsView.as_view()),

    url(r'^api/store/putComment/(?P<fingerprint>[^/]+)$', putCommentView.as_view()),


    # fast links to dependency latest revision
    url(r'^file/(?P<plugin_hash>[^/]+)/(?P<version>[0-9]+)/(?P<filename>[^/]+)$',
        DeveloperFileView.as_view(), name='developer-file'),

)
