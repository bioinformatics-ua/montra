# -*- coding: utf-8 -*-

# Copyright (C) 2013 Luís A. Bastião Silva and Universidade de Aveiro
#
# Authors: Luís A. Bastião Silva <bastiao@ua.pt>
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


from github3 import login
from emif.models import *
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError



"""
Put this variables in settings.py or local_settings.py
GITHUB_USERNAME='bastiao'
GITHUB_PASSWD='GOFUCKYOURSELF'
GITHUB_ACCOUNT='bioinformatics-ua'
GITHUB_REPO='emif-fb'
"""

def feedback_thankyou(request, template_name='feedback_thankyou.html'):
    return render(request, template_name, {'request': request, 'breadcrumb': True})

def report_bug(request):

    if request.method == 'POST':  # If the form has been submitted...
        form = BugReportForm(request.POST)
        if form.is_valid():  # All validation rules pass

            title = request.POST.get('title', '').encode('ascii', 'ignore')
            name = request.user.get_full_name()
            description = request.POST.get('description', '').encode('ascii', 'ignore')
            from_email = request.user.email
            issue = Issue(settings.GITHUB_USERNAME, settings.GITHUB_PASSWD)
            description = description + "\n\nReported by %s, email: %s" % (name, from_email)
            issue.create(title, description)
            
            try:
                send_mail(title, description, settings.DEFAULT_FROM_EMAIL, [from_email])
            except:
                pass
            return feedback_thankyou(request)

    else:
        form = BugReportForm()  # An unbound form
    return render(request, 'bugreport.html', {'form': form, 'request': request, 'breadcrumb': True})




class Issue(object):
	def __init__(self, user, pw):
		self.gh = login(user, pw)

	def create(self, title, body ):
		return self.gh.create_issue(settings.GITHUB_ACCOUNT,settings.GITHUB_REPO, title, body)

"""
>>> from github3 import login
>>> gh = login('bastiao','GOFUCKYOURSELF')
>>> gh.create_issue('bioinformatics-ua', 'emif-fb', 'bastiao test inserting issue programtically')
"""
