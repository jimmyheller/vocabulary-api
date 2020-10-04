from rest_framework import serializers
from .models import Vocabulary


class VocabularySerializer(serializers.ModelSerializer):
	""" Vocabulary model serialier """
	class Meta:
		model = Vocabulary
		fields = "__all__"
