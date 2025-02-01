from django import forms
from django.core.exceptions import ValidationError

from lists.models import Item


EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"



class ItemForm(forms.models.ModelForm):
	"""Форма для элемента списка."""
	
	class Meta:
		model = Item
		fields = ('text',)
		widgets = {
			'text': forms.fields.TextInput(attrs={
				'placeholder': 'Enter a to-do item',
				'class': 'form-control input-lg',
			}),
		}
		error_messages = {
			'text': {'required': EMPTY_ITEM_ERROR}
		}


	def save(self, for_list):
		self.instance.list = for_list
		return super().save()



class ExistingListItemForm(ItemForm):
	"""Форма для элемента существующего списка."""


	def __init__(self, for_list, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.instance.list = for_list
