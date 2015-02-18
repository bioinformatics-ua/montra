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

from accounts.models import *
import sys

print '\nbegin adding profiles to users...\n'

if not Profile.objects.all().count():
	p1 = Profile(name='Data Custodian', description='some dummy description for data custodian profile')
	p1.save()
	p2 = Profile(name='Researcher', description='some dummy description for researcher profile')
	p2.save()

for ep in EmifProfile.objects.all():
	print '\n'
	print ep
	for p in Profile.objects.all():
		print 'Adding profile ' + p.name + ' to ' + ep.user.email
		ep.profiles.add(p)
	for i in Questionnaire.objects.all():
		print 'Adding interest ' + i.name + ' to ' + ep.user.email
		ep.interests.add(i)

print '\nend!'
