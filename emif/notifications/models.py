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

from django.db import models
from django.contrib.auth.models import User

# Model for a new notification
class Notification(models.Model):
    MESSAGE = 0
    SYSTEM = 1
    NOTIFICATION_TYPES = (
        (MESSAGE, 'Private Message'),
        (SYSTEM, 'System Notification'),
    )
    destiny = models.ForeignKey(User, related_name="destiny") # destinatary user for the notifications
    origin = models.ForeignKey(User, related_name="origin") #all notification have origin (this way we may later use this as a messaging system also ?)
    type = models.IntegerField(choices=NOTIFICATION_TYPES, default=SYSTEM)
    href = models.TextField(null=True) # this page can have a reference to somewhere
    notification = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    read_date = models.DateTimeField(null=True)
    read = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.notification)
