from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest



class ItemValidationTest(FunctionalTest):
	"""Тест валидации элемента списка."""


	def test_cannot_add_empty_list_items(self):
		"""Тест: нельзя добавлять пустые элементы списка."""
		# Эдит открывает домашнюю страницу и случайны пытается отправить пустой элемент списка. Она нажимает Enter на пустом поле ввода.
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys(Keys.ENTER)

		# Браузер перехватывает запрос и не загружает страницу со списком.
		self.wait_for(
			lambda:
				self.browser.find_elements(By.CSS_SELECTOR, '#id_text:invalid')
		)

		# Эдит начинает набирать текст нового элемента и ошибка исчезает.
		self.get_item_input_box().send_keys('Buy milk')
		self.wait_for(
			lambda:
				self.browser.find_elements(By.CSS_SELECTOR, '#id_text:valid')
		)

		# И она может отправить его успешно.
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		# Как ни странно, Эдит решает отправить второй пустой элемент списка.
		self.get_item_input_box().send_keys(Keys.ENTER)

		# И снова браузер не подчиняется.
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for(
			lambda:
				self.browser.find_elements(By.CSS_SELECTOR, '#id_text:invalid')
		)

		# И она может исправиться, заполнив поле текстом.
		self.get_item_input_box().send_keys('Make tea')
		self.wait_for(
			lambda:
				self.browser.find_elements(By.CSS_SELECTOR, '#id_text:valid')
		)

		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for_row_in_list_table('2: Make tea')
