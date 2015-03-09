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

class DeveloperListView(TemplateView):
    template_name = "developer.html"

    def get(self, request):

        return render(request, self.template_name,
            {
                'plugins': Plugin.all(owner=request.user),
                'request': request,
                'breadcrumb': True
            })

class DeveloperDetailView(TemplateView):
    template_name = "developer_detail.html"

    def get(self, request, plugin_hash):

        return render(request, self.template_name,
            {
                'request': request,
                'breadcrumb': True,
                'plugin': True,
            })

class DeveloperAddView(TemplateView):
    template_name = "developer_detail.html"

    def get(self, request):

        return render(request, self.template_name,
            {
                'request': request,
                'breadcrumb': True
            })

