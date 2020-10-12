from django.conf import settings
import os


def binary_search_word(word):
	word = str(word).lower()
	first_char = word[0]
	reference_word = str(settings.BASE_DIR) + f"/scraper/reference_words/{first_char}.txt"
	try:
		with open(str(reference_word), "r") as file:
			data = [line.strip() for line in file]
	except:
		return None
	low = 0
	high = len(data) - 1
	while low <= high:
		mid = int((low + high) / 2)
		guess = data[mid]
		if guess == word:
			return mid
		if guess > word:
			high = mid - 1
		else:
			low = mid + 1
	return None
