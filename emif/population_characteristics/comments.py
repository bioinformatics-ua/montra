# -*- coding: utf-8 -*-
# Copyright (C) 2014 Luís A. Bastião Silva and Universidade de Aveiro
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

# import the logging library
import logging


from .models import * 

logger = logging.getLogger(__name__)

"""
Management of comments 
"""


class CommentManager(object):


    def __init__(self, fingerprint_id):
        self.fingerprint_id=fingerprint_id
        logger.debug('Fingerprint id: %s' % fingerprint_id)

    """
    Comment for a specific chart of a a fingerprint 
    """
    def comment(self, chart_id, title, description, user):
        comments = Comments()
        comments.user = user
        comments.fingerprint_id = self.fingerprint_id
        jerboa_documents = Characteristic.objects.filter(fingerprint_id=self.fingerprint_id).order_by('latest_date')
        contains_population = len(jerboa_documents)!=0
        comments.document = jerboa_documents[0]
        comments.title = title 
        comments.description = description
        comments.save()
        logger.error('comments is: %s' % comments.__str__())
        return comments 

    """List of comments for a specific chart of a specific fingerprint id
    """
    def list_comments(self, fingerprint_id, chart_id):
        pass




