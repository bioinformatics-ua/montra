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
from django.conf import settings

from accounts.models import EmifProfile, Profile
from developer.models import Plugin, PluginVersion

def debug(context):
  return {'DEBUG': settings.DEBUG}

def baseurl(request):
    """
    Return a BASE_URL template context for the current request.
    """
    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'

    return {'BASE_URL': scheme + request.get_host() + settings.BASE_URL,}

# make user personal profiles available everywhere
def profiles_processor(request):
    profiles = []

    if request.user.is_authenticated():
        try:

            user_profile = EmifProfile.objects.get(user = request.user)

            profiles = user_profile.profiles.all()

        except EmifProfile.DoesNotExist:
            pass

    return { 'profiles': profiles }

# making certain globals like brand and footer available everywhere

def globals(request):
    return settings.GLOBALS

def thirdparty(request):
    return { 'thirdparty': PluginVersion.all_valid(type=Plugin.THIRD_PARTY)}
