import re
from collections import Counter
from datetime import date

from bs4 import BeautifulSoup
import requests
from celery import shared_task

from .search_word import binary_search_word
from vocab.translator import translator
from vocab.models import Vocabulary


@shared_task
def scrap_words_of_each_post(post_url: str, section_name: str):
	"""
	grab all words of given link

	description :
		1- grab all <p> tags from each post ( tag <p> contains english sentences )
		2- eliminate all extra html tags and symbols from each <p> tags
		3- split all sentences into array of words
		4- validate each words
		5- translate each words and add them into our database
	"""

	# contain all words from each posts in this section
	final_words = []

	# grab post html
	post_page_html = requests.get(str(post_url)).content

	# create soup obj from html
	soup_obj = BeautifulSoup(post_page_html, 'html.parser')

	# grab all tag <p> contain sentences in post link
	context = soup_obj.find_all('p')

	# process through all <p> tags
	for paragraph in range(len(context)):
		# convert each tag <p> to string
		context[paragraph] = str(context[paragraph])

		# eliminate all extra html tags and symbols
		context[paragraph] = re.sub('<.*?>', '', context[paragraph])
		context[paragraph] = re.sub('[0-9?"“”)’(—,\\.:;©"]+', '', context[paragraph])

		# convert paragraph into list ( divide to single words )
		context[paragraph] = list(context[paragraph].split(" "))

		final_words += context[paragraph]

	# eliminate repetitive words
	final_words = Counter(list(final_words))
	final_words = list(final_words)

	if len(final_words) > 2:
		for word in final_words:
			if len(word) > 3 and binary_search_word(word) and word.islower():
				try:
					translation = list(translator(word=[word, ], source="en", destination="fa"))
					action = Vocabulary()
					action.word = translation[0][0]
					action.meaning = translation[0][1]
					action.tag = section_name
					action.save()
				except:
					continue


def ny_times_scraper():
	"""
	new-york times scraper

	description :
		1- the website has news in about 20 section ( arts , sports , travel , .... )
		2- grab links fro those sections
		3- grab all posts in those sections
		4- grab all words in each post
		5- translate those words and add them in our database

	"""
	# grab 'nytimes' site html
	main_page_html = requests.get("https://www.nytimes.com/").content

	# create soup obj from html
	soup_obj = BeautifulSoup(main_page_html, 'html.parser')

	# array of section links
	sections = []

	# find all tag <a> contain sections in html
	for section_link in soup_obj.find_all('a'):
		if re.match(r"https:[//]+[a-z]*.[a-z]*.com[/]section[/][a-z]*", str(section_link.get('href'))):
			sections.append(section_link.get('href'))

	# grab all post in sections
	for section in sections:

		section_name = section.split("/")

		# contain all posts links
		posts = []

		section_page_html = requests.get(section).content
		soup_obj = BeautifulSoup(section_page_html, 'html.parser')

		# grab all post links in this section
		for post_link in soup_obj.find_all('a'):
			if re.match(r"[/[/0-9/][/0-9/][/0 -9/]+[/a-z/]+([a-z-])*(\/.*)", str(post_link.get('href'))):
				posts.append("https://www.nytimes.com" + str(post_link.get('href')))

		today_date = str(date.today())
		date_regex_pattern = "[0-9]+/[0-9]+/[0-9]+"

		for post in posts:
			if re.search(date_regex_pattern, post).group(0).replace("/", "-") == today_date:
				scrap_words_of_each_post.delay(post_url=post, section_name=section_name[4])
