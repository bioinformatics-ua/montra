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
# Django settings for emif project.
import os.path

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from os import path
from saml2 import saml
import saml2


BASEDIR = path.dirname(path.abspath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_NAME = "EMIF Catalogue"

GLOBALS = {
    'BRAND': "EMIF Catalogue",
    # url based upon STATIC_URL
    'BRAND_LOGO': "img/emif_logo_trans.png",
    'COPYRIGHT': "© EMIF Catalogue",
    'FOOTER_EXTRA': """
                    <!-- EXTRA HTML FOOTER CODE HERE -->
                    <small id="supportability">This website is optimised to Safari, Chrome, Firefox, Opera and IE9+.
                    <!--It runs in IE7-IE8, but it has low performance and no enhanced features.--></small>
                   """
}
# Header and Footer Settings


#BASE_URL = '/emif-dev/'
# Note: When changing this to something not /, all is automatically changed on the links (except for links inside css files)
# for this files we must change it manually (or serve them as dinamic files), this problem only ocurrs on IE
# so if changing to something that not /, we should also change on file /static/css/bootstrap_ie_compatibility.css all relative # paths. This is necessary because i cant use django template variables inside a considered static file.
BASE_URL = '/'
VERSION = '1.0'
VERSION_DATE = '2015.Mar.22 - 21:03UTC'
PROJECT_DIR_ROOT = '/projects/emif-dev/'

XMLSEC_BIN = '/usr/bin/xmlsec1'
IDP_SERVICES = [
    path.join(BASEDIR, 'remote_metadata.xml'),
    path.join(BASEDIR, 'testshib.xml')
]

if DEBUG:
    PROJECT_DIR_ROOT = "./"
    MIDDLE_DIR = ""
    IDP_URL = "http://localhost:8000/"
else:
    MIDDLE_DIR = "/emif/"
    IDP_URL = BASE_URL

ADMINS = (
    ('Luis A. Bastiao Silva', 'bastiao@ua.pt'),
#    ('José Luis Oliveira', 'jlo@ua.pt'),
#    ('Tiago Godinho', 'tmgodinho@ua.pt'),
    ('Ricardo Ribeiro', 'ribeiro.r@ua.pt'),
)

SOLR_HOST = "localhost"
SOLR_PORT = "8983"
SOLR_PATH = "/solr"

BROKER_CELERY='amqp://guest@localhost//'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "emif.context_processors.debug",
    "emif.context_processors.baseurl",
    "emif.context_processors.profiles_processor",
    'constance.context_processors.config',
    "emif.context_processors.globals"
)

MANAGERS = ADMINS

DATABASE_PATH_SQLITE3 = "emif.db"

if not DEBUG:
    DATABASE_PATH_SQLITE3 = PROJECT_DIR_ROOT + "emif/" + DATABASE_PATH_SQLITE3

'''DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
    'NAME': DATABASE_PATH_SQLITE3,                      # Or path to database file if using sqlite3.
    'USER': '',                      # Not used with sqlite3.
    'PASSWORD': '',                  # Not used with sqlite3.
    'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
    'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
'''
DATABASES = {
    'default': {
        #        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'emif_testing', # Or path to database file if using sqlite3.
        'USER': 'postgres', # Not used with sqlite3.
        'PASSWORD': '12345', # Not used with sqlite3.
        'HOST': 'localhost', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
        'AUTOCOMMIT': True,
        'autocommit': True,
        'OPTIONS': {
            'autocommit': True,
        },
    },
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Lisbon'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"

if DEBUG:
    STATIC_ROOT = ''
else:
    STATIC_ROOT = PROJECT_DIR_ROOT + 'emif/emif/collected-static'



# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = BASE_URL+'static/'


# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'emif/static'),
    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'questionnaire/static/'),
    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'fingerprint/static/'),
    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'population_characteristics/static'),
    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'literature/static'),
    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'docs_manager/static'),
    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'advancedsearch/static'),
    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'public/static'),
    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'accounts/static'),
    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'dashboard/static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    #'djangobower.finders.BowerFinder',
    'compressor.finders.CompressorFinder',
)
COMPRESS_JS_FILTERS = (
    'compressor.filters.jsmin.JSMinFilter',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'j*zdirg7yy9@q1k=c*q!*kovfsd#$FDFfsdfkae#id04pyta=yz@w34m6rvwfe'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'questionnaire.request_cache.RequestCacheMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'emif.middleware.LoginRequiredMiddleware',
    'emif.middleware.ProfileRequiredMiddleware',
    'emif.interceptor.NavigationInterceptor',
    'johnny.middleware.LocalStoreClearMiddleware',
    'johnny.middleware.QueryCacheMiddleware',
)

ROOT_URLCONF = 'emif.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'emif.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'apps/seantis-questionnaire/questionnaire/templates'),
    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'emif/templates'),
    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'population_characteristics/templates'),
    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'literature/templates'),
    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'control_version/templates'),
    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'docs_manager/templates'),
    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'advancedsearch/templates'),
    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'public/templates'),
    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'dashboard/templates'),

    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'notifications/templates'),
    os.path.abspath(PROJECT_DIR_ROOT + MIDDLE_DIR + 'accounts/templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.markup',
    'django.contrib.comments',

    # Admin area
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.admindocs',



    # Questionnaires
    'transmeta',
    'questionnaire',
    #'questionnaire.page',

    # User signup/signin/management
    'userena',
    'guardian',
    'easy_thumbnails',
    'accounts',

    # DB migrations
    'south',

    # Django Rest Framework
    'rest_framework',
    'rest_framework.authtoken',

    # Bootstrap layouts and forms
    'crispy_forms',
    'emif',

    'searchengine',
    'api',
    'fingerprint',
    'control_version',
    'docs_manager',
    'population_characteristics',
    'literature',
    'django_bootstrap_breadcrumbs',
    'bootstrap_pagination',
    'django_jenkins',


    'djcelery',
    #'djangobower',
    'advancedsearch',

    # public links
    'public',

    # newsletters
    'django_extensions',
    'sorl.thumbnail',
    'newsletter',

    # FAQ
    'fack',

    # Utility to hook custom view admin pages easily
    'adminplus',

    # unique views counter
    'hitcount',

    # dashboard
    'dashboard',

    # notifications
    'notifications',
    # Django-Compressor
    "compressor",

    "raven.contrib.django.raven_compat",

    # django-constance
    'constance.backends.database',
    "constance",

    "djangosaml2"
)

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
    'Request_Answer': (True, 'Controls whether we activate/deactivate the request answer functionality.'),
    'population_characteristics': (True, 'Controls whether we activate/deactivate the Population Characteristics functionality.'),
    'documents': (True, 'Controls whether we activate/deactivate the Documents functionality.'),
    'literature': (True, 'Controls whether we activate/deactivate the Literature functionality.'),
    'extra_information': (True, 'Controls whether we activate/deactivate the Extra Information functionality.'),
    'discussion': (True, 'Controls whether we activate/deactivate the discussion functionality.'),
    'newsletter': (True, 'Controls whether we activate/deactivate the newsletter functionality.'),
    'private_links': (True, 'Controls whether we activate/deactivate the private links functionality.'),
    'more_like_this': (True, 'Controls whether we activate/deactivate the more like this functionality.'),
    'geolocation': (True, 'Controls whether we activate/deactivate the geolocation functionality.'),
    'datatable': (True, 'Controls whether we activate/deactivate the datatable functionality.'),
}

# Userena settings

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    'djangosaml2.backends.Saml2Backend',
)

LOGIN_URL = '/saml2/login/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Email backend settings
# EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025

ANONYMOUS_USER_ID = -1

AUTH_PROFILE_MODULE = 'accounts.EmifProfile'


SAML_CONFIG = {
    # full path to the xmlsec1 binary programm
    'xmlsec_binary': XMLSEC_BIN,

    # your entity id, usually your subdomain plus the url to the metadata view
    'entityid': IDP_URL+'saml2/metadata',

    # directory with attribute mapping
    'attribute_map_dir': path.join(BASEDIR, 'attributemaps'),

    # this block states what services we provide
    'service': {
         # we are just a lonely SP
        'sp' : {
            'name': 'Emif Catalogue SP',
            'name_id_format': saml.NAMEID_FORMAT_TRANSIENT,
            'endpoints': {
                # url and binding to the assetion consumer service view
                # do not change the binding or service name
                'assertion_consumer_service': [
                    (IDP_URL+'saml2/acs/',
                        saml2.BINDING_HTTP_POST),
                    ],
                    # url and binding to the single logout service view
                    # do not change the binding or service name
                    'single_logout_service': [
                        (IDP_URL+'saml2/ls/',
                            saml2.BINDING_HTTP_REDIRECT),
                        (IDP_URL+'saml2/ls/post',
                            saml2.BINDING_HTTP_POST)
                        ],


                },

           # attributes that this project need to identify a user
          'required_attributes': ['uid'],

           # attributes that may be useful to have but not required
          'optional_attributes': ['eduPersonAffiliation'],
          },
      },

  # where the remote metadata is stored
  'metadata': {
      'local': IDP_SERVICES,
      },

  # set to 1 to output debugging information
  'debug': 1,

  # certificate
  'key_file': path.join(BASEDIR, 'sp.key'),  # private part
  'cert_file': path.join(BASEDIR, 'sp.crt'),  # public part

  # own metadata settings
  'contact_person': [
      {'given_name': 'José Luis',
       'sur_name': 'Oliveira',
       'company': 'DETI/IEETA',
       'email_address': 'jlo@ua.pt',
       'contact_type': 'administrative'},
      ],
  # you can set multilanguage information here
  'organization': {
      'name': [('EMIF Catalogue', 'en')],
      'display_name': [('EMIF Catalogue', 'en')],
      'url': [('http://bioinformatics.ua.pt/emif', 'en')],
      },
  'valid_for': 24,  # how long is our metadata valid
}

SAML_DJANGO_USER_MAIN_ATTRIBUTE = 'email'
SAML_USE_NAME_ID_AS_USERNAME = False
SAML_CREATE_UNKNOWN_USER = True
SAML_ATTRIBUTE_MAPPING = {
    'mail': ('email', 'username' ),
    'eduPersonPrincipalName': ('email', 'username'),
    'givenName': ('first_name', ),
    'sn': ('last_name', ),
}

#Userena settings
USERENA_ACTIVATION_REQUIRED = True
USERENA_SIGNIN_AFTER_SIGNUP = False
USERENA_WITHOUT_USERNAMES = True
USERENA_DISABLE_PROFILE_LIST = True
USERENA_USE_MESSAGES = False
USERENA_REDIRECT_ON_SIGNOUT = BASE_URL
USERENA_SIGNIN_REDIRECT_BASE = BASE_URL
USERENA_SIGNIN_REDIRECT_URL = BASE_URL + 'dashboard'
USERENA_MODERATE_REGISTRATION = True                    #True - need admin approval (activation)
USERENA_ACTIVATION_REJECTED = 'ACTIVATION_REJECTED'
USERENA_PENDING_MODERATION = 'PENDING_MODERATION'
USERENA_ACTIVATED = 'ALREADY_ACTIVATED'
USERENA_REMEMBER_ME_DAYS = ('a day', 1)
USERENA_HTML_EMAIL = True
USERENA_USE_PLAIN_TEMPLATE = False

LOGIN_REDIRECT_URL = USERENA_SIGNIN_REDIRECT_URL
LOGIN_URL = BASE_URL + ''
LOGOUT_URL = BASE_URL + 'accounts/signout/'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'DEBUG',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'saml2.response': {
            'handlers': ['console'],
            'level': os.getenv('DEBUG'),
        },
        'djangosaml2': {
            'handlers': ['console'],
            'level': os.getenv('DEBUG'),
        },
        "saml2.mdstore": {
            'handlers': ['console'],
            'level': os.getenv('DEBUG'),
        },
    }
}

# Questionaire languages
LANGUAGES = (
    ('en', 'English'),
)

# Defines the progressbar behavior in the questionnaire
# the possible options are 'default', 'async' and 'none'
#
#   'default'
#   The progressbar will be rendered in each questionset together with the
#   questions. This is a good choice for smaller questionnaires as the
#   progressbar will always be up to date.
#
#   'async'
#   The progressbar value is updated using ajax once the questions have been
#   rendered. This approach is the right choice for bigger questionnaires which
#   result in a long time spent on updating the progressbar with each request.
#   (The progress calculation is by far the most time consuming method in
#    bigger questionnaires as all questionsets and questions need to be
#    parsed to decide if they play a role in the current run or not)
#
#   'none'
#   Completely omits the progressbar. Good if you don't want one or if the
#   questionnaire is so huge that even the ajax request takes too long.
QUESTIONNAIRE_PROGRESS = 'async'

#DEBUG_TOOLBAR
if not DEBUG:
    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INSTALLED_APPS += (
    'debug_toolbar',
    )

    DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.profiling.ProfilingDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.cache.CacheDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    )

    DEBUG_TOOLBAR_CONFIG = {
    # 'INTERCEPT_REDIRECTS': False,
    }


JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
)

#JENKINS_TEST_RUNNER='django_jenkins.nose_runner.CINoseTestSuiteRunner'

#Pages that do not require login
LOGIN_EXEMPT_URLS = (
    r'^$',
    r'^indexbeta$',
    r'^saml2$',
    r'^saml2/login',
    r'^saml2/metadata',
    r'^saml2/acs',
    r'^saml2/ls',
    r'^about',
    r'^feedback',
    r'^faq',
    r'^accounts/signup',
    r'^accounts/signin',
    r'^accounts/activate/(?P<activation_key>\w+)/$',
    r'^accounts/signup/complete',
    r'^accounts/password/reset/',
    r'^accounts/(?P<username>[^/]+)/disabled/',
    r'^api/metadata',
    r'^api/search',
    r'^api-token-auth-create/',
    r'^import-questionnaire',
    r'^delete-questionnaire',
    r'^bootstrap_ie_compatibility',
    # public shares
    r'^public/fingerprint/(?P<fingerprint_id>[^/]+)',
    r'^literature/(?P<fingerprint_id>[^/]+)/(?P<page>[0-9]+)$',
    r'^literature/(?P<fingerprint_id>[^/]+)$',
    r'^fingerprintqs/(?P<runcode>[^/]+)/(?P<qsid>[0-9]+)/$',
    r'^population/jerboafiles/(?P<fingerprint_id>[^/]+)/$',
    r'^population/jerboalistvalues/(?P<var>[^/]+)/(?P<row>[^/]+)/(?P<fingerprint_id>[^/]+)/(?P<revision>[^/]+)$',
    r'^population/filters/(?P<var>[^/]+)/(?P<fingerprint_id>[^/]+)$',
    r'^population/genericfilter/(?P<param>[^/]+)$',
    r'^population/settings/(?P<runcode>[^/]+)/$',

    r'^docsmanager/docfiles/(?P<fingerprint>[^/]+)/$',
    r'^api/getfile',

)

#Pages that wont be logged into user history
DONTLOG_URLS = (
    r'^fingerprintqs/(?P<runcode>[^/]+)/(?P<qsid>[0-9]+)/$',
    r'^api/(?P<anything>[^/]*)',
    r'^docsmanager/uploadfile/(?P<fingerprint_id>[^/]+)/$',
    r'^docsmanager/docfiles/(?P<fingerprint_id>[^/]+)/$',
    r'^population/settings/(?P<fingerprint_id>[^/]+)/$',
    r'^population/jerboafiles/(?P<fingerprint_id>[^/]+)/$',
    r'^jerboalistvalues/(?P<var>[^/]+)/(?P<row>[^/]+)/(?P<fingerprint_id>[^/]+)/(?P<revision>[^/]+)$'
    r'^searchqs/(?P<questionnaire_id>[0-9]+)/(?P<sortid>[0-9]+)/(?P<aqid>[0-9]+)?$',
    r'^addqs/(?P<fingerprint_id>[^/]+)/(?P<questionnaire_id>[0-9]+)/(?P<sortid>[0-9]+)/$',
    r'^addPost/(?P<questionnaire_id>[0-9]+)/(?P<sortid>[0-9]+)/(?P<saveid>[0-9]+)$',
    r'^dbEdit/(?P<fingerprint_id>[^/]+)/(?P<questionnaire_id>[0-9]+)$',
    r'^dbEdit/(?P<fingerprint_id>[^/]+)/(?P<questionnaire_id>[0-9]+)/(?P<sort_id>[0-9]+)/$',
    r'^dbDetailed/(?P<fingerprint_id>[^/]+)/(?P<questionnaire_id>[0-9]+)$',
    r'^dbDetailed/(?P<fingerprint_id>[^/]+)/(?P<questionnaire_id>[0-9]+)/(?P<sort_id>[0-9]+)$',
    r'^editqs/(?P<fingerprint_id>[^/]+)/(?P<questionnaire_id>[0-9]+)/(?P<sort_id>[0-9]+)/$',
    r'^detailedqs/(?P<fingerprint_id>[^/]+)/(?P<questionnaire_id>[0-9]+)/(?P<sort_id>[0-9]+)/$',
    r'^qs_data_table$',
    r'^admin/jsi18n/',
)

#Set session idle timeout (seconds)
SESSION_IDLE_TIMEOUT = 7200
SESSION_SAVE_EVERY_REQUEST = True



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    )

}

#MONGODB
#=======
#Settings of EMIF MongoDB server, this is used to store the analytic data of population characteristics
MONGO_EMIF = {
    'DB_NAME': 'emif_mongo',
    'HOST': 'localhost',
    'PORT': 27017,
    'COLLECTION': 'jerboa_files'
}

#CONNECT MONGODB
#===============

# Connect on MongoDB Database
# from pymongo.connection import Connection
from pymongo.errors import ConnectionFailure
import sys
# try:
#     connection = Connection(MONGO_EMIF['HOST'], MONGO_EMIF['PORT'])
#     DBCON = connection[MONGO_EMIF['DB_NAME']]
# except ConnectionFailure, e:
#     sys.stderr.write("Could not connect to MongoDB: %s" % e)
#     sys.exit(1)


from pymongo import MongoClient
try:
    client = MongoClient(MONGO_EMIF['HOST'], MONGO_EMIF['PORT'])
    # db_name_mongo = MONGO_EMIF['DB_NAME']
    # db_mongo = client.db_name_mongo
    db_mongo = client.emif_mongo
    # jerboa_collection = db_mongo.MONGO_EMIF['COLLECTION']
    jerboa_collection = db_mongo.jerboa_files
    jerboa_aggregation_collection = db_mongo.jerboa_aggregation
except ConnectionFailure, e:
    sys.stderr.write("Could not connect to MongoDB: %s" % e)
    sys.exit(1)

# REDIRECT USER ACCORDING TO PROFILE
REDIRECT_DATACUSTODIAN = 'dashboard.views.dashboard'
REDIRECT_RESEARCHER = 'dashboard.views.dashboard'


# MEMCACHED
CACHES = {
    'default' : dict(
        BACKEND = 'johnny.backends.memcached.MemcachedCache',
        LOCATION = ['127.0.0.1:11211'],
        JOHNNY_CACHE = True,
    )
}

JOHNNY_MIDDLEWARE_KEY_PREFIX='emif_'

PUBLIC_LINK_MAX_VIEWS = 50; # number of views
PUBLIC_LINK_MAX_TIME = 24*30; # hours


# Unique views definitions
HITCOUNT_KEEP_HIT_ACTIVE = { 'days': 1 }

# Django-Compressor activation
COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False


# Periodic user updates newsletter settings
NEWSLETTER_DAY='friday'
NEWSLETTER_HOUR = 3
NEWSLETTER_MIN = 0

try:
    from local_settings import *
except:
    pass

