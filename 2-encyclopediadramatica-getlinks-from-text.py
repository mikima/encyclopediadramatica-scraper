import requests
import urllib2, json, csv, re

#firce Unicode
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# set up the csv file
out_name = 'links-from-text'
ofile  = open(out_name + '.csv', "wb")
writer = csv.writer(ofile, delimiter='\t', quotechar='"')
writer.writerow(["source","target"])
# set up error csv
errFile  = open('links-errors.csv', "wb")
errWriter = csv.writer(errFile, delimiter='\t', quotechar='"')

def getLinksFromText(endpoint, page, _writer):

	baseurl = endpoint + "/api.php"

	params = {}
	params['action'] = 'query'
	params['prop'] = 'revisions'
	params['rvprop'] = 'content'
	params['format'] = 'json'
	params['titles'] = page

	r = requests.get(baseurl, params = params)
	data = r.json()

	#get page id
	pageid = data['query']['pages'].keys()[0]

	wikitext = data['query']['pages'][pageid]['revisions'][0]['*']

	regex = re.compile(r'\[\[([^:]+?)\]\]', re.I)
	links = regex.findall(wikitext)

	results = []

	for link in links:
		if '|' in link:
			link = link.split('|')[0]

		if '#' in link:
			link = link.split('#')[0]
		print page,link
		_writer.writerow([page,link])
		results.append(link)

	return results

def get_links(altpedia, page, _writer):
	# example url https://encyclopediadramatica.rs/api.php?action=query&titles=Mark%20Zuckerberg&prop=links&format=json&pllimit=500
	# api ref https://www.mediawiki.org/wiki/API:Links
	baseurl = altpedia + "/api.php"

	params = {}
	params['action'] = 'query'
	params['format'] = 'json'
	params['prop'] = 'links'
	params['pllimit'] = '500'
	params['titles'] = page

	querycontinue = True
	results = []

	while querycontinue == True:
		r = requests.get(baseurl, params = params)
		data = r.json()

		pageid = next(iter(data['query']['pages']))

		results = results + data['query']['pages'][pageid]['links']

		if _writer:
			for item in data['query']['pages'][pageid]['links']:
				print page, item['title']
				_writer.writerow([page, item['title']])

		if 'continue' in data:
			params['plcontinue'] = data['continue']['plcontinue']
		else:
			querycontinue = False

	return results

#links = get_links('https://encyclopediadramatica.rs','Mark Zuckerberg', writer)
count = 0;

with open('pages.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter='\t')
	# skip fist Line
	next(readCSV, None)

	for row in readCSV:
		count = count + 1
		print count
		try:
			getLinksFromText('https://encyclopediadramatica.rs',row[2], writer)
		except:
			print 'error: ', row[2]
