from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest



class ItemValidationTest(FunctionalTest):
	"""Тест валидации элемента списка."""


	def get_error_element(self):
		"""Получить элемент с ошибкой."""
		return self.browser.find_element(By.CSS_SELECTOR, '.has-error')


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
		self.add_list_item('Buy milk')
		self.wait_for(
			lambda:
				self.browser.find_elements(By.CSS_SELECTOR, '#id_text:valid')
		)

		# И она может отправить его успешно.
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
		self.add_list_item('Make tea')
		self.wait_for(
			lambda:
				self.browser.find_elements(By.CSS_SELECTOR, '#id_text:valid')
		)

		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for_row_in_list_table('2: Make tea')


	def test_cannot_add_duplicate_items(self):
		"""Тест: нельзя добавлять повторяющиеся элементы."""
		# Эдит открывает домашнюю страницу и начинает новый список.
		self.browser.get(self.live_server_url)
		self.add_list_item('Buy wellies')
		self.wait_for_row_in_list_table('1: Buy wellies')

		# Она случайно пытается ввести повторяющийся элемент.
		self.add_list_item('Buy wellies')

		# Она видит полезное сообщение об ошибке.
		self.wait_for(
			lambda:
				self.assertEqual(
					self.get_error_element().text,
					"You've already got this in your list"
				)
		)


	def test_error_messages_are_cleared_on_input(self):
		"""Тест: сообщения об ошибках очищаются при вводе."""
		# Эдит начинает список и вызывает ошибку валидации:
		self.browser.get(self.live_server_url)
		self.add_list_item('Banter too thick')
		self.wait_for_row_in_list_table('1: Banter too thick')
		self.add_list_item('Banter too thick')

		self.wait_for(
			lambda: 
				self.assertTrue(
					self.get_error_element().is_displayed()
				)
		)

		# Она начинает набирать в поле ввода, чтобы очистить ошибку.
		self.get_item_input_box().send_keys('a')

		# Она довольна от того, что сообщение об ошибке исчезает.
		self.wait_for(
			lambda:
				self.assertFalse(
					self.get_error_element().is_displayed()
				)
		)
