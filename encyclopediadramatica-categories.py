import requests
import urllib2, json, csv

#firce Unicode
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def getAllCategories():
	# https://encyclopediadramatica.rs/api.php?action=query&list=allcategories&format=json&aclimit=500
	# https://www.mediawiki.org/wiki/API:Allcategories
	baseurl = "https://encyclopediadramatica.rs/api.php"

	params = {}
	params['action'] = 'query'
	params['format'] = 'json'
	params['list'] = 'allcategories'
	params['aclimit'] = '500'

	querycontinue = True
	results = []

	while querycontinue == True:
		r = requests.get(baseurl, params = params)
		data = r.json()

		results = results + data['query']['allcategories']

		if 'continue' in data:
			params['accontinue'] = data['continue']['accontinue']
		else:
			querycontinue = False

	return results

def getCategoryMembers(category):
	# https://encyclopediadramatica.rs/api.php?action=query&list=categorymembers&cmtitle=Category:Trump&format=json
	# https://www.mediawiki.org/wiki/API:Categorymembers
	baseurl = "https://encyclopediadramatica.rs/api.php"

	params = {}
	params['action'] = 'query'
	params['format'] = 'json'
	params['list'] = 'categorymembers'
	params['cmtitle'] = 'Category:' + category
	params['cmlimit'] = '500'

	querycontinue = True
	results = []

	while querycontinue == True:
		r = requests.get(baseurl, params = params)
		data = r.json()

		results = results + data['query']['categorymembers']

		if 'continue' in data:
			params['cmcontinue'] = data['continue']['cmcontinue']
		else:
			querycontinue = False

	return results

# set up the csv file
out_name = 'categories-pages'
ofile  = open(out_name + '.csv', "wb")
writer = csv.writer(ofile, delimiter='\t', quotechar='"')
writer.writerow(["category","pageid","ns","title"])

categories = getAllCategories()
#print json.dumps(categories, sort_keys=False, separators=(',', ': '))
print 'categories loaded'

for category in categories:
	categoryname = category['*']
	members = getCategoryMembers(categoryname)
	for member in members:
		print [categoryname, member["pageid"], member["ns"], member["title"]]
		writer.writerow([categoryname, member["pageid"], member["ns"], member["title"]])
