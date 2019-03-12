#-*- coding: utf-8 -*-

import feedparser
import argparse
import datetime

##############################################################################################################
###########################################    Global Variables    ###########################################
##############################################################################################################
# Full link : http://www.etnews.com/rss/
urls_etnews = (
	"http://www.boannews.com/media/news_rss.xml",	# full news
	"http://rss.etnews.com/Section901.xml",			# today news
	"http://rss.etnews.com/Section902.xml",			#
	"http://rss.etnews.com/03.xml",					# Communication/broadcast
	"http://rss.etnews.com/04045.xml"				# Security
)

# Full link : https://www.boannews.com/custom/news_rss.asp
urls_boannews = (
	"http://www.boannews.com/media/news_rss.xml",			# full news
	"http://www.boannews.com/media/news_rss.xml?kind=1",	# accident
	"http://www.boannews.com/media/news_rss.xml?kind=2",	# Government
	"http://www.boannews.com/media/news_rss.xml?skind=5",	# Sokbo
	"http://www.boannews.com/media/news_rss.xml?skind=2",	# Security Column
	"http://www.boannews.com/media/news_rss.xml?skind=6"	# Security Policy
)

# Full link : http://news.google.co.kr/news?pz=1&cf=all&ned=kr&hl=ko&output=rss
urls_googlenews = ( 'https://news.google.com/rss?pz=1&cf=all&hl=ko&gl=KR&ceid=KR:ko' )	# full news


# catch string list
watch_strs = ('SK', 'SKT', 'Hack', 'hack', 'HACK', u'해킹', u'보안', u'유출')


# Deduplication
news_results = {}
news_dicts = {}
news_lists = []

# report filename
today = datetime.datetime.today().strftime("%Y-%m-%d-%H")
filename = 'rss_report-'+today+'.txt'

#seperate_bar = '======================================================================================================================'
seperate_bar = '####################################################################################################################'
seperate_line= '[*] ================================================================================================================'


##############################################################################################################
###############################################    Functions    ##############################################
##############################################################################################################
# get etnews, boannews
def get_rss_et_boan_news(url):
	feed_data = feedparser.parse(url)
	#print type(feed_data)
	#print '########################################  ' + feed_data.feed["title"] + '  ########################################'
	#write_report('########################################  ' + feed_data.feed["title"] + '  ########################################')

	for news in feed_data.entries:
		for watch_str in watch_strs:
			if news.title.find(watch_str) >= 0:
				news.link.strip()
				news_dicts[news.link]=[news.title,news.description, feed_data.feed["title"]]

	return news_dicts
	
				
# write report
def write_report(feed_data):
	with open(filename, 'a') as fd:
		fd.write((feed_data+"\n").encode('euc-kr'))

# print & write
def print_write(title, link, content):
	print '[+]' + title
	write_report('[+]' + title)
	print link
	write_report(link)
	print content
	write_report(content)
	print '\n'
	write_report('\n')

# print category
def print_category(data):
	print '########################################  ' + data + '  ########################################'
	write_report('########################################  ' + data + '  ########################################')
	


##############################################################################################################
#############################################    Do  Execution    ############################################
##############################################################################################################
# clear report
with open(filename, 'w') as fd:
	fd.write('')



# Get etnews
print_category(u'전자뉴스 (etnews)')
for url in urls_etnews:
	temp_results = get_rss_et_boan_news(url)
	news_results.update(temp_results)

for link in news_results.keys():
	print_write(news_results[link][0], link, news_results[link][1])

# clear data
news_results = {}
news_dicts = {}
news_lists = []

# Get boannews
print_category(u'보안뉴스 (boannews)')
for url in urls_boannews:
	temp_results = get_rss_et_boan_news(url)
	news_results.update(temp_results)

for link in news_results.keys():
	print_write(news_results[link][0], link, news_results[link][1])
