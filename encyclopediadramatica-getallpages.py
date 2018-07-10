import requests
import urllib2, json, csv

def get_allpages(altpedia):
	#url = http://en.wikipedia.org/w/api.php?action=query&format=json&list=backlinks&bllimit=250&blredirect&bltitle=Open_data
	#https://encyclopediadramatica.rs/api.php?action=query&list=allpages&aplimit=500&format=json
	baseurl = altpedia + "/api.php"

	params = {}
	params['action'] = 'query'
	params['format'] = 'json'
	params['list'] = 'allpages'
	params['aplimit'] = '500'

	querycontinue = True
	results = []

	while querycontinue == True:
		r = requests.get(baseurl, params = params)
		data = r.json()

		print data['query']['allpages']

		results = results + data['query']['allpages']

		if 'continue' in data:
			params['apcontinue'] = data['continue']['apcontinue']
		else:
			querycontinue = False

	return results

backlinks = get_allpages('https://encyclopediadramatica.rs')
print json.dumps(backlinks, sort_keys=False, separators=(',', ': '))
