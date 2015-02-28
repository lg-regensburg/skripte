#!/usr/bin/env python
# -*- coding: utf-8 -*-

# to do: 
# add <p align="center"> for centering images (and remove class=...
# add class="highlight indent" in comments on top

from bs4 import BeautifulSoup
import codecs
import re, os, shutil

def convert_to_lca_style(filename):
	outfile = open(filename + '.php', mode='w', encoding='utf-8')
	soup = BeautifulSoup(open(filename + '.htm', encoding='utf-8'))
	soup.prettify()

	# tags style und head entfernen
	soup.style.decompose()
	soup.head.decompose()

	# b, div, span entfernen (Inhalt bleibt)
	bs = soup.find_all("b")
	for tag in bs:
		soup.b.unwrap()
	divs = soup.find_all("div")
	for tag in divs:
		soup.div.unwrap()
	spans = soup.find_all("span")
	for tag in spans:
		soup.span.unwrap()

	# p: attribute etc. bereinigen	
	paragraphs = soup.find_all("p")
	replacements = {'\n':' ', '\r':' ', 'muß':'muss', 'müßte':'müsste', 'usschuß':'usschuss', 'eschluß':'eschluss', 'rozeß':'rozess', 'ißerfolg':'isserfolg'}
	last_paragraph = ''
	for paragraph in paragraphs:
		del paragraph['class']
		del paragraph['style']
		str = paragraph.get_text()
		if paragraph.find("img") is None:
			for src, target in replacements.items():
				str = str.replace(src, target)
			# str = re.sub("\ {2,999}", 'HERE', str)
			paragraph.string = str
		if (paragraph.string is None or paragraph.string.strip() == '') and paragraph.find("img") is None:
			paragraph.extract()
		
	# Heading
	heading = soup.find("p")
	heading_text = heading.get_text()
	heading.string = ''
	heading.append(soup.new_tag("h2"))
	heading.h2.string = heading_text
	heading.unwrap()

	# Sub-Headings
	paragraphs = soup.find_all("p")
	last_paragraph = ''
	for paragraph in paragraphs:	
		last_paragraph = paragraph
		if len(paragraph.get_text()) < 140 and paragraph.find("img") is None:
			text = paragraph.get_text()
			paragraph.string = ''
			paragraph.append(soup.new_tag("strong"))
			paragraph.strong.string = text

	# Last paragraph
	if len(last_paragraph.get_text()) <140:
		last_paragraph.string = last_paragraph.strong.get_text()
		last_paragraph['style'] = 'font-size:0.8em'
	else:
		source = soup.new_tag("p", style='font-size:0.8em')
		last_paragraph.insert_after(source)
		source.string = 'QUELLENANGABEN'

	# images: attributes
	images = soup.find_all("img")
	for image in images:
		del image['alt']
		del image['height']
		del image['id']
		image['width'] = '500px'
		image['class'] = 'float_left'
		image['title'] = 'TODO'
		image['src'] = '../photos/ADDHERE.jpg'

	# html und body entfernen (Inhalt bleibt)
	soup.html.unwrap()
	soup.body.unwrap()

	outfile.write("<?php $title = \"" + heading_text + "\"; ?>\n <?php require(\"../_header.dir1.inc.php\"); ?>\n\n")
	outfile.write(soup.prettify())
	outfile.write("\n\n<?php require(\"../_footer.dir1.inc.php\"); ?>")
	outfile.close()
	

	# non-beautiful soup editing

	# temporary file
	shutil.copy(os.getcwd() + '\\' + filename + ".php", os.getcwd() + '\\' + filename + ".php.tmp")
	# remove newlines
	withoutNewLines = open(filename + ".php", encoding='utf-8').read().replace('\n', '')
	outfile = open(filename + ".php.tmp", 'w', encoding='utf-8')
	outfile.write(withoutNewLines)
	outfile.close()

	infile = open(filename + ".php.tmp", encoding='utf-8')
	outfile2 = open(filename + ".php", 'w', encoding='utf-8')

	replacements = {'</p>':'</p>\n\n', '?>':'?>\n\n', '</h2>':'</h2>\n\n', ' <':'<', '> ':'>'}

	for line in infile:
		for src, target in replacements.items():
			line = line.replace(src, target)
		line = line.replace(' <', '<')
		line = line.replace('> ', '>')
		outfile2.write(line)
	infile.close()
	outfile2.close()

	os.remove(filename + ".php.tmp")

	return
	
	
	

input('Export word-file as website (filtered) and convert to utf-8. Press Enter to continue.')

for file in os.listdir(os.getcwd()):
	if os.path.splitext(file)[1] == ".htm":
		filename = os.path.splitext(file)[0]
		convert_to_lca_style(filename)

input('Rename file, add location/author/date, check img-titles, links, sources, typos etc.. Press Enter to close.')
