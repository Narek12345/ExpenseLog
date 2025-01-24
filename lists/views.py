from django.shortcuts import render


def home_page(request):
	"""Домашняя страница."""
	return render(request, 'home.html')
