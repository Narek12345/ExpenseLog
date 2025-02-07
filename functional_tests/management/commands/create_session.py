from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand


User = get_user_model()



class Command(BaseCommand):
	"""Команда."""


	def add_arguments(self, parser):
		"""Добавить аргументы."""
		parser.add_argument('email')


	def handle(self, *args, **options):
		"""Обработать."""
		session_key = create_pre_authenticated_session(options['email'])
		self.stdout.write(session_key)



def create_pre_authenticated_session(email):
	"""Создать предварительно аутентифицированный сеанс."""
	user = User.objects.create(email=email)
	session = SessionStore()
	session[SESSION_KEY] = user.pk
	session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
	session.save()
	return session.session_key
