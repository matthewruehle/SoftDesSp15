"""
Ordinarily I'd have put this at the front of my other code, but I figured there was no need to unnecessarily slow my program & tax the project gutenberg servers.

.txt files used elsewhere were basically from this thingie, just saved & reused more directly.

In retrospect this was probably a good move. Project Gutenberg looks to have blocked Olin's IP for the next while.

Matt Ruehle, Feb '15

"""

import os

from pattern.web import *

def grab_text_file(text_name, text_url):
	"""
	Put in a URL to a text file. This'll grab it, then save it as text_name.txt offline.
	"""
	web_file = URL(text_url).download()
	text_file = open(text_name + '.txt', 'w')
	text_file.write(web_file)
	text_file.close

def grab_gutenberg_text_file(text_name, text_url):
	"""
	grabs a text file from project gutenberg, and gets rid of the PROJECT GUTENBERG errata.
	Not the most efficient, but it gets the job done quick enough.
	"""
	web_file = URL(text_url).download()
	temporary_holding_file = open('gutenbergizer_temp.txt','w')
	temporary_holding_file.write(web_file)
	temporary_holding_file.close
	new_file_to_read = open('gutenbergizer_temp.txt','r')
	lines = new_file_to_read.readlines
	start_line = 0
	end_line = 0
	while lines[start_line].find('START OF THIS PROJECT GUTENBERG EBOOK') == -1:
		start_line += 1
	while lines[end_line].find('END OF THIS PROJECT GUTENBERG EBOOK') == -1:
		end_line += 1
	book_text_file = open(text_name + '.txt', 'w')
	book_text_file.write(lines[start_line+1:end_line])
	book_text_file.close
	os.remove('gutenbergizer_temp.txt')