import os
import re
import time
import email
import imaplib

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from email.header import decode_header

from django.core import mail

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
			email_out = mail.outbox[0]  # Переименовано здесь
			self.assertIn(test_email, email_out.to)
			self.assertEqual(email_out.subject, subject)
			return email_out.body

		mail = imaplib.IMAP4_SSL('imap.gmail.com')
		mail.login(test_email, os.getenv('GMAIL_PASSWORD'))
		mail.select('inbox')

		status, messages = mail.search(None, 'ALL')
		messages_id = messages[0].split()

		last_messages_id = messages_id[-20:][::-1]

		for message_id in last_messages_id:
			message_id = str(message_id, 'utf-8')
			status, msg_data = mail.fetch(message_id, '(RFC822)')

			for response_part in msg_data:
				if isinstance(response_part, tuple):
					msg_email = email.message_from_bytes(response_part[1])
					current_email_subject, encoding = decode_header(msg_email['Subject'])[0]

					if isinstance(current_email_subject, bytes):
						current_email_subject = current_email_subject.decode(encoding if encoding else "utf-8")

					try:
						self.assertIn(test_email, msg_email.get('From'))
						self.assertEqual(current_email_subject, subject)

						body = msg_email.get_payload(decode=True).decode()

						mail.close()
						mail.logout()

						print(body)
						return body
					except Exception as e:
						continue
