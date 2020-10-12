from bs4 import BeautifulSoup
import requests
import re
from .search_word import binary_search_word
from collections import Counter
from celery import shared_task
from datetime import date


@shared_task
def scrap_word_of_each_section(section_url: str, section_name: str):
	today = str(date.today())
	posts = []
	final_words = []

	html_main_section_page = requests.get(section_url).content
	soup = BeautifulSoup(html_main_section_page, 'html.parser')
	for post_link in soup.find_all('a'):
		if re.match(r"[/[/0-9/][/0-9/][/0 -9/]+[/a-z/]+([a-z-])*(\/.*)", str(post_link.get('href'))):
			posts.append("https://www.nytimes.com" + str(post_link.get('href')))

	for post in posts:
		r = "[0-9]+/[0-9]+/[0-9]+"
		if re.search(r, post).group(0).replace("/", "-") == today:

			html_main_page = requests.get(str(post)).content
			soup = BeautifulSoup(html_main_page, 'html.parser')

			context = soup.find_all('p')
			for paragraph in range(len(context)):
				context[paragraph] = str(context[paragraph])
				context[paragraph] = re.sub('<.*?>', '', context[paragraph])
				context[paragraph] = re.sub('[0-9?"“”)’(—,\\.:;©"]+', '', context[paragraph])
				context[paragraph] = list(context[paragraph].split(" "))
				final_words += context[paragraph]

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
	html_main_page = requests.get("https://www.nytimes.com/").content
	soup = BeautifulSoup(html_main_page, 'html.parser')

	sections = []
	for section_link in soup.find_all('a'):
		if re.match(r"https:[//]+[a-z]*.[a-z]*.com[/]section[/][a-z]*", str(section_link.get('href'))):
			sections.append(section_link.get('href'))

	for section in sections:
		section_name = section.split("/")
		scrap_word_of_each_section.delay(section_url=section, section_name=section_name[4])
