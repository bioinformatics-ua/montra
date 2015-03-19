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
from django.db import models

from django.contrib.auth.models import User
from django.db import models

from django.db.models.fields import *
from django import forms

from emif.utils import send_custom_mail
from django.conf import settings
from django.utils import timezone

class OpenBugReportManager(models.Manager):
    def get_queryset(self):
        return super(OpenBugReportManager, self).get_queryset().filter(closed=False)

class BugReport(models.Model):
    # github issue generated
    issue = models.IntegerField()
    requester = models.ForeignKey(User)
    report = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField(null=True)
    closed = models.BooleanField(default=False)

    # Manager that returns only open issues
    open = OpenBugReportManager()

    @staticmethod
    def close(issue_number, send_mail=False):
        try:
           bugreport = BugReport.open.get(issue=issue_number)

           bugreport.closed = True
           bugreport.close_date = timezone.now()


           if send_mail:
               send_custom_mail('EMIF Catalogue: Bug Report #%d solved' % (issue_number),
                """ Dear %s,\n\n
                    The following bug report:\n
                    <blockquote>
                    %s\n
                    </blockquote>
                    has been solved by our development team, and will be incorporated in our next scheduled system update.
                    \n\n
                    Sincerely,\n
                    EMIF Catalogue
                """ % (bugreport.requester.get_full_name(), bugreport.report),
                settings.DEFAULT_FROM_EMAIL,
                [bugreport.requester.email])



           bugreport.save()

        except BugReport.DoesNotExist:
            pass

    def __str__(self):
        return self.issue

class BugReportForm(forms.Form):
    NOP = 'Not really a problem'
    LOW = 'Low Priority'
    MED = 'Medium Priority'
    HIGH = 'High Priority'
    CRIT = 'Critical Priority'
    PRIORITIES = (
        (LOW, 'Low Priority'),
        (MED, 'Medium Priority'),
        (HIGH, 'High Priority'),
        (CRIT, 'Critical Priority'),
        (NOP, 'Not really a problem'),

    )
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'class': 'span6', 'placeholder': 'Title'}))
    description = forms.CharField(label='Description', initial='',
        widget=forms.Textarea(attrs={'cols': 30, 'rows': 4, 'class': 'span6', 'placeholder': 'Description'}))

    steps = forms.CharField(label='Steps to reproduce', initial='',
        widget=forms.Textarea(attrs={'cols': 30, 'rows': 4, 'class': 'span6', 'placeholder': 'Steps to reproduce'}))

    expected = forms.CharField(label='Expected Result', initial='',
        widget=forms.Textarea(attrs={'cols': 30, 'rows': 4, 'class': 'span6', 'placeholder': 'Expected Result'}))

    priority = forms.ChoiceField(label='Priority', choices=PRIORITIES,
        widget=forms.Select(attrs={'class': 'span6', 'placeholder': 'Priority'}))

