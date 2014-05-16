
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


# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from searchengine.models import ContactForm
from django.template import RequestContext, Context
from django import forms

from django.core.mail import BadHeaderError
from emif.utils import send_custom_mail

def contactview(request, email):
		subject = request.POST.get('topic', '')
		message = request.POST.get('message', '')
		from_email = request.POST.get('email', '')

		if subject and message and from_email:
		        try:
					send_custom_mail(subject, message, "bioinformatics@ua.pt", [from_email, 'bastiao@ua.pt'])
        		except BadHeaderError:
            			return HttpResponse('Invalid header found.')
        		return HttpResponseRedirect('http://bioinformatics.ua.pt/emif/contact/thankyou/')
		else:
			return render_to_response('contact_form.html', {'form': ContactForm(), 'email_to': email}, RequestContext(request))
	
		return render_to_response('contact_form.html', {'form': ContactForm()},
			RequestContext(request))


def thankyou(request):
		return render_to_response('contact_thankyou.html')
