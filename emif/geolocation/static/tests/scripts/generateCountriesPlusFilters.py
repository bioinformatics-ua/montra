import sys, json, csv
from random import randint, choice, uniform, random, sample

# read the number of countries to add from the input arguments
numCountries = int(sys.argv[1])

cr = csv.reader(open("../iso-codes.csv","rb"))
countries=[]
i = 0
for row in cr:
	v, k = row
	countries.append(v)

# create a JSON object
jsonArray = []

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
		'continuous' : 'false',
		'values' : [
			2010,
			2011,
			2012,
			2013
		]
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

# validate the number of countries to generate (max)
if(numCountries > len(countries)):
	print 'Max number of countries is ', len(countries)
	sys.exit()

for i in range(numCountries):
	# create a new country
	jsonObject = {}
	# count
	jsonObject['count'] = randint(1000,2000)
	# name
	selectedCountry = choice(countries)
	countries.remove(selectedCountry)
	jsonObject['name'] = selectedCountry
	# attributes
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
	jsonArray.append(jsonObject)

# write countries
with open('../json/test-countries.json', 'w') as outfile:
    json.dump(jsonArray, outfile)

# write filters
with open('../json/test-filters.json', 'w') as outfile:
    json.dump(filters, outfile)
