from django.conf.urls import patterns, include, url

from django.contrib.auth import views as auth_views

from django.contrib import admin
admin.autodiscover()

from userena import views as userena_views
from accounts.views import SignupFormExtra, signup, signin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'emif.views.home', name='home'),
    # url(r'^emif/', include('emif.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Index page
    url(r'^$', 'emif.views.index'),

    # Questionnaire URLs
    url(r'q/', include('questionnaire.urls')),

    url(r'^take/(?P<questionnaire_id>[0-9]+)/$', 'questionnaire.views.generate_run'),
    # url(r'^$', 'questionnaire.page.views.page', {'page': 'index'}),
    # url(r'^(?P<page>.*)\.html$', 'questionnaire.page.views.page'),
    # url(r'^(?P<lang>..)/(?P<page>.*)\.html$', 'questionnaire.page.views.langpage'),
    # url(r'^setlang/$', 'questionnaire.views.set_language'),

    #
    # User accounts URLs
    #

    # Signup, signin and signout
    url(r'^accounts/signup/$',
        signup,
        {'signup_form': SignupFormExtra,
         'success_url': '/take/1/'},
        name='userena_signup'),
    url(r'^accounts/signin/$',
        signin,
        name='userena_signin'),
    url(r'^accounts/signout/$',
        userena_views.signout,
        name='userena_signout'),

    # Reset password
    # url(r'^accounts/password/reset/$',
    #     auth_views.password_reset,
    #     {'template_name': 'userena/password_reset_form.html',
    #      'email_template_name': 'userena/emails/password_reset_message.txt'},
    #     name='userena_password_reset'),
    # url(r'^accounts/password/reset/done/$',
    #     auth_views.password_reset_done,
    #     {'template_name': 'userena/password_reset_done.html'},
    #     name='userena_password_reset_done'),
    # url(r'^accounts/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
    #     auth_views.password_reset_confirm,
    #     {'template_name': 'userena/password_reset_confirm_form.html'},
    #     name='userena_password_reset_confirm'),
    # url(r'^accounts/password/reset/confirm/complete/$',
    #     auth_views.password_reset_complete,
    #     {'template_name': 'userena/password_reset_complete.html'}),

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
    url(r'^accounts/(?P<username>[^/]+)/edit/$',
        userena_views.profile_edit,
        name='userena_profile_edit'),

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
)
