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
from django.http import Http404, HttpResponseRedirect


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

    def get(self, request, plugin_hash, add=False, update=False):
        plugin = None
        try:
            plugin = Plugin.objects.get(slug=plugin_hash)
        except Plugin.DoesNotExist:
            pass

        return render(request, self.template_name,
            {
                'request': request,
                'breadcrumb': True,
                'plugin': plugin,
                'plugin_types': Plugin.TYPES,
                'add': add,
                'update': update

            })

class DeveloperPluginSaveView(TemplateView):
    template_name = 'developer_detail.html'
    def post(self, request):
        plugin = None

        plugin_hash = request.POST.get('plugin_hash', None)
        name = request.POST.get('name', None)
        type = request.POST.get('type', None)

        # create
        if plugin_hash == '':

            plugin = Plugin.create(name, type, request.user)

            if plugin != None:
                return redirect('developer-detail', plugin_hash=plugin.slug)

        # update
        elif plugin_hash != None:
            plugin = Plugin.update(plugin_hash, name, type, request.user)
            if plugin != None:
                return redirect('developer-detail', plugin_hash=plugin.slug)

        # error request
        raise Http404

class PluginForm(forms.ModelForm):
    class Meta:
        model = Plugin
        fields = ['name', 'type']

class DeveloperAddView(TemplateView):
    template_name   = "developer_detail.html"
    form_class      = PluginForm
    success_url     = '/thanks/'

    def get(self, request):

        return render(request, self.template_name,
            {
                'request': request,
                'breadcrumb': True,
                'plugin_types': Plugin.TYPES
            })

class DeveloperVersionView(TemplateView):
    template_name   = "developer_version.html"

    def post(self, request, plugin_hash, version=None):
        v = None

        version_new = request.POST.get('version', None)
        is_remote = request.POST.get('is_remote', None)
        data = request.POST.get('data', None)

        # consider a creation of version
        if version == None:
            v = PluginVersion.create(plugin_hash, version_new, is_remote, path, code)
        # this is just an update
        else:
            v = PluginVersion.update(plugin_hash, version, version_new, is_remote, data)

        return self.get(request, plugin_hash, v.version)

    def get(self, request, plugin_hash, version=None):
        plugin = version_obj = None
        try:
            plugin = Plugin.objects.get(slug=plugin_hash)
        except Plugin.DoesNotExist:
            pass

        try:
            version_obj = PluginVersion.all(plugin=plugin).get(version=version)
        except PluginVersion.DoesNotExist:
            pass

        print version

        return render(request, self.template_name,
            {
                'request': request,
                'breadcrumb': True,
                'plugin': plugin,
                'version': version_obj
            })
