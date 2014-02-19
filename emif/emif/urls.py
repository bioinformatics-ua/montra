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
from django.views.generic.simple import direct_to_template

admin.autodiscover()

from userena import views as userena_views
from accounts.views import SignupFormExtra, EditProfileFormExtra, profile_edit, signup, signin
from views import *

from django.conf import settings

urlpatterns = patterns('',


    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Index page
    url(r'^$', 'emif.views.index', name="home"),
    
    url(r'^about$', 'emif.views.about'),

    # must do this to be able to use custom paths on this css file
    url(r'^bootstrap_ie_compatibility$', 'emif.views.bootstrap_ie_compatibility'),
    
    # Quick Search
    url(r'^search$', 'emif.views.quick_search'),

    # Advanced Search
    url(r'^advancedSearch/(?P<questionnaire_id>[0-9]+)/(?P<question_set>[0-9]+)/$', 'emif.views.advanced_search'),
    
    # Database Add

    url(r'^add/(?P<questionnaire_id>[0-9]+)/(?P<sortid>[0-9]+)/$', 'emif.views.database_add'),
    url(r'^searchqs/(?P<questionnaire_id>[0-9]+)/(?P<sortid>[0-9]+)/$', 'emif.views.database_search_qs'),
    url(r'^addPost/(?P<questionnaire_id>[0-9]+)/(?P<sortid>[0-9]+)$', 'emif.views.check_database_add_conditions'),
    

    
    # Database Edit
    url(r'^dbEdit/(?P<fingerprint_id>[^/]+)/(?P<questionnaire_id>[0-9]+)$$', 'emif.views.database_edit'),
    #url(r'^dbEdit/(?P<questionnaire_id>[0-9]+)/$$', 'emif.views.database_edit'),
    url(r'^q3/(?P<runcode>[^/]+)/$', questionaries_with_sets, name='questionaries_with_sets'),
    url(r'^q3/(?P<runcode>[^/]+)/(?P<qs>[-]{0,1}\d+)/$',
            questionaries_with_sets, name='questionset_sets'),


    url(r'^feedback/thankyou/', 'emif.views.feedback_thankyou'),
    url(r'^feedback$', 'emif.views.feedback', name="feedback"),
    url(r'^bugreport$', 'control_version.views.bug_report', name="bug_report"),


    (r'^contact/thankyou/', 'searchengine.views.thankyou'),
    (r'^contact$', 'searchengine.views.contactview'),
    # Results
    #url(r'^results/(?P<query>[a-zA-Z0-9]+)/$', 'emif.views.results'),
    url(r'^results$', 'emif.views.results_fulltext'),

    #Statistics
    url(r'^statistics/(?P<questionnaire_id>[0-9]+)/(?P<question_set>[0-9]+)/$', 'emif.views.statistics'),
    # url(r'^statistics$', 'emif.views.statistics'),

    url(r'^geo$', 'emif.views.geo'),


    url(r'^resultsdiff/(?P<page>[-]{0,1}\d+)?$', 'emif.views.results_diff'),
    url(r'^resultscomp', 'emif.views.results_comp'),
    #url(r'^fingerprint/(?P<runcode>[^/]+)/(?P<qs>[-]{0,1}\d+)/$', 'emif.views.fingerprint'),
    url(r'^fingerprint/(?P<runcode>[^/]+)/(?P<qs>[-]{0,1}\d+)/$', 'population_characteristics.documents.document_form_view'),
    
    # List Databases
    url(r'^databases/(?P<page>[-]{0,1}\d+)?$', 'emif.views.databases', name="databases"),
    url(r'^alldatabases/(?P<page>[-]{0,1}\d+)?$', 'emif.views.all_databases'),
    url(r'^alldatabases/data-table$', 'emif.views.all_databases_data_table'),
    url(r'^qs_data_table$', 'emif.views.qs_data_table'),    
    url(r'^export_all_answers$', 'emif.views.export_all_answers'),
    url(r'^export_my_answers$', 'emif.views.export_my_answers'),
    url(r'^export_bd_answers/(?P<runcode>[^/]+)/$', 'emif.views.export_bd_answers'),
    url(r'^import-questionnaire', 'emif.views.import_questionnaire'),
    url(r'^delete-questionnaire/(?P<qId>[0-9]+)/$', 'utils.delete_questionnaire.delete'),
    # Documentation
    url(r'^docs/api$', 'emif.views.docs_api'),


    url(r'^rm/(?P<id>[^/]+)', 'emif.views.delete_fingerprint'),
    url(r'^force-rm/(?P<id>[^/]+)', 'emif.views.force_delete_fingerprint'),
    
    url(r'^share/activation/(?P<activation_code>[^/]+)', 'emif.views.sharedb_activation'),
    url(r'^share/(?P<db_id>[^/]+)', 'emif.views.sharedb'),

    # API
    url(r'^api/', include('api.urls')),

    # Control version
    url(r'^controlversion/', include('control_version.urls')),

    # Questionnaire URLs
    url(r'q/', include('questionnaire.urls')),

    url(r'^take/(?P<questionnaire_id>[0-9]+)/$', 'questionnaire.views.generate_run'),
    

    #
    # User accounts URLs
    #

    # Signup, signin and signout
    url(r'^accounts/signup/$',
        signup,
        {'signup_form': SignupFormExtra,
         'success_url': settings.BASE_URL + 'databases'},
        name='userena_signup'),

    url(r'^accounts/signup/complete/$',
        direct_to_template,
        {'template': 'userena/signup_complete.html',
         'extra_context': {'userena_activation_required': settings.USERENA_ACTIVATION_REQUIRED,
                           'userena_moderated_registration': settings.USERENA_MODERATE_REGISTRATION}},
        name='userena_signup_complete'),

    url(r'^accounts/signup/activate/complete/$',
        direct_to_template,
        {'template': 'userena/activation_complete.html'},
        name='userena_activated'),

    url(r'^accounts/signin/$',
        signin,
        name='userena_signin'),
    url(r'^accounts/signout/$',
        userena_views.signout,
        name='userena_signout'),

    # Edit Profile
    url(r'^accounts/profile_edit/$', 'accounts.views.profile_edit'),

    # Reset password
    url(r'^accounts/password/reset/$',
        auth_views.password_reset,
        {'template_name': 'userena/password_reset_form.html',
         'email_template_name': 'userena/emails/password_reset_message.txt'},
        name='userena_password_reset'),
    url(r'^accounts/password/reset/done/$',
        auth_views.password_reset_done,
        {'template_name': 'userena/password_reset_done.html'},
        name='userena_password_reset_done'),
    url(r'^accounts/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'template_name': 'userena/password_reset_confirm_form.html'},
        name='userena_password_reset_confirm'),
    url(r'^accounts/password/reset/confirm/complete/$',
        auth_views.password_reset_complete,
        {'template_name': 'userena/password_reset_complete.html'}),

    # Activate
    url(r'^accounts/activate/(?P<activation_key>\w+)/$',
       userena_views.activate,
       name='userena_activate'),


    # Change email and confirm it
    url(r'^accounts/(?P<username>[^/]+)/email/$',
        userena_views.email_change,
        name='userena_email_change'),
    url(r'^accounts/(?P<username>[^/]+)/email/complete/$',
        userena_views.direct_to_user_template,
        {'template_name': 'userena/email_change_complete.html'},
        name='userena_email_change_complete'),
    url(r'^accounts/(?P<username>[^/]+)/confirm-email/complete/$',
        userena_views.direct_to_user_template,
        {'template_name': 'userena/email_confirm_complete.html'},
        name='userena_email_confirm_complete'),
    url(r'^accounts/confirm-email/(?P<confirmation_key>\w+)/$',
        userena_views.email_confirm,
        name='userena_email_confirm'),

    # Disabled account
    url(r'^accounts/(?P<username>[^/]+)/disabled/$',
        userena_views.direct_to_user_template,
        {'template_name': 'userena/disabled.html'},
        name='userena_disabled'),

    # Change password
    url(r'^accounts/(?P<username>[^/]+)/password/$',
        userena_views.password_change,
        name='userena_password_change'),
    url(r'^accounts/(?P<username>[^/]+)/password/complete/$',
        userena_views.direct_to_user_template,
        {'template_name': 'userena/password_complete.html'},
        name='userena_password_change_complete'),

    # Edit profile
    # url(r'^accounts/(?P<username>[^/]+)/edit/$',
    #     userena_views.profile_edit,
    #     {'edit_profile_form': EditProfileForm},
    #     name='userena_profile_edit'),

    # View profiles
    url(r'^accounts/(?P<username>(?!signout|signup|signin)[^/]+)/$',
        userena_views.profile_detail,
        name='userena_profile_detail'),
    url(r'^accounts/page/(?P<page>[0-9]+)/$',
        userena_views.ProfileListView.as_view(),
        name='userena_profile_list_paginated'),
    url(r'^accounts/$',
        userena_views.ProfileListView.as_view(),
        name='userena_profile_list'),

    # url(r'^api-upload-info/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^api-info/(?P<page>[-]{0,1}\d+)?', 'emif.views.create_auth_token', name="api-info"),
    url(r'^docs/api', 'emif.views.docs_api'),

    # Population Characteristics URLs
    url(r'population/', include('population_characteristics.urls')),
)
