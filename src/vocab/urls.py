from django.urls import path
from .views import RandomWordApi

# routing
urlpatterns = [
	path('', RandomWordApi.as_view()),
]
