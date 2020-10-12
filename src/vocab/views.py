from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Vocabulary
from vocab.serializers import VocabularySerializer
from random import randint
from scraper.new_york import ny_times_scraper


class RandomWordApi(APIView):

	@staticmethod
	def get(request):
		"""
		returns one random word on each call
		"""
		# count all words
		words_count = Vocabulary.objects.all().count()

		# check if there is word in database
		if words_count:
			# random word
			word = Vocabulary.objects.all()[randint(0, words_count - 1)]

			# serializer word queryset
			serializer = VocabularySerializer(instance=word, many=False)

			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			response = {
				"detail": "error",
				"message": "There is no word."
			}
			return Response(response, status=status.HTTP_400_BAD_REQUEST)


def index(request):
	ny_times_scraper()
	return HttpResponse("ok")