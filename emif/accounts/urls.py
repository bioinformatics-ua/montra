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
#
from django.conf.urls.defaults import *
from views import *
from django.views.generic.simple import direct_to_template
from userena import views as userena_views
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^signup/$',
        signup,
        {'signup_form': SignupFormExtra,
         'success_url': settings.BASE_URL + 'dashboard'},
        name='userena_signup'),

    url(r'^signup/complete/$',
        direct_to_template,
        {'template': 'userena/signup_complete.html',
         'extra_context': {'userena_activation_required': settings.USERENA_ACTIVATION_REQUIRED,
                           'userena_moderated_registration': settings.USERENA_MODERATE_REGISTRATION}},
        name='userena_signup_complete'),

    url(r'^signup/activate/complete/$',
        direct_to_template,
        {'template': 'userena/activation_complete.html'},
        name='userena_activated'),

    url(r'^signin/$',
        signin,
        name='userena_signin'),

    url(r'^signout/$',
        userena_views.signout,
        name='userena_signout'),

    # Edit Profile
    url(r'^profile_edit/$', 'accounts.views.profile_edit'),

    # Reset password
    url(r'^password/reset/$',
        auth_views.password_reset,
        {'template_name': 'userena/password_reset_form.html',
         'email_template_name': 'userena/emails/password_reset_message.txt'},
        name='userena_password_reset'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        {'template_name': 'userena/password_reset_done.html'},
        name='userena_password_reset_done'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'template_name': 'userena/password_reset_confirm_form.html'},
        name='userena_password_reset_confirm'),
    url(r'^password/reset/confirm/complete/$',
        auth_views.password_reset_complete,
        {'template_name': 'userena/password_reset_complete.html'}),

    # Activate
    url(r'^activate/(?P<activation_key>\w+)/$',
       userena_views.activate,
       name='userena_activate'),

    # reject user
    url(r'^reject/(?P<activation_key>\w+)/$',
       userena_views.reject,
       name='userena_reject'),

    # Change email and confirm it
    url(r'^(?P<username>[^/]+)/email/$',
        userena_views.email_change,
        name='userena_email_change'),
    url(r'^(?P<username>[^/]+)/email/complete/$',
        userena_views.direct_to_user_template,
        {'template_name': 'userena/email_change_complete.html'},
        name='userena_email_change_complete'),
    url(r'^(?P<username>[^/]+)/confirm-email/complete/$',
        userena_views.direct_to_user_template,
        {'template_name': 'userena/email_confirm_complete.html'},
        name='userena_email_confirm_complete'),
    url(r'^confirm-email/(?P<confirmation_key>\w+)/$',
        userena_views.email_confirm,
        name='userena_email_confirm'),

    # Disabled account
    url(r'^(?P<username>[^/]+)/disabled/$',
        userena_views.direct_to_user_template,
        {'template_name': 'userena/disabled.html'},
        name='userena_disabled'),

    # Change password
    url(r'^(?P<username>[^/]+)/password/$',
        userena_views.password_change,
        name='userena_password_change'),
    url(r'^(?P<username>[^/]+)/password/complete/$',
        userena_views.direct_to_user_template,
        {'template_name': 'userena/password_complete.html'},
        name='userena_password_change_complete'),

    # View profiles
    url(r'^(?P<username>(?!signout|signup|signin)[^/]+)/$',
        userena_views.profile_detail,
        name='userena_profile_detail'),
    url(r'^page/(?P<page>[0-9]+)/$',
        userena_views.ProfileListView.as_view(),
        name='userena_profile_list_paginated'),
    url(r'^$',
        userena_views.ProfileListView.as_view(),
        name='userena_profile_list'),
)
