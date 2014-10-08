# -*- coding: utf-8 -*-
# Copyright (C) 2014 Ricardo F. Gonçalves Ribeiro and Universidade de Aveiro
#
# Authors: Ricardo F. Gonçalves Ribeiro <ribeiro.r@ua.pt>
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

from notifications.models import Notification

from django.contrib.auth.models import User
from django.utils import timezone    
from datetime import timedelta

'''
    Send a notification with a timeframe, if timeframe is None, there's no time frame,
    otherwise its a timeframe specified as a timedelta
'''
def sendNotification(timeframe, destiny, origin, href, message):

        timeout = timezone.now() - timeframe

        existing_notifications = Notification.objects.filter(destiny = destiny, origin = origin, href=href,
            notification=message, created_date__gt=timeout).order_by("-created_date")

        # if theres notifications inside the time frame, just update it
        if len(existing_notifications) >= 1:
            notification = existing_notifications[0]
            notification.created_date = timezone.now()
            notification.removed = False
            notification.read = False
            notification.read_date = None
            notification.save()
        else:
            # if theres no notification inside the time frame create a new one
            new_notification = Notification(destiny = destiny, origin = origin, href=href,
            notification=message)
            new_notification.save()