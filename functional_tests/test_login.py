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


SUBJECT = 'Your login link for SuperLists'



class LoginTest(FunctionalTest):
	"""Тест регистрации в системе."""


	def test_can_get_email_link_to_log_in(self):
		"""Тест: можно получить ссылку по почте для регистрации."""
		# Эдит заходит на офигительный сайт суперсписков и впервые замечает раздел "войти" в навигационной панели.
		# Он говорит ей ввести свой адрес электронной почты, что она и делает.
		if self.staging_server:
			test_email = 'narekbayanduryan16@gmail.com'
		else:
			test_email = 'edith@example.com'

		self.browser.get(self.live_server_url)
		self.browser.find_element(By.NAME, 'email').send_keys(test_email)
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
		body = self.wait_for_email(test_email, SUBJECT)

		# Оно содержит ссылку на url-адрес.
		self.assertIn('Use this link to log in', body)
		url_search = re.search(r'http://.+/.+$', body)

		if not url_search:
			self.fail(f'Could not find url in email body:\n{body}')

		url = url_search.group(0)
		self.assertIn(self.live_server_url, url)

		# Эдит нажимает на ссылку.
		self.browser.get(url)

		# Она зарегестрировалась в системе.
		self.wait_to_be_logged_in(email=test_email)

		# Теперь она выходит из системы.
		self.browser.find_element(By.LINK_TEXT, 'Log out').click()

		# Она вышла из системы.
		self.wait_to_be_logged_out(email=test_email)


	def wait_for_email(self, test_email, subject):
		"""Ожидать электронное сообщение."""
		if not self.staging_server:
			email_message = mail.outbox[0]
			self.assertIn(test_email, email_message.to)
			self.assertEqual(email_message.subject, subject)
			return email_message.body

		mail_client = imaplib.IMAP4_SSL('imap.gmail.com')
		mail_client.login(test_email, os.getenv('GMAIL_PASSWORD'))
		mail_client.select('inbox')

		status, messages = mail_client.search(None, 'ALL')
		messages_id = messages[0].split()

		last_messages_id = messages_id[-20:][::-1]

		for message_id in last_messages_id:
			message_id = str(message_id, 'utf-8')
			status, msg_data = mail_client.fetch(message_id, '(RFC822)')

			for response_part in msg_data:
				if isinstance(response_part, tuple):
					msg_email = email.message_from_bytes(response_part[1])
					current_email_subject, encoding = decode_header(msg_email['Subject'])[0]

					if isinstance(current_email_subject, bytes):
						current_email_subject = current_email_subject.decode(encoding if encoding else "utf-8")
					try:
						self.assertIn(test_email, msg_email.get('From'))
						self.assertEqual(current_email_subject, subject)

						# Разбираем тело сообщения.
						body = ""
						if msg_email.is_multipart():
							for part in msg_email.walk():
								content_type = part.get_content_type()
								content_disposition = str(part.get("Content-Disposition"))

								if content_type == "text/plain" and "attachment" not in content_disposition:
									body = part.get_payload(decode=True).decode().strip()
									break
						else:
							body = msg_email.get_payload(decode=True).decode().strip()
						return body
					except Exception as e:
						continue
