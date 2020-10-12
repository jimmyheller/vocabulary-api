import re
from collections import Counter
from datetime import date

from bs4 import BeautifulSoup
import requests
from celery import shared_task

from .search_word import binary_search_word


@shared_task
def scrap_words_of_each_section(section_url: str, section_name: str):
	"""
	grab all posts of given section and mine all words from each single post

	description :
		1- we grab all posts in given section
		2- we grab all <p> tags from each post ( tag <p> contains english sentences )
		3- we eliminate all extra html tags and symbols from each tag <p>
		4- split all sentences into array of words
		5- validate each words
		6- translate each words and add them into our database
	"""

	today_date = str(date.today())

	# array of all posts link in this section
	posts = []

	# contain all words from each posts in this section
	final_words = []

	# grab section html
	section_page_html = requests.get(section_url).content

	# create soup obj from html
	soup_obj = BeautifulSoup(section_page_html, 'html.parser')

	# grab all post links in this section
	for post_link in soup_obj.find_all('a'):
		if re.match(r"[/[/0-9/][/0-9/][/0 -9/]+[/a-z/]+([a-z-])*(\/.*)", str(post_link.get('href'))):
			posts.append("https://www.nytimes.com" + str(post_link.get('href')))

	for post in posts:

		# if post date is equal to today date
		date_regex_pattern = "[0-9]+/[0-9]+/[0-9]+"
		if re.search(date_regex_pattern, post).group(0).replace("/", "-") == today_date:

			# grab post html
			post_page_html = requests.get(str(post)).content

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
		with open(f"{section_name}.txt", "w+") as file:
			for word in final_words:
				if len(word) > 3 and binary_search_word(word) != None:
					file.write(word.lower())
					file.write("\n")
			file.close()


def ny_times_scraper():
	"""
	new-york times scraper

	description :
		1- the website has news in about 20 section ( arts , sports , travel , .... )
		2- we grab links fro those sections
		3- we grab all posts in those sections
		4- we grab all words in each post
		5- we translate those words and add them in our database

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
		scrap_words_of_each_section.delay(section_url=section, section_name=section_name[4])
