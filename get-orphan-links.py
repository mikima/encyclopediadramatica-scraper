import requests
import urllib2, json, csv

#firce Unicode
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sources = {}
targets = {}
orphans = {}

# api https://www.mediawiki.org/wiki/API:Query#Resolving_redirects
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
		results = [page, True, data['query']['redirects'][0]['to']]
	except:
		results = [page, False,'']
		print 'error: ', page

	return results


# set up the csv file
out_name = 'redirects-table'
ofile  = open(out_name + '.csv', "wb")
writer = csv.writer(ofile, delimiter='\t', quotechar='"')
writer.writerow(["page","exists","redirect"])


#open source file
with open('links.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter='\t')
	# skip fist Line
	next(readCSV, None)

	for row in readCSV:
		if row[0] not in sources:
			sources[row[0]] = True
		if row[1] not in targets:
			targets[row[1]] = True

	print 'sources: ', len(sources)
	print 'targets: ', len(targets)

	#now check targets
	it = 0

	for item in targets:
		
		it = it+1

		if item not in sources:
			orphans[item] = True
			percent = it/len(targets)*100.0
			print it, '/', len(targets), ' - ', percent, '%'
			redirr = get_redirect('https://encyclopediadramatica.rs', item)
			writer.writerow(redirr)


	print 'orphans: ', len(orphans)
	# for key, value in targets.iteritems():
	# 	if key not in sources:
	# 		it = it+1
	# 		orphans[key] = get_redirect('https://encyclopediadramatica.rs', key)
	# 		print it,'/',len(targets)
	# 		writer.writerow(orphans[key])
