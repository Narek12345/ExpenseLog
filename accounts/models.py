import uuid

from django.db import models



class User(models.Model):
	"""Пользователь."""
	email = models.EmailField(primary_key=True)
	
	REQUIRED_FIELDS = []
	USERNAME_FIELD = 'email'
	is_anonymous = False
	is_authenticated = True



class Token(models.Model):
	"""Маркер."""
	email = models.EmailField()
	uid = models.CharField(default=uuid.uuid4, max_length=40)
