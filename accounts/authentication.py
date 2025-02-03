from accounts.models import User, Token



class PasswordlessAuthenticationBackend(object):
	"""Беспарольный серверный процессор аутентификации."""


	def authenticate(self, request, uid):
		"""Аутентифицировать."""
		try:
			token = Token.objects.get(uid=uid)
			return User.objects.get(email=token.email)
		except User.DoesNotExist:
			return User.objects.create(email=token.email)
		except Token.DoesNotExist:
			return None


	def get_user(self, email):
		"""Получить пользователя."""
		try:
			return User.objects.get(email=email)
		except User.DoesNotExist:
			return None
