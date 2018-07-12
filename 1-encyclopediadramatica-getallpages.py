import requests
import urllib2, json, csv

# set up the csv file
out_name = 'pages'
ofile  = open(out_name + '.csv', "wb")
writer = csv.writer(ofile, delimiter='\t', quotechar='"')
writer.writerow(["pageid","ns","title"])

def get_allpages(altpedia, _writer):
	#url = http://en.wikipedia.org/w/api.php?action=query&format=json&list=backlinks&bllimit=250&blredirect&bltitle=Open_data
	#https://encyclopediadramatica.rs/api.php?action=query&list=allpages&aplimit=500&format=json
	# api https://www.mediawiki.org/wiki/API:Allpages
	baseurl = altpedia + "/api.php"

	params = {}
	params['action'] = 'query'
	params['format'] = 'json'
	params['list'] = 'allpages'
	params['aplimit'] = '500'
	params['apfilterredir'] = 'nonredirects'

	querycontinue = True
	results = []

	while querycontinue == True:
		r = requests.get(baseurl, params = params)
		data = r.json()

		if _writer:
			for item in data['query']['allpages']:
				newrow = [item['pageid'], item['ns'], item['title'].encode('utf-8')];
				print item
				_writer.writerow([item['pageid'], item['ns'], item['title'].encode('utf-8')]);

		results = results + data['query']['allpages']

		if 'continue' in data:
			params['apcontinue'] = data['continue']['apcontinue']
		else:
			querycontinue = False

	return results

get_allpages('https://encyclopediadramatica.rs', writer)
