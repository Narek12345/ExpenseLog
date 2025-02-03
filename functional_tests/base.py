from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

import os
import time


MAX_WAIT = 5



class FunctionalTest(StaticLiveServerTestCase):
	"""Функциональный тест."""


	def setUp(self):
		"""Установка."""
		self.browser = webdriver.Chrome()
		staging_server = os.environ.get('STAGING_SERVER')
		if staging_server:
			self.live_server_url = 'http://' + staging_server


	def tearDown(self):
		"""Демонтаж."""
		self.browser.quit()


	def wait_for_row_in_list_table(self, row_text):
		"""Ожидает строку в таблице списка."""
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element(By.ID, 'id_list_table')
				rows = table.find_elements(By.TAG_NAME, 'tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)


	def wait_for(self, fn):
		"""Добавляет ожидание."""
		start_time = time.time()
		while True:
			try:
				return fn()
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)


	def get_item_input_box(self):
		"""Получить поле ввода для элемента."""
		return self.browser.find_element(By.ID, 'id_text')


	def wait_to_be_logged_in(self, email):
		"""Ожидать входа в систему."""
		self.wait_for(
			lambda:
				self.browser.find_element(By.LINK_TEXT, 'Log out')
		)
		navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
		self.assertIn(email, navbar.text)
