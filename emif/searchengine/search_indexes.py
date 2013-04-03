#!/usr/bin/env python
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


"""A module for Python index

.. moduleauthor:: Luís A. Bastião Silva <bastiao@ua.pt>

"""

from __future__ import print_function
import pysolr


from questionnaire.models import Answer, Question

"""
Convert a answer from questionarie to a JSON document to be indexed by SOLR
"""
def convert_answer_to_json(question_id,answers):
	# Get the questions

	response = dict()

	for answer in answers:
		question_key = answer.question.text
		question_value = answer.answer 
		response[question_key] = question_value

	# Convert to JSON
	response_json =  JSONEncoder().encode(response)

	return response_json


"""It is responsible for index the documents and search over them
It also connects to SOLR
"""
class IndexEngine:
	CONNECTION_TIMEOUT_DEFAULT = 10
	def __init__(self, timeout=CONNECTION_TIMEOUT_DEFAULT):
		# Setup a Solr instance. The timeout is optional.
		self.solr = pysolr.Solr('http://localhost:8983/solr/', timeout=timeout)

	def index_fingerprint(self, doc):
		"""Index fingerprint 
		"""
		# index document
		self.solr.add(convert_answer_to_json(doc))
		self.optimize()

	def optimize(self):
		"""This function optimize the index. It improvement the search and retrieve documents subprocess.
		However, it is a hard tasks, and call it for every index document might not be a good idea.
		"""
		self.solr.optimize()

	def update(self, doc):
		"""Update the document
		"""
		# Search  and identify the document id

		# Delete 
		self.solr.delete(id='doc_1')

		# Index the new document
		self.index(doc)

	def search_fingerprint(self, query):
		"""search the fingerprint
		"""
		# Later, searching is easy. In the simple case, just a plain Lucene-style
		# query is fine.
		results = self.solr.search(query)

		# # The ``Results`` object stores total results found, by default the top
		# # ten most relevant results and any additional data like
		# # facets/highlighting/spelling/etc.
		# print("Saw {0} result(s).".format(len(results)))

		# # Just loop over it to access the results.
		# for result in results:
		#     print("The title is '{0}'.".format(result['title'])

		# For a more advanced query, say involving highlighting, you can pass
		# additional options to Solr.
		results = self.solr.search('bananas', **{
		    'hl': 'true',
		    'hl.fragsize': 10,
		})
		return results

	def more_like_this(self, id_doc):
		pass

		# You can optimize the index when it gets fragmented, for better speed.

		# You can also perform More Like This searches, if your Solr is configured
		# correctly.
		similar = self.solr.more_like_this(q='id:doc_2', mltfl='text')

		# Finally, you can delete either individual documents...
		solr.delete(id='doc_1')

		# ...or all documents.
		solr.delete(q='*:*')