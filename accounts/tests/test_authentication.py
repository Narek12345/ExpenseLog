from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token


User = get_user_model()



class AuthenticateTest(TestCase):
	"""Тест аутентификации."""


	def test_returns_None_if_no_such_token(self):
		"""Тест: возвращается None, если нет такого маркера."""
		result = PasswordlessAuthenticationBackend().authenticate(
			'no-such-token'
		)
		self.assertIsNone(result)
