from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile

from accounts.models import NavigationHistory

# Log, log log, log all away. This middleware intercepts all traffic and logs urls used to a table.
# We obviously have to exclude api calls, and javascript loaded pages

DONTLOG_URLS = []

if hasattr(settings, 'DONTLOG_URLS'):
    DONTLOG_URLS += [compile(expr) for expr in settings.DONTLOG_URLS]

class NavigationInterceptor:
    user = None
    def process_request(self, request):
        assert hasattr(request, 'user'), "The Navigation Interceptor middleware\
 requires authentication middleware to be installed. Edit your\
 MIDDLEWARE_CLASSES setting to insert\
 'django.contrib.auth.middlware.AuthenticationMiddleware'. If that doesn't\
 work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes\
 'django.core.context_processors.auth'."
        self.user = request.user
    def process_response(self, request, response):
        if self.user and self.user.is_authenticated() and response.status_code == 200:
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in DONTLOG_URLS):
                new_history = NavigationHistory(user = self.user, path=path)
                new_history.save()

        return response