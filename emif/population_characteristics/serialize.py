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

import mimetypes
import re
from django.core.urlresolvers import reverse

# Code adapted from: https://github.com/sigurdga/django-jquery-file-upload

def serialize(instance, file_attr='file'):
    """serialize -- Serialize a File instance into a dict.

    instance -- File instance
    file_attr -- attribute name that contains the FileField or ImageField

    """

    return {
        'url': '#',
        'name': instance.name,
        #'type': mimetypes.guess_type(obj.path)[0] or 'image/png',
        'type': 'unknown',
        'thumbnailUrl': '#',
        'size': instance.size,
        'deleteUrl': '#',
        'deleteType': 'DELETE',
    }
