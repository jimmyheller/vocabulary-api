from django.db import models


# Create your models here.
class Vocabulary(models.Model):
	word = models.CharField(max_length=50, unique=True)
	meaning = models.CharField(max_length=50, blank=True, null=True)
	tag = models.CharField(max_length=50, blank=True, null=True)

	def __str__(self):
		return self.word
