from unittest.mock import patch, call

from django.test import TestCase

from accounts.models import Token



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


	def test_creates_token_associated_with_email(self):
		"""Тест: создается маркер, связанный с электронной почтой."""
		self.client.post('/accounts/send_login_email', data={
			'email': 'edith@example.com'
		})
		token = Token.objects.first()
		self.assertEqual(token.email, 'edith@example.com')


	@patch('accounts.views.send_mail')
	def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
		"""Тест: отсылается ссылка на вход в систему, используя uid маркера."""
		self.client.post('/accounts/send_login_email', data={
			'email': 'edith@example.com'
		})

		token = Token.objects.first()
		expected_url = f'http://testserver/accounts/login?token={token.uid}'
		(subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
		self.assertIn(expected_url, body)



class LoginViewTest(TestCase):
	"""Тест представления входа в систему."""


	def test_redirects_to_home_page(self):
		"""Тест: переадресуется на домашнюю страницу."""	
		response = self.client.get('/accounts/login?token=abcd123')
		self.assertRedirects(response, '/')


	@patch('accounts.views.auth')
	def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
		"""Тест: вызывается authenticate с uid из GET-запроса."""
		self.client.get('/accounts/login?token=abcd123')
		self.assertEqual(
			mock_auth.authenticate.call_args,
			call(uid='abcd123')
		)
