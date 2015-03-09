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

from django.views.generic import TemplateView
from django.shortcuts import render, redirect

from .models import *
from django import forms

class DeveloperListView(TemplateView):
    template_name = "developer.html"

    def get(self, request, **kwargs):
        success=None
        try:
            success = kwargs['success']
        except KeyError:
            pass

        return render(request, self.template_name,
            {
                'developer': True,
                'plugins': Plugin.all(owner=request.user),
                'request': request,
                'breadcrumb': True,
                'success': success
            })

    def post(self, request):
        slug = request.POST.get('slug', None)

        if slug != None:
            success = Plugin.remove(slug)
            return self.get(request, success=success)

        return self.get(request)

class DeveloperDetailView(TemplateView):
    template_name = "developer_detail.html"

    def get(self, request, plugin_hash):

        return render(request, self.template_name,
            {
                'request': request,
                'breadcrumb': True,
                'plugin': True,
            })



class PluginForm(forms.ModelForm):
    class Meta:
        model = Plugin
        fields = ['name', 'type']

class DeveloperAddView(TemplateView):
    template_name   = "developer_detail.html"
    form_class      = PluginForm
    success_url     = '/thanks/'

    def get(self, request):

        new_plugin = PluginForm()

        return render(request, self.template_name,
            {
                'request': request,
                'breadcrumb': True
            })

