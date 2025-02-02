from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages


def send_login_email(request):
	"""Отправить сообщение для входа в систему."""
	email = request.POST['email']
	send_mail(
		'Your login link for SuperLists',
		'Use this link to log in',
		'narekbayanduryan16@gmail.com',
		[email]
	)

	messages.success(
		request,
		"Check your email, you'll find a message with a link that will log you into the site.",
	)

	return redirect('/')
