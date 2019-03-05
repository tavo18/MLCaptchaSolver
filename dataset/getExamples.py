import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

EXAMPLES = 1000
DEST_FOLDER = "/home/tavo/MEGA/ProyectoBOT/dataset/ejemplos8/"
URL_CAPTCHA = "https://prenotaonline.esteri.it/captcha/default.aspx?pos=1&vers=497517779"

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

with requests.Session() as s:
	i=0
	while True:
		try:
			imr = s.get(URL_CAPTCHA,headers = headers) #parte clave, obtener el captcha
			im = Image.open(BytesIO(imr.content))
			im.save(DEST_FOLDER+str(i)+".png", "PNG")
			print("Imagen "+str(i+1)+" de "+str(EXAMPLES))
			i+=1	
		except requests.exceptions.ConnectionError:
			print("Error de conexion")
		except requests.exceptions.Timeout:
			print("Timeout")

		if i==EXAMPLES:
			break



	