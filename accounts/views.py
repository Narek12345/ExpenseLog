from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from django.contrib import messages, auth

from accounts.models import Token


def send_login_email(request):
	"""Отправить сообщение для входа в систему."""
	email = request.POST['email']
	token = Token.objects.create(email=email)
	url = request.build_absolute_uri(
		reverse('login') + '?token=' + str(token.uid)
	)
	message_body = f'Use this link to log in:\n\n{url}'
	send_mail(
		'Your login link for SuperLists',
		message_body,
		'narekbayanduryan16@gmail.com',
		[email]
	)

	messages.success(
		request,
		"Check your email, you'll find a message with a link that will log you into the site.",
	)

	return redirect('/')


def login(request):
	"""Зарегестрировать вход в систему."""
	user = auth.authenticate(uid=request.GET.get('token'))
	if user:
		auth.login(request, user)
	return redirect('/')


def logout(request):
	"""Выйти из системы."""
	auth.logout(request)
	return redirect('/')
