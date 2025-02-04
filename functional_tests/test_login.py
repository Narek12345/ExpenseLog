import os
import re
import time
import poplib

from django.core import mail

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


TEST_EMAIL = 'edith@example.com'
SUBJECT = 'Your login link for SuperLists'



class LoginTest(FunctionalTest):
	"""Тест регистрации в системе."""


	def test_can_get_email_link_to_log_in(self):
		"""Тест: можно получить ссылку по почте для регистрации."""
		# Эдит заходит на офигительный сайт суперсписков и впервые замечает раздел "войти" в навигационной панели.
		# Он говорит ей ввести свой адрес электронной почты, что она и делает.
		self.browser.get(self.live_server_url)
		self.browser.find_element(By.NAME, 'email').send_keys(TEST_EMAIL)
		self.browser.find_element(By.NAME, 'email').send_keys(Keys.ENTER)

		# Появляется сообщение, которое говорит, что ей на почту было выслано электронное письмо.
		self.wait_for(
			lambda:
				self.assertIn(
					'Check your email',
					self.browser.find_element(By.TAG_NAME, 'body').text
				)
		)

		# Эдит проверяет свою почту и находит сообщение.
		email = mail.outbox[0]
		self.assertIn(TEST_EMAIL, email.to)
		self.assertEqual(email.subject, SUBJECT)

		# Оно содержит ссылку на url-адрес.
		self.assertIn('Use this link to log in', email.body)
		url_search = re.search(r'http://.+/.+$', email.body)

		if not url_search:
			self.fail(f'Could not find url in email body:\n{email.body}')

		url = url_search.group(0)
		self.assertIn(self.live_server_url, url)

		# Эдит нажимает на ссылку.
		self.browser.get(url)

		# Она зарегестрировалась в системе.
		self.wait_to_be_logged_in(email=TEST_EMAIL)

		# Теперь она выходит из системы.
		self.browser.find_element(By.LINK_TEXT, 'Log out').click()

		# Она вышла из системы.
		self.wait_to_be_logged_out(email=TEST_EMAIL)


	def wait_for_email(self, test_email, subject):
		"""Ожидать электронное сообщение."""
		if not self.staging_server:
			email = mail.outbox[0]
			self.assertIn(test_email, email.to)
			self.assertEqual(email.subject, subject)
			return email.body

		email_id = None
		start = time.time()
		inbox = poplib.POP3_SSL('pop.gmail.com')

		try:
			inbox.user(test_email)
			inbox.pass_(os.environ['GMAIL_PASSWORD'])

			while time.time() - start < 60:
				# Получить 10 самых новых сообщении.
				count, _ = inbox.stat()
				for i in reversed(range(max(1, count - 10), count + 1)):
					print('getting msg', i)
					_, lines, __ = inbox.retr(1)
					lines = [l.decode('utf8') for l in lines]
					print(lines)
					if f'Subject: {subject}' in lines:
						email_id = 1
						body = '\n'.join(lines)
						return body
				time.sleep(5)
		finally:
			if email_id:
				inbox.dele(email_id)
			inbox.quit()
