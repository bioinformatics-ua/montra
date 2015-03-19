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
import os

from django.conf import settings
if settings.DEBUG:
    PATH_STORE_FILES = settings.PROJECT_DIR_ROOT  + 'emif/static/files/'
else:
    PATH_STORE_FILES = settings.PROJECT_DIR_ROOT  + settings.MIDDLE_DIR +'static/files/'

class HandleFile(object):
    """This class handle with the file upload for multiple backends
    """
    def __init__(self, wrapper):
        self._handler_wrapper = wrapper

    def handle_file(self, f, revision=""):
        """
        Handle File
        """
        return self._handler_wrapper.handle_uploaded_file(f, revision=revision)

        # Store the metadata

class FileSystemHandleFile(object):
    """Store the file in file system
    """
    def __init__(self):
        pass

    def __get_path_abs(self, path):
        # check if file exists

        # if the file exists...warning
        pass



    def handle_uploaded_file(self, f, revision=""):
        """Store the files in file disk
        """
        full_name = revision+f.name
        with open(os.path.join(os.path.abspath(PATH_STORE_FILES), full_name),
                  'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return os.path.join(os.path.abspath(PATH_STORE_FILES), full_name)

class MongoDBHandleFile(object):
    """Store the file in MongoDB
    """
    def __init__(self):
        pass

    def handle_uploaded_file(self, f,  revision=""):
        """Store the files in file disk
        """
        pass

