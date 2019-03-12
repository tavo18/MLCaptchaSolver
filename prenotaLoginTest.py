# coding=utf-8

import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

USER = "marangoniricardo4@gmail.com"
PASS = "Richard81"


headers = {
	"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Language": "es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3",
	"Accept-Encoding": "gzip, deflate, br",
	"Referer": "https://prenotaonline.esteri.it/login.aspx?cidsede=100076&returnUrl=%2f%2f",
	"Content-Type": "application/x-www-form-urlencoded",
	# Content-Length: 32710
	"Connection": "keep-alive",
	"Host": "prenotaonline.esteri.it",
	# Cookie: _ga=GA1.2.1771542195.1538579413; ASP.NET_SessionId=nacgsr45ns2xk145dfy03sbc; publicform=4EB8F9E676101233EC1CE9DC92B7564AB13C9A05344ED5C2281FC2353DFC012B979095293AD8DF761956CED1666C5EC0BE3FE42E8F6AE7C1A701557D01894208B71D3512D96B74547F7D5AA01D8AF0D96DE013868701C83A07A8636667188A6FA9484128019B7026F5EB4D41288D8AB721602193FD4CF4057A561BBF284F09D3E1E28F4DA2BFED4B3F54A5AED8DA83FEB9B3B8CA
	"Upgrade-Insecure-Requests": "1"
}



parametrosIniciales = {
	'__EVENTTARGET': '',
	'__EVENTARGUMENT': '',
	'BtnLogin': 'Login+usuario+ya+registrado'
}

parametrosLogin = {
	'__EVENTTARGET': '',
	'__EVENTARGUMENT': '',
	'BtnConfermaL': 'Login',
	'UserName':	USER
	'Password':	PASS
}


with requests.Session() as s:
	url = "https://prenotaonline.esteri.it/login.aspx?cidsede=100076&returnUrl=%2f%2f"
	r = s.get(url, headers = headers)
	soup = BeautifulSoup(r.content, 'html5lib')
	parametrosIniciales['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value'].encode("utf-8")
	parametrosIniciales['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value'].encode("utf-8")
	parametrosIniciales['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value'].encode("utf-8")
	

	r = s.post(url, data=parametrosIniciales, headers=headers)
	
	soup = BeautifulSoup(r.content, 'html5lib')
	# 
	urlCaptcha = "https://prenotaonline.esteri.it/"+soup.find('img', attrs={'id': 'captchaLogin'})['src']
	imr = s.get(urlCaptcha,headers = headers) 
	im = Image.open(BytesIO(imr.content))

	# 
	files = {
	    'file': ('image.png', BytesIO(imr.content))
	}

	# Captcha prediction request to local server
	response = requests.post('http://127.0.0.1:5000/4', files=files).json()
	print(response['prediction'])


	parametrosLogin['loginCaptcha'] =  response['prediction']
	parametrosLogin['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value'].encode("utf-8")
	parametrosLogin['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value'].encode("utf-8")
	parametrosLogin['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value'].encode("utf-8")



	r = s.post(url, data=parametrosLogin,headers=headers)
	print(r.content)