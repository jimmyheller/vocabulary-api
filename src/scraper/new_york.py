from bs4 import BeautifulSoup
import requests
import re
from .search_word import binary_search_word
from collections import Counter
from celery import shared_task
from datetime import date


@shared_task
def scrap_word_of_each_section(section_url: str, section_name: str):
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
	today = str(date.today())

	# link for all posts in this section
	posts = []

	# contain all words from each posts in this section
	final_words = []

	# grab section html
	html_main_section_page = requests.get(section_url).content

	# create soup obj from html
	soup = BeautifulSoup(html_main_section_page, 'html.parser')

	# grab all post links in this section
	for post_link in soup.find_all('a'):
		if re.match(r"[/[/0-9/][/0-9/][/0 -9/]+[/a-z/]+([a-z-])*(\/.*)", str(post_link.get('href'))):
			posts.append("https://www.nytimes.com" + str(post_link.get('href')))

	for post in posts:
		r = "[0-9]+/[0-9]+/[0-9]+"

		# if post date is equal to today date
		if re.search(r, post).group(0).replace("/", "-") == today:

			# grab post html
			html_main_page = requests.get(str(post)).content

			# create soup obj from html
			soup = BeautifulSoup(html_main_page, 'html.parser')

			# grab all tag <p> contain sentences in post link
			context = soup.find_all('p')

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
	html_main_page = requests.get("https://www.nytimes.com/").content

	# create soup obj from html
	soup = BeautifulSoup(html_main_page, 'html.parser')

	sections = []
	# find all tag <a> contain sections in html
	for section_link in soup.find_all('a'):
		if re.match(r"https:[//]+[a-z]*.[a-z]*.com[/]section[/][a-z]*", str(section_link.get('href'))):
			sections.append(section_link.get('href'))

	# grab all post in sections
	for section in sections:
		section_name = section.split("/")
		scrap_word_of_each_section.delay(section_url=section, section_name=section_name[4])
