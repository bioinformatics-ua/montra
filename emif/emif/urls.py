from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'emif.views.home', name='home'),
    # url(r'^emif/', include('emif.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # questionnaire urls
    url(r'q/', include('questionnaire.urls')),

    url(r'^take/(?P<questionnaire_id>[0-9]+)/$', 'questionnaire.views.generate_run'),
    url(r'^$', 'questionnaire.page.views.page', {'page': 'index'}),
    url(r'^(?P<page>.*)\.html$', 'questionnaire.page.views.page'),
    url(r'^(?P<lang>..)/(?P<page>.*)\.html$', 'questionnaire.page.views.langpage'),
    url(r'^setlang/$', 'questionnaire.views.set_language'),
)
