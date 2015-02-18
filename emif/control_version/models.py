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

