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

from __future__ import absolute_import

from celery import shared_task

from django.contrib.auth.models import User

from developer.models import Plugin, PluginVersion
from emif.utils import send_custom_mail

from django.conf import settings

@shared_task
def sendCommitEmails(p, pv):
    emails = [p.owner.email]
    adict = dict(settings.ADMINS)
    for admin in adict:
        emails.append(adict[admin])

    desc = ""
    if pv.submitted_desc:
        desc = """
            The following description was added:\n
                "
                %s
                " """ % (pv.submitted_desc)
    # sent email to admin and developer about plugin
    try:
        send_custom_mail('EMIF Catalogue: Plugin %s v.%s submitted for approval' % (p.name, pv.version),
            """Dear Colleague,\n
                    A new plugin version %s for plugin %s has been submitted for approval on the platform <a href="http://bioinformatics.ua.pt/emif">EMIF Catalogue</a>.

                    %s

                    The system administrators will review and approve it as soon as possible.\n
                    \n\n
                    \n\nSincerely,\nEMIF Catalogue
            """ %(pv.version, p.name, desc), settings.DEFAULT_FROM_EMAIL, emails)
    except:
        print "Couldn't send email for commit approval"
