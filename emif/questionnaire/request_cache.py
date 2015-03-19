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

# Per request cache middleware

# Provides a simple cache dictionary only existing for the request's lifetime

# The middleware provides a threadsafe LocMemCache which can be used just
# like any other django cache facility

from functools import wraps
from threading import currentThread
from django.core.cache.backends.locmem import LocMemCache

_request_cache = {}
_installed_middleware = False

def get_request_cache():
    assert _installed_middleware, 'RequestCacheMiddleware not loaded'
    return _request_cache[currentThread()]

def clear_request_cache():
    _request_cache[currentThread()].clear()

class RequestCache(LocMemCache):
    def __init__(self):
        name = 'locmemcache@%i' % hash(currentThread())
        params = dict()
        super(RequestCache, self).__init__(name, params)

class RequestCacheMiddleware(object):
    def __init__(self):
        global _installed_middleware
        _installed_middleware = True

    def process_request(self, request):
        cache = _request_cache.get(currentThread()) or RequestCache()
        _request_cache[currentThread()] = cache

        cache.clear()

class request_cache(object):
    """ A decorator for use around functions that should be cached for the current
    request. Use like this:

    @request_cache()
    def cached(name):
        print "My name is %s and I'm cached" % name

    @request_cache(keyfn=lambda p: p['id'])
    def cached(param):
        print "My id is %s" % p['id']

    If no keyfn is provided the decorator expects the args to be hashable.

    """

    def __init__(self, keyfn=None):
        self.keyfn = keyfn or (lambda *args: hash(args))

    def __call__(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = get_request_cache()

            cachekey = self.keyfn(*args)
            cacheval = cache.get(cachekey, 'expired')

            if not cacheval == 'expired':
                return cacheval

            result = func(*args, **kwargs)
            cache.set(cachekey, result)

            return result

        return wrapper
