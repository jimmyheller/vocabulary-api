from googletrans import Translator


def translator(word: list, source: str, destination: str) -> tuple:
	"""
	translate every word between languages

	:param word: the word needed to translate
	:param source: the word origin language
	:param destination: the destination that word must translate to
	:return string: meaning of word
	"""

	# available languages
	LANGUAGES = {
		'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian', 'az': 'azerbaijani',
		'eu': 'basque', 'be': 'belarusian',
		'bn': 'bengali', 'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa',
		'zh-cn': 'chinese (simplified)', 'zh-tw': 'chinese (traditional)',
		'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish', 'nl': 'dutch', 'en': 'english',
		'eo': 'esperanto', 'et': 'estonian',
		'tl': 'filipino', 'fi': 'finnish', 'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian',
		'de': 'german', 'el': 'greek',
		'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew', 'he': 'hebrew',
		'hi': 'hindi', 'hmn': 'hmong',
		'hu': 'hungarian', 'is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'it': 'italian',
		'ja': 'japanese', 'jw': 'javanese',
		'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz',
		'lo': 'lao', 'la': 'latin',
		'lv': 'latvian', 'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay',
		'ml': 'malayalam', 'mt': 'maltese',
		'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian', 'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian',
		'or': 'odia', 'ps': 'pashto',
		'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian',
		'sm': 'samoan', 'gd': 'scots gaelic', 'sr': 'serbian',
		'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian',
		'so': 'somali', 'es': 'spanish',
		'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai',
		'tr': 'turkish',
		'uk': 'ukrainian', 'ur': 'urdu', 'ug': 'uyghur', 'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh',
		'xh': 'xhosa', 'yi': 'yiddish',
		'yo': 'yoruba', 'zu': 'zulu',
	}

	if not word:  # if word not entered
		raise ValueError("Word not provided.")

	if not LANGUAGES.get(source) or not LANGUAGES.get(destination):  # if source and destination not valid
		raise ValueError("Enter correct format.")

	# translator obj
	translator_obj = Translator()
	translations = translator_obj.translate(word, src=source, dest=destination)

	for word in translations:
		yield (word.origin, word.text)
