from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List



class ItemModelTest(TestCase):
	"""Тест модели элемента."""


	def test_default_text(self):
		"""Тест заданного по умолчанию текста."""
		item = Item()
		self.assertEqual(item.text, '')



class ListAndItemModelsTest(TestCase):
	"""Тест модели элемента списка."""


	def test_item_is_related_to_list(self):
		"""Тест: элемент связан со списком."""
		list_ = List.objects.create()
		item = Item()
		item.list = list_
		item.save()
		self.assertIn(item, list_.item_set.all())


	def test_cannot_save_empty_list_items(self):
		"""Тест: нельзя добавлять пустые элементы списка."""
		list_ = List.objects.create()
		item = Item(list=list_, text='')
		with self.assertRaises(ValidationError):
			item.save()
			item.full_clean()


	def test_get_absolute_url(self):
		"""Тест: получен абсолютный url."""
		list_ = List.objects.create()
		self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}')


	def test_duplicate_items_are_invalid(self):
		"""Тест: повторы элементов не допустимы."""
		list_ = List.objects.create()
		Item.objects.create(list=list_, text="bla")

		with self.assertRaises(ValidationError):
			item = Item(list=list_, text='bla')
			item.full_clean()


	def test_CAN_save_same_item_to_different_lists(self):
		"""Тест: может сохранить тот же элемент в разные списки."""
		list1 = List.objects.create()
		list2 = List.objects.create()
		Item.objects.create(list=list1, text='bla')
		item = Item(list=list2, text='bla')
		item.full_clean()


	def test_list_ordering(self):
		"""Тест упорядочения списка."""
		list1 = List.objects.create()
		item1 = Item.objects.create(list=list1, text='i1')
		item2 = Item.objects.create(list=list1, text='item 2')
		item3 = Item.objects.create(list=list1, text='3')

		self.assertEqual(
			list(Item.objects.all()),
			[item1, item2, item3]
		)


	def test_string_representaion(self):
		"""Тест строкового представления."""
		item = Item(text='some text')
		self.assertEqual(str(item), 'some text')
