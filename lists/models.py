from django.db import models


class Item(models.Model):
	"""Элемент списка."""
	text = models.TextField(default="")
