from django.db import models
from django.urls import reverse
from django.conf import settings



class List(models.Model):
	"""Список с элементами."""
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
	

	def get_absolute_url(self):
		"""Получить абсолютный url."""
		return reverse('view_list', args=[self.id])


	@property
	def name(self):
		"""Возвращает текст первого элемента списка."""
		return self.item_set.first().text



class Item(models.Model):
	"""Элемент списка."""
	text = models.TextField(default="")
	list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)


	class Meta:
		ordering = ('id',)
		unique_together = ('list', 'text')


	def __str__(self):
		return self.text
