#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import pyperclip

http = httplib2.Http()

status, response = http.request('http://la-coaching-academy.de', "GET")
response = response.decode('iso-8859-1')
soup = BeautifulSoup(response)

for div in soup.select('div#col3_content'):
	# outfile.write(div.h2.get_text() + '\n\n')
	new_article = BeautifulSoup('')
	i = 0
	for p in div.find_all('p'):
		if i<2:
			new_article.append(p)
			i = i+1

for img in new_article.find_all('img'):
	img['class'] = 'caption'
	img['width'] = '200px'
	source = img['src']
	img['src'] = 'http://la-coaching-academy.de/' + source[3:]
	del img['id']
	del img['border']
	del img['height']

for link in new_article.find_all('a'):
	ref = link['href']
	link['href'] = 'http://la-coaching-academy.de/' + ref
	link['target'] = '_blank'

var = new_article.prettify('utf-8')
pyperclip.copy(var)

print("Copied to clipboard - paste to new joomla-article as html")

