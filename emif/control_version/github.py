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
#
from github3 import login
from control_version.models import *
from django.shortcuts import render
from django.conf import settings
from emif.utils import send_custom_mail


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

            description = "<strong>Description: </strong>"+request.POST.get('description', '').encode('ascii', 'ignore')
            description += "\n<strong>Steps to reproduce: </strong>"+request.POST.get('steps', '').encode('ascii', 'ignore')
            description += "\n<strong>Expected result: </strong>"+request.POST.get('expected', '').encode('ascii', 'ignore')
            description += "\n<strong>Priority: </strong>"+request.POST.get('priority', '').encode('ascii', 'ignore')

            from_email = request.user.email
            issue = IssueManager(settings.GITHUB_USERNAME, settings.GITHUB_PASSWD)
            browser = ''
            try:
                browser = request.META['HTTP_USER_AGENT']
            except:
                pass

            description = description + "\n\nReported by %s, email: %s with: %s" % (name, from_email, browser)
            issue.create(title, description)

            emails_to_feedback = [from_email]
            for k, v in settings.ADMINS:
                emails_to_feedback.append(v)

            try:
                send_custom_mail(title, description, settings.DEFAULT_FROM_EMAIL, emails_to_feedback)
            except:
                pass
            return feedback_thankyou(request)

    else:
        form = BugReportForm()  # An unbound form
    return render(request, 'bugreport.html', {'form': form, 'request': request, 'breadcrumb': True})

def issues_handler(request):
    issue = IssueManager(settings.GITHUB_USERNAME, settings.GITHUB_PASSWD)
    error_loading_issues = False

    try:
        issues_open = issue.list('open', None)
    except:
        issues_open = []
        error_loading_issues = True

    try:
        issues_closed = issue.list('closed', None)
    except:
        issues_closed = []
        error_loading_issues = True

    try:
        milestones = issue.list_milestones()
    except:
        raise
        milestones = []
        error_loading_issues = True



    return render(request, 'list_issues.html', {'request': request,
     'breadcrumb': True,
     'issues_open': issues_open, 'issues_closed':issues_closed, 'milestones': milestones})

class IssueManager(object):
    def __init__(self, user, pw):
        self.gh = login(user, pw)

    def create(self, title, body ):
        return self.gh.create_issue(settings.GITHUB_ACCOUNT,settings.GITHUB_REPO, title, body, labels=['bugreport'])

    def list(self, state_of, labels_of):
        """
        should do:
        for i in issuemanager.list(state='open'):
            print i.created_at
            print i.body_text
            print i.title

        """
        return self.gh.iter_repo_issues(settings.GITHUB_ACCOUNT,settings.GITHUB_REPO, state=state_of, labels=labels_of)

    def list_labels(self):
        # I'm adding this shit statically due to the use case of the EMIF Catalogue
        # It's the only way that this will make sense.
        return ['Use Case 1', 'Use Case 2', 'Use Case 3', 'Use Case 4', 'Use Case 5', 'Use Case 6']

    def list_milestones(self):
        repo = self.gh.repository(settings.GITHUB_ACCOUNT,settings.GITHUB_REPO)

        # for some reason i couldnt find out,
        # milestones iterator only returns open milestones when used without state parameter
        # so i join them up myself...
        milestones = []
        miles_open = repo.iter_milestones()
        miles_closed = repo.iter_milestones(state='closed')

        for mile in miles_closed:
            milestones.append(mile)

        for mile in miles_open:
            milestones.append(mile)

        return milestones[::-1]
