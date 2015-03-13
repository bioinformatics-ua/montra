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

from django.contrib import admin
from django.contrib.auth.models import User
from adminplus.sites import AdminSitePlus

from django.shortcuts import render

from django.forms import ModelForm, ModelChoiceField

from django import forms
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from django.db.models import Count, Avg, Max, Min

from django.utils import timezone
import datetime

from .models import *
from django_ace import AceWidget

class PluginVersionInline(admin.TabularInline):
    model = PluginVersion

class PluginAdmin(admin.ModelAdmin):
    inlines = [
        PluginVersionInline,
    ]
    list_display = ['name', 'type', 'owner', 'removed']

class PluginVersionForm(forms.ModelForm):
    path = forms.CharField(widget=AceWidget(mode='javascript', theme='github', width="90%"))


class PluginVersionAdmin(admin.ModelAdmin):
    form = PluginVersionForm
    def queryset(self, request):

        qs = super(PluginVersionAdmin, self).queryset(request)

        return qs.filter(approved=False, submitted=True)

    list_display = ['plugin', 'version', 'submitted', 'approved']
admin.site.register(Plugin, PluginAdmin)
admin.site.register(PluginVersion, PluginVersionAdmin)

