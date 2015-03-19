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

from notifications.models import Notification

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from emif.utils import send_custom_mail
from django.conf import settings

'''
    Send a notification with a timeframe, if timeframe is None, there's no time frame,
    otherwise its a timeframe specified as a timedelta
'''
def sendNotification(timeframe, destiny, origin, href, message, custom_mail_message=None):

        notification = None

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
            notification = Notification(destiny = destiny, origin = origin, href=href,
            notification=message)
            notification.save()

        if notification != None and notification.destiny.emif_profile.mail_not == True:
            subject = None
            message = None
            if custom_mail_message != None:
                (subject, message) = custom_mail_message
            else:
                subject = "EMIF Catalogue: Notification"
                message = """Dear %s,\n\n
                    \n\n
                    %s\n\n
                    You can see it <a href="%s%s">here</a>.
                    \n\nSincerely,\nEMIF Catalogue
                """ % (notification.destiny.get_full_name(), notification.notification, settings.BASE_URL
                    ,notification.href)

            send_custom_mail(subject,
                message, settings.DEFAULT_FROM_EMAIL,
                [notification.destiny.email])

