from selenium import webdriver


browser = webdriver.Chrome()
browser.get('http://localhost:8000')

assert 'The install worked successfully! Congratulations!' in browser.title
