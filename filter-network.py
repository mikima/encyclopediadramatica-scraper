import requests
import urllib2, json, csv

#firce Unicode
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# filters a network starting from a lsit of pages

pages = {}
#open source file
with open('data/encyclopedia-dramatica-redirects-more-than-10.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter='\t')
	# skip fist Line
	next(readCSV, None)
	#populate links
	for row in readCSV:
		pages[row[2]] = True

# set up the csv file
writer = csv.writer(open('filtered-network.csv', "wb"), delimiter='\t', quotechar='"')
writer.writerow(["source","target"])

#open the network file and filter Links
with open('data/reciprocal-links.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter='\t')
	# skip fist Line
	next(readCSV, None)
	#populate links
	for row in readCSV:
		if (row[0] in pages) and (row[1] in pages):
			#write in a new file
			writer.writerow(row)
