# This script allows to crawl information and repositories from GitHub using the GitHub REST API (https://developer.github.com/v3/search/).
#
# Given a query, the script downloads for each repository returned by the query its ZIP file.
# In addition, it also generates a CSV file containing the list of repositories queried.
# For each query, GitHub returns a json file which is processed by this script to get information about repositories.
#
# The GitHub API limits the queries to get 100 elements per page and up to 1,000 elements in total.
# To get more than 1,000 elements, the main query should be splitted in multiple subqueries using different time windows through the constant SUBQUERIES (it is a list of subqueries).
#
# As example, constant values are set to get the repositories on GitHub of the user 'rsain'.


#############
# Libraries #
#############

import wget
import time
import simplejson
import csv
import pycurl
import math
from StringIO import StringIO
import calendar


#############
# Constants #
#############

URL = "https://api.github.com/search/repositories?q=" #The basic URL to use the GitHub API
QUERY = "leetcode" #The personalized query (for instance, to get repositories from user 'rsain')
#https://api.github.com/search/repositories?q=leetcode+created%3A2015-04-30..2016-07-04
#https://api.github.com/search/repositories?q=leetcode+created%3A2013-01-01..2013-07-04
#SUBQUERIES = ["+created%3A<%3D2013-12-30","+created%3A>%3D2014-01-01"] #Different subqueries if you need to collect more than 1000 elements
PARAMETERS = "&per_page=100" #Additional parameters for the query (by default 100 items per page)
DELAY_BETWEEN_QUERYS = 5 #The time to wait between different queries to GitHub (to avoid be banned)
OUTPUT_FOLDER = "./" #Folder where ZIP files will be stored
OUTPUT_CSV_FILE = "./repositories.csv" #Path to the CSV file generated as output


#############
# Functions #
#############

def getUrl (url) :
	''' Given a URL it returns its body '''
	buffer = StringIO()
	c = pycurl.Curl()
	c.setopt(c.URL, url)
	c.setopt(c.WRITEDATA, buffer)
	c.perform()
	c.close()
	body = buffer.getvalue()

	return body


########
# MAIN #
########

#To save the number of repositories processed
countOfRepositories = 0

#Output CSV file which will contain information about repositories
csvfile = open(OUTPUT_CSV_FILE, 'wb')
repositories = csv.writer(csvfile, delimiter=',')

from datetime import datetime, timedelta
from collections import OrderedDict
dates = ["2013-01-01", "2020-12-01"]
start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
dateRange = OrderedDict(((start + timedelta(_)).strftime(r"%Y-%m"), None) for _ in xrange((end - start).days)).keys()


#Run queries to get information in json format and download ZIP file for each repository
for year in range(2013, 2020):
	for month in range(1,12):

		curMonth = str(year)+"-"+format(month,'02d') 
		lastDay = format(calendar.monthrange(year,month)[1],'02d') 

		SUB_QUERY = "+created%3A"+curMonth+"-01.."+curMonth+"-"+lastDay
		#Obtain the number of pages for the current subquery (by default each page contains 100 items)
		url = URL + QUERY + SUB_QUERY + PARAMETERS			
		print "Processing "+url
		dataRead = simplejson.loads(getUrl(url))	

		if(dataRead.get('total_count') is None):
			print dataRead

		numberOfPages = int(math.ceil(dataRead.get('total_count')/100.0))	

		

		#Results are in different pages
		for currentPage in range(1, numberOfPages+1):
			url = URL + QUERY + SUB_QUERY + PARAMETERS + "&page=" + str(currentPage) 
			print "SUB Processing "+url + " ...out of "+str(numberOfPages)		
			dataRead = simplejson.loads(getUrl(url))
			
			#Iteration over all the repositories in the current json content page
			for item in dataRead['items']:
				#Obtain user and repository names
				user = item['owner']['login']
				repository = item['name']

				#Update repositories counter
				countOfRepositories = countOfRepositories + 1

				if item['license']  is not None:
					if item['license']['key'] is not None:								
						#Download the zip file of the current project				
						print ("'%s' from user '%s' ... '%s'" %(repository,user,item['license']['key'] ))
						url = item['clone_url']
						fileToDownload = url[0:len(url)-4] + "/archive/master.zip"
						fileName = item['full_name'].replace("/","_") + ".zip"
						#wget.download(fileToDownload, out=OUTPUT_FOLDER + fileName)
										
						repositories.writerow([user, repository, url, fileToDownload, item['license']['key']])

			#A delay between different subqueries
			time.sleep(DELAY_BETWEEN_QUERYS)

print "DONE! " + str(countOfRepositories) + " repositories have been processed."
csvfile.close()


 