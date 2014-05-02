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


from questionnaire.models import Question
from searchengine.search_indexes import CoreEngine


class Statistic(object):
    def __init__(self, question):
        self.question = question
        self.search = CoreEngine()

    def get_percentage(self):
        #slug = self.question.slug
        slug = self.question.slug_fk.slug1
        # print slug
        type_id = self.question.questionset.questionnaire.slug

        if slug is None:
            return None
        results = self.search.search_fingerprint(slug + "_t:* AND type_t:" + type_id, 0, 100, slug + "_t")
        values = []
        # print "RESULTS: " + str(results.__len__())
        if results:
            values_aux = dict()
            for r in results:

                for s in r.values()[0].split("#"):
                    
                    if s:
                        try:
                            if s in values_aux.keys():
                                values_aux[s] += 1
                            else:
                                values_aux[s] = 1
                        except:
                            raise
            values.append(values_aux)

        return values

    def tag_cloud(self):
        # http://www.jason-palmer.com/2011/05/creating-a-tag-cloud-with-solr-and-php/
        # solr = query = "(.................. )"
        # solr.search([solrquery],facet = 'on' ,** {'facet.field' : ['fieldname']})
        pass


class Timeline(object):
    def __init__(self):
        pass


