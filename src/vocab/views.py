import random

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Vocabulary
from vocab.serializers import VocabularySerializer
from random import randint
from scraper.new_york import ny_times_scraper

from random import randint



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

          
class MultipleChoiceApi(APIView):

    @staticmethod
    def get(request):
        """
            returns one random word with multiple choice
        """
        count = Vocabulary.objects.count()
        random_word = []

        for i in range(4):
            random_word.append(Vocabulary.objects.all()[randint(0, count - i)])

        question = random_word[randint(0, 3)]

        random.shuffle(random_word)

        response = {
            'question_word': question.word,
            'choice1': random_word[0].meaning,
            'choice2': random_word[1].meaning,
            'choice3': random_word[2].meaning,
            'choice4': random_word[3].meaning,
        }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)

def index(request):
	ny_times_scraper()
	return HttpResponse("ok")
