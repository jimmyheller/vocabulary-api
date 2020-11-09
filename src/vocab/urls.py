from django.urls import path
from .views import RandomWordApi, MultipleChoiceApi

# routing
urlpatterns = [
	path('single_word/', RandomWordApi.as_view()),
	path('multiple_choice/', MultipleChoiceApi.as_view()),
]
