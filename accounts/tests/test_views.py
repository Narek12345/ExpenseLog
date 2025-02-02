from unittest.mock import patch, call

from django.test import TestCase



class SendLoginEmailViewTest(TestCase):
	"""Тест представления, которое отправляет сообщение для входа в систему."""


	def test_redirects_to_home_page(self):
		"""Тест: переадресуется на домашнюю страницу."""
		response = self.client.post('/accounts/send_login_email', data={
			'email': 'edith@example.com'
		})
		self.assertRedirects(response, '/')


	@patch('accounts.views.send_mail')
	def test_sends_mail_to_address_from_post(self, mock_send_mail):
		"""Тест: отправляется сообщение на адрес из метода post."""
		self.client.post('/accounts/send_login_email', data={
			'email': 'edith@example.com',
		})

		self.assertEqual(mock_send_mail.called, True)
		(subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
		self.assertEqual(subject, 'Your login link for SuperLists')
		self.assertEqual(from_email, 'narekbayanduryan16@gmail.com')
		self.assertEqual(to_list, ['edith@example.com'])


	@patch('accounts.views.messages')
	def test_adds_seccess_message_with_mocks(self, mock_messages):
		response = self.client.post('/accounts/send_login_email', data={
			'email': 'edith@example.com'
		})
		expected = "Check your email, you'll find a message with a link that will log you into the site."

		self.assertEqual(
			mock_messages.success.call_args,
			call(response.wsgi_request, expected),
		)



class LoginViewTest(TestCase):
	"""Тест представления входа в систему."""


	def test_redirects_to_home_page(self):
		"""Тест: переадресуется на домашнюю страницу."""	
		response = self.client.get('/accounts/login?token=abcd123')
		self.assertRedirects(response, '/')
