import requests
import urllib2, json, csv

#firce Unicode
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#function to get Redircts
def get_redirect(altpedia, page):

	baseurl = altpedia + "/api.php"

	params = {}
	params['action'] = 'query'
	params['format'] = 'json'
	params['redirects'] = ''
	params['titles'] = page

	results = []

	r = requests.get(baseurl, params = params)
	data = r.json()

	print data

	try:
		if 'redirects' in data['query']:
			results = [page, True, data['query']['redirects'][0]['to']]
		elif 'normalized' in data['query']:
			results = [page, True, data['query']['normalized'][0]['to']]
		else:
			results = [page, False,'']
	except:
		results = [page, False,'']
		print 'error: ', page

	return results


#first, dict with pages
pages = {}

with open('pages-no-redirects.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter='\t')
	# skip fist Line
	next(readCSV, None)

	for row in readCSV:
		pages[row[2]] = True

# set up the csv file
out_name = 'targets-redirects-second'
ofile  = open(out_name + '.csv', "wb")
writer = csv.writer(ofile, delimiter='\t', quotechar='"')
writer.writerow(["page","exists","redirect"])

count = 0
with open('list-of-unique-targets-second-tranche.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter='\t')
	# skip fist Line
	next(readCSV, None)


	for row in readCSV:
		count = count + 1
		print count
		if row[0] in pages:
			writer.writerow([row[0],True,row[0]])
		else:
			print 'get redirect ',row[0]
			redirr = get_redirect('https://encyclopediadramatica.rs', row[0])
			print ' =>',redirr
			writer.writerow(redirr)
