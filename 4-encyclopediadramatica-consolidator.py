import requests
import urllib2, json, csv

#firce Unicode
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


redirects = {}
with open('target-redirects-final.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter='\t')
	next(readCSV, None)
	for row in readCSV:
			redirects[row[0]] = row

print json.dumps(redirects, sort_keys=False, separators=(',', ': '))

# set up the csv file
out_name = 'links-fixed-final'
ofile  = open(out_name + '.csv', "wb")
writer = csv.writer(ofile, delimiter='\t', quotechar='"')
writer.writerow(["source","target"])

#open source file
with open('links-from-text-fixed-aggregated.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter='\t')
	# skip fist Line
	next(readCSV, None)

	for row in readCSV:

		if row[1] in redirects:
			redirect = redirects[row[1]]
			if redirect[1] == 'True':
				writer.writerow([row[0], redirect[2]])
				print 'redirect',row[1],"=>",redirect[2]
			if redirect[1] == 'False':
				#do nothing the target page doesnt exists
				print 'no target',row[0],"=>None"
		else:
			writer.writerow(row)
			#print 'none',row
