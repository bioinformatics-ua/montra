import sys, json, csv
from random import randint, choice, uniform, random, sample

# read the number of markers to add from the input arguments
numMarkers = sys.argv[1]

cr = csv.reader(open("../iso-codes.csv","rb"))
countries={}
i = 0
for row in cr:
	v, k = row
	countries[i] = v
	i = i +1

# filters
filters = [
	{
		'name': 'gender',
		'continuous' : 'false',
		'values': [
			'M',
			'F',
			'T'
		]
	},
	{
		'name' : 'year',
		'continuous' : 'true',
		'min' : 2010,
		'max' : 2014
	},
	{
		'name':'height',
		'continuous' : 'true',
		'min': 100,
		'max': 200
	},
	{
		'name' : 'weight',
		'continuous': 'true',
		'min': 20,
		'max': 200
	}
]

# create a JSON object
jsonArray = []

for i in range(int(numMarkers)):
	# create a new marker
	jsonObject = {}
	jsonObject['count'] = randint(1000,2000)
	jsonObject['country'] = choice(countries)
	jsonObject['latitude'] = uniform(-90, 90)
	jsonObject['longitude'] = uniform(-180, 180)
	# generate attributes
	attributes = {}
	for filter in filters:
		filterName = filter['name']
		if filter['continuous'] == 'false':
			# discrete values - pick one value from values
			attributes[filterName] = sample(filter['values'], 1)
		else:
			# continuous - pick one random number between the range
			attributes[filterName] = randint(filter['min'],filter['max'])
	jsonObject['attributes'] = attributes
	jsonObject['icon'] = sample(['red','green','blue'], 1)
	jsonArray.append(jsonObject)

with open('../json/test-markers.json', 'w') as outfile:
    json.dump(jsonArray, outfile)

with open('../json/test-filters.json', 'w') as outfile:
    json.dump(filters, outfile)
