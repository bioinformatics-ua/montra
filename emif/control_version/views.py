# -*- coding: utf-8 -*-

# Copyright (C) 2014 Luís A. Bastião Silva and Universidade de Aveiro
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

from django.shortcuts import render
from control_version.github import report_bug, issues_handler
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from control_version.models import BugReport

# Bug Report
def bug_report(request, template_name='bugreport.html'):
    return report_bug(request)

def list_issues(request, template_name='list_issues.html'):
    return issues_handler(request)

def list_labels(request, template_name='bugreport.html'):
    return report_bug(request)

@csrf_exempt
def github_event(request):

    body = json.loads(request.body)

    try:
        action = body.get('action')

        if action == 'closed':
            issue = body.get('issue')
            number = issue['number']

            BugReport.close(number, send_mail=True)

    except KeyError:
        return HttpResponse('Forbidden', status=403)

    return HttpResponse('')
