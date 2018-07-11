import requests
import urllib2, json, csv

#firce Unicode
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# set up the csv file
out_name = 'redirects-table'
ofile  = open(out_name + '.csv', "wb")
writer = csv.writer(ofile, delimiter='\t', quotechar='"')
writer.writerow(["source","target"])


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

		print data

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

with open('pages-only-redirects.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter='\t')
	# skip fist Line
	next(readCSV, None)

	for row in readCSV:
		try:
			get_links('https://encyclopediadramatica.rs',row[2], writer)
		except:
			errWriter.writerow(row[2])
