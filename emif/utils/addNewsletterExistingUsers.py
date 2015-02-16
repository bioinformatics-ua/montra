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
from django.contrib.auth.models import User
from newsletter.models import Subscription, Newsletter

def importUsers():

    try:
        newsl = Newsletter.objects.get(slug='emif-catalogue-newsletter')


        users = User.objects.all()

        for user in users:
            try:
                subscription = Subscription.objects.get(user=user,  newsletter=newsl)

            except Subscription.DoesNotExist:
                # create subscription if doesnt exist yet
                user_sub = Subscription(user=user,  newsletter=newsl)

                user_sub.subscribe()

                user_sub.save()

                print "-- Created subscription for emif newsletter to user "+str(user.username)

                pass

    except Newsletter.DoesNotExist:
        print "Problem finding default newsletter for emif"

importUsers()
