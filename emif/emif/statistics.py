


from questionnaire.models import Question
from searchengine.search_indexes import CoreEngine

class Statistic(object):


	def __init__(self, question):
		self.question = question 
		self.search = CoreEngine()


	def get_percentage(self):
		slug = self.question.slug 
		results = self.search.search_fingerprint(slug + ":*")
		values = dict()
		for r in results:
			for k in r:
				try:
					if (not values.has_key(r[k])):
						values[r[k]] = values[r[k]]
					else:
						values[r[k]] = 1
				except:
					continue

	def tag_cloud(self):
		pass








