from django.conf import settings


def binary_search_word(word):
	"""
	find given word in our reference data using binary search techniue
	"""
	word = str(word).lower()
	first_char = word[0]
	reference_word = str(settings.BASE_DIR) + f"/scraper/reference_words/{first_char}.txt"
	try:
		with open(str(reference_word), "r") as file:
			words_array = [line.strip() for line in file]
	except:
		return None

	low_bound = 0
	high_bound = len(words_array) - 1
	while low_bound <= high_bound:
		middle_index = int((low_bound + high_bound) / 2)
		guess = words_array[middle_index]
		if guess == word:
			return middle_index
		if guess > word:
			high_bound = middle_index - 1
		else:
			low_bound = middle_index + 1
	return None
