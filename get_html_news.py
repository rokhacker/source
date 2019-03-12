#-*- coding: utf-8 -*-

import sys
import os
import urllib
import lxml
import platform
import datetime

from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
from datetime import date, timedelta



html_parser = HTMLParser()

watch_strs = ('SK', 'Hack', 'hack', 'HACK', u'해킹', u'유출', u'취약')

#watch_strs = ('test',)

# report filename
today = datetime.datetime.now().strftime("%Y-%m-%d-%H")
yesterday = str(date.today() - timedelta(1))
filename = 'news-'+today+'.txt'
is_windows = True

seperate_bar = '======================================================================================================================'
seperate_line= '[*] =================================================================================================================='



# crawling news
def conn_web(url):
	fp = urllib.urlopen(url)
	html_contents = fp.read()
	fp.close()
	return html_contents

# write report
def write_report(feed_data):
	with open(filename,'a') as fd:
		if is_windows == True:
			fd.write((feed_data+"\n").encode('euc-kr'))
		else:
			fd.write((feed_data+"\n").encode('utf-8'))


def chk_windows():
	if platform.system().find('Windows') == 0:
		return True
	else:
		reload(sys)
		sys.setdefaultencoding('utf-8')
		return False

# print & write
def print_write(title, link, content, date):
	print '[+]' + title
	write_report('[+]' + title)
	print link
	write_report(link)
	print content
	write_report(content)
	print date
	write_report(date)
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



#write_report(seperate_bar)
#write_report("Keywords :: " + ", ".join(watch_strs))
#write_report(seperate_bar)



def get_boannews():
	#web_url = "https://www.boannews.com/search/news_list.asp?search=title&find="
	url_site = "https://www.boannews.com"
	url_path = "/search/news_list.asp?search=title&find="
	
	news_collected = {}
	
	print_category(url_site)
	print '[*] Searching',
	for watch_str in watch_strs:
		#global news_collected
		watch_str = urllib.quote(watch_str.encode('utf-8'))
		html_contents = conn_web(url_site + url_path + watch_str)

		soup = BeautifulSoup(html_contents, 'lxml')

		news_lists = soup.find_all('div', class_='news_list')

		print '.',
		for news_list in news_lists:
			news_anchor = news_list.find_all('a')
			news_link = news_anchor[0].get('href')
			news_link = url_site + html_parser.unescape(news_link)
			#print news_link
			
			news_title = news_list.find('span', class_='news_txt')
			news_title = html_parser.unescape(news_title.text)
			news_title = news_title.replace(u'\xa0',' ')
			#print news_title

			news_contents = news_anchor[1].string
			news_contents = html_parser.unescape(news_contents)
			news_contents = news_contents.replace(u'\xa0',' ')
			news_contents = news_contents.replace(u'\u2027',' ')
			news_contents = news_contents.replace(u'\u2013',' ')
			news_contents = news_contents.replace(u'\x0a',' ')
			#print news_contents
			
			news_date = news_list.find('span', class_='news_writer')
			news_date = html_parser.unescape(news_date.text.split(" | ")[1])
			
			# from previous month
			#if float(news_date[:7]) >= (float(today[:7].replace('-','.'))-0.001):
			# only this month
			news_date_merge = (news_date[:7] + news_date[8:10]).replace('-','.')
			today_date_merge = (today[:7]+today[8:10]).replace('-','.')
			yesterday_date_merge = (yesterday[:7]+yesterday[8:10]).replace('-','.')

			#if news_date[:7] == today[:7].replace('-','.'):
			if (news_date_merge == today_date_merge) or (news_date_merge == yesterday_date_merge):
				#print news_date_merge + " :: " + today_date_merge + " :: " + yesterday_date_merge
				news_collected[news_link]=[news_title, news_contents, news_date]

			

	print '\n'
	for news_link in news_collected:
		print_write(news_collected[news_link][0], news_link, news_collected[news_link][1], news_collected[news_link][2])


def get_etnews():
	#web_url = "http://search.etnews.com/etnews/search.php?category=CATEGORY1&kwd=hack&pageNum=1&pageSize=3&reSrchFlag=false&sort=1&startDate=&endDate=&sitegubun=&jisikgubun=&preKwd%5B0%5D=hack"
	url_site = "http://search.etnews.com"
	url_path = "/etnews/search.php?category=CATEGORY1&pageNum=1&pageSize=&reSrchFlag=false&sort=1&startDate=&endDate=&sitegubun=&jisikgubun=&kwd="
	
	news_collected = {}
	
	print_category(url_site)
	print '[*] Searching',
	for watch_str in watch_strs:
		#global news_collected
		watch_str = urllib.quote(watch_str.encode('utf-8'))
		html_contents = conn_web(url_site + url_path + watch_str)

		soup = BeautifulSoup(html_contents, 'lxml')

		news_lists = soup.find_all('dl', class_='clearfix')

		print '.',
		for news_list in news_lists:
			
			news_anchor = news_list.find_all('a')
			#print news_anchor
			news_link = news_anchor[0].get('href')
			news_link = html_parser.unescape(news_link)
			#print news_link
			

			news_title = news_anchor[0].text
			news_title = news_title.replace(u'\xa0',' ')
			news_title = news_title.replace(u'\u2027',' ')
			#print news_title

			news_contents = news_list.find('dd', class_='summury')
			news_contents = html_parser.unescape(news_contents.text)
			news_contents = news_contents.replace(u'\xa0',' ')
			news_contents = news_contents.replace(u'\u2027',' ')
			news_contents = news_contents.replace(u'\u2013',' ')
			news_contents = news_contents.replace(u'\x0a',' ')
			#print news_contents
			
			news_date = news_list.find('dd', class_='date')
			news_date = news_date.text
			#print news_date.encode("euc-kr")

			# match today and yesterday
			news_date_merge = (news_date[:4] + "." + news_date[6:8]).replace('-','.')
			today_date_merge = (today[:7]+today[8:10]).replace('-','.')
			yesterday_date_merge = (yesterday[:7]+yesterday[8:10]).replace('-','.')
			#print news_date_merge + " :: " + today_date_merge + " :: " + yesterday_date_merge
			if (news_date_merge == today_date_merge) or (news_date_merge == yesterday_date_merge):
				if news_title.find(u"ET투자뉴스") >= 0:
					continue
				news_collected[news_link]=[news_title, news_contents, news_date]
			

	print '\n'
	for news_link in news_collected:
		print_write(news_collected[news_link][0], news_link, news_collected[news_link][1], news_collected[news_link][2])


def sendmail_news():
	if is_windows == False:
		os.system('/bin/mutt -s "' + today + ' News" admin@admin.org < ' + filename)
		#os.system('/bin/mutt -s "' + today + ' News" admin@admin.org -cadmin@admin.org -a attach.zip < ' + filename)
	else:
		pass



is_windows = chk_windows()

get_boannews()
get_etnews()
sendmail_news()
