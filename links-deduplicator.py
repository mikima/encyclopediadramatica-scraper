import requests
import urllib2, json, csv

#firce Unicode
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

links = {}
results = []


# set up the csv file
out_name = 'reciprocal-links'
ofile  = open(out_name + '.csv', "wb")
writer = csv.writer(ofile, delimiter='\t', quotechar='"')
writer.writerow(["source","target"])

#open source file
with open('links-fixed-final.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter='\t')
	# skip fist Line
	next(readCSV, None)
	#populate links
	for row in readCSV:
		if row[0] not in links:
			links[row[0]] = {}

		links[row[0]][row[1]] = True


	count = 0
	for source, targets in links.iteritems():
		count = count + 1
		try:
			for target in targets:
				if source in links[target]:
					print 'reciprocal: ',source,target
					writer.writerow([source,target])
				else:
					print 'duplicated: ',source,target
		except:
			print 'error: ',source, target
