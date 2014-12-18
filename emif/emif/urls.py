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


from django.conf.urls import patterns, include, url

from django.contrib.auth import views as auth_views

from django.contrib import admin
from adminplus.sites import AdminSitePlus

from userena import views as userena_views
from accounts.views import SignupFormExtra, signup, signin
from views import *

from django.conf import settings

from hitcount.views import update_hit_count_ajax



admin.site = AdminSitePlus()
admin.autodiscover()

urlpatterns = patterns('',

    # Comments
    url(r'^comments/', include('django.contrib.comments.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Index page
    url(r'^$', 'emif.views.index', name="home"),
    url(r'^index$', 'emif.views.index', name="home"),

    url(r'^about$', 'emif.views.about'),

    # must do this to be able to use custom paths on this css file
    url(r'^bootstrap_ie_compatibility$', 'emif.views.bootstrap_ie_compatibility'),

    # Advanced Search
    url(r'^advancedSearch/(?P<questionnaire_id>[0-9]+)/(?P<question_set>[0-9]+)/(?P<aqid>[0-9]+)?$', 'advancedsearch.views.advanced_search'),

    # Database Add

    url(r'^add/(?P<questionnaire_id>[0-9]+)/(?P<sortid>[0-9]+)/$', 'fingerprint.views.database_add'),
    url(r'^searchqs/(?P<questionnaire_id>[0-9]+)/(?P<sortid>[0-9]+)/((?P<aqid>[0-9]+)/)?$', 'advancedsearch.views.database_search_qs'),
    url(r'^addqs/(?P<fingerprint_id>[^/]+)/(?P<questionnaire_id>[0-9]+)/(?P<sortid>[0-9]+)/$', 'fingerprint.views.database_add_qs'),

    url(r'^addPost/(?P<questionnaire_id>[0-9]+)/(?P<sortid>[0-9]+)/(?P<saveid>[0-9]+)$', 'fingerprint.views.check_database_add_conditions'),



    # Database Edit
    url(r'^dbEdit/(?P<fingerprint_id>[^/]+)/(?P<questionnaire_id>[0-9]+)$', 'fingerprint.views.database_edit'),
    url(r'^dbEdit/(?P<fingerprint_id>[^/]+)/(?P<questionnaire_id>[0-9]+)/(?P<sort_id>[0-9]+)/$', 'fingerprint.views.database_edit_dl'),
    url(r'^dbDetailed/(?P<fingerprint_id>[^/]+)/(?P<questionnaire_id>[0-9]+)$', 'fingerprint.views.database_detailed_view'),
    url(r'^dbDetailed/(?P<fingerprint_id>[^/]+)/(?P<questionnaire_id>[0-9]+)/(?P<sort_id>[0-9]+)$', 'fingerprint.views.database_detailed_view_dl'),

    url(r'^editqs/(?P<fingerprint_id>[^/]+)/(?P<questionnaire_id>[0-9]+)/(?P<sort_id>[0-9]+)/$', 'fingerprint.views.database_edit_qs'),
    url(r'^detailedqs/(?P<fingerprint_id>[^/]+)/(?P<questionnaire_id>[0-9]+)/(?P<sort_id>[0-9]+)/$', 'fingerprint.views.database_detailed_qs'),

    url(r'^feedback/thankyou/', 'emif.views.feedback_thankyou'),
    url(r'^feedback$', 'emif.views.feedback', name="feedback"),
    url(r'^bugreport$', 'control_version.views.bug_report', name="bug_report"),

    # Results
    url(r'^results$', 'fingerprint.listings.results_fulltext'),

    #Statistics
    url(r'^statistics/(?P<questionnaire_id>[0-9]+)/(?P<question_set>[0-9]+)/$', 'emif.views.statistics'),
    # url(r'^statistics$', 'emif.views.statistics'),

    url(r'^geo$', 'geolocation.views.geo'),


    url(r'^resultsdiff/(?P<page>[-]{0,1}\d+)?$', 'fingerprint.listings.results_diff'),
    url(r'^resultscomp', 'compare.views.results_comp'),
    #url(r'^fingerprint/(?P<runcode>[^/]+)/(?P<qs>[-]{0,1}\d+)/$', 'emif.views.fingerprint'),
    url(r'^fingerprint/(?P<runcode>[^/]+)/(?P<qs>[-]{0,1}\d+)/$', 'population_characteristics.documents.document_form_view'),
    url(r'^fingerprint/(?P<runcode>[^/]+)/(?P<qs>[-]{0,1}\d+)/(?P<activetab>[^/]+)/$', 'population_characteristics.documents.document_form_view'),
    # Single qs for load by blocks
    url(r'^fingerprintqs/(?P<runcode>[^/]+)/(?P<qsid>[0-9]+)/$', 'population_characteristics.documents.single_qset_view'),

    # List Databases
    url(r'^query/(?P<page>[-]{0,1}\d+)?$', 'fingerprint.listings.query_solr'),
    url(r'^databases/(?P<page>[-]{0,1}\d+)?$', 'fingerprint.listings.databases', name="databases"),
#    url(r'^alldatabases/(?P<page>[-]{0,1}\d+)?$', 'emif.views.all_databases'),
    url(r'^alldatabases/(?P<page>[-]{0,1}\d+)?$', 'fingerprint.listings.all_databases_user'),
    url(r'^alldatabases/data-table$', 'datatable.views.all_databases_data_table'),
    url(r'^qs_data_table$', 'datatable.views.qs_data_table'),
    url(r'^export_datatable$', 'datatable.views.export_datatable'),
    url(r'^export_all_answers$', 'emif.views.export_all_answers'),
    url(r'^export_my_answers$', 'emif.views.export_my_answers'),
    url(r'^export_search_answers$', 'emif.views.export_search_answers'),
    url(r'^export_bd_answers/(?P<runcode>[^/]+)/$', 'fingerprint.views.export_bd_answers'),
    url(r'^delete-questionnaire/(?P<qId>[0-9]+)/$', 'utils.delete_questionnaire.delete'),
    # Documentation
    url(r'^docs/api$', 'fingerprint.listings.docs_api'),
    #more like this
    url(r'^mlt/(?P<doc_id>[^/]+)/(?P<page>[-]{0,1}\d+)?$', 'fingerprint.listings.more_like_that'),


    url(r'^rm/(?P<id>[^/]+)', 'fingerprint.views.delete_fingerprint'),

    url(r'^share/activation/(?P<activation_code>[^/]+)', 'emif.views.sharedb_activation'),
    url(r'^share/(?P<db_id>[^/]+)', 'emif.views.sharedb'),

    url(r'^invite/(?P<db_id>[^/]+)', 'emif.views.invitedb'),

    # API
    url(r'^api/', include('api.urls')),

    # Control version
    url(r'^controlversion/', include('control_version.urls')),

    # Questionnaire URLs
    #url(r'q/', include('questionnaire.urls')),
    #
    # User accounts URLs
    #
    url(r'^accounts/', include('accounts.urls')),

    # url(r'^api-upload-info/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^api-info/(?P<page>[-]{0,1}\d+)?', 'fingerprint.listings.create_auth_token', name="api-info"),

    # Population Characteristics URLs
    url(r'population/', include('population_characteristics.urls')),

    # Docs Manager
    url(r'docsmanager/', include('docs_manager.urls')),

    # Literature URLs
    url(r'literature/', include('literature.urls')),

    # AdvancedSearch URLs
    url(r'advsearch/', include('advancedsearch.urls')),

    # Private links URLs
    url(r'public/', include('public.urls')),

    # newsletter system
    url(r'^newsletter/', include('newsletter.urls')),

    # Notifications URLs
    url(r'notifications/', include('notifications.urls')),

    # Faq
    url('^faq/', include('fack.urls')),

    # unique views plugin
    url(r'^api/hit_counter/$', update_hit_count_ajax, name='hitcount_update_ajax'),

    # Fingerprint
    url('^fingerprint/', include('fingerprint.urls')),

    # DashBoard
    url(r'^dashboard', include('dashboard.urls')),


    # Statistics
    url(r'^statistics', include('statistics.urls')),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^500/$', 'django.views.generic.simple.direct_to_template', {'template': '500.html'}),
        (r'^404/$', 'django.views.generic.simple.direct_to_template', {'template': '404.html'}),
        (r'^403/$', 'django.views.generic.simple.direct_to_template', {'template': '403.html'}),
    )
