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
	"Referer": "https://prenotaonline.esteri.it/login.aspx?cidsede=100064&returnUrl=%2f%2f",
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
	'UserName':	USER,
	'Password':	PASS
}

parametrosCita = {
	'ctl00$repFunzioni$ctl00$btnMenuItem': 'Haga su cita'
}

parametrosTipoCita = {
	#Parametros del servicio emision del pasaporte
	'ctl00$ContentPlaceHolder1$rpServizi$ctl01$h_idservizio': '796',
	'ctl00$ContentPlaceHolder1$rpServizi$ctl01$h_settimane':	'2',
	'ctl00$ContentPlaceHolder1$rpServizi$ctl01$h_bloccato':	'False',
	'ctl00$ContentPlaceHolder1$rpServizi$ctl01$h_attivo':	'True',
	# 'ctl00$ContentPlaceHolder1$rpServizi$ctl01$btnNomeServizio':	'Pasaportes',

	#Parametros del servicio ciudadania hijos mayores de 18
	'ctl00$ContentPlaceHolder1$rpServizi$ctl02$h_idservizio':	'861',
	'ctl00$ContentPlaceHolder1$rpServizi$ctl02$h_settimane':	'4',
	'ctl00$ContentPlaceHolder1$rpServizi$ctl02$h_bloccato':	'False',
	'ctl00$ContentPlaceHolder1$rpServizi$ctl02$h_attivo':	'True',
	# 'ctl00$ContentPlaceHolder1$rpServizi$ctl02$btnNomeServizio':	'Ciudadanía+hijos+mayores+de+18+años',

	#Parametros del servicio reconstrucción de ciudadanía
	'ctl00$ContentPlaceHolder1$rpServizi$ctl03$h_idservizio':	'1753',
	'ctl00$ContentPlaceHolder1$rpServizi$ctl03$btnNomeServizio':	'Reconstrucción+de+ciudadanía',
	'ctl00$ContentPlaceHolder1$rpServizi$ctl03$h_settimane':	'2',
	'ctl00$ContentPlaceHolder1$rpServizi$ctl03$h_bloccato':	'False',
	'ctl00$ContentPlaceHolder1$rpServizi$ctl03$h_attivo':	'True',
	#Parametros del servicio visto consular
	'ctl00$ContentPlaceHolder1$rpServizi$ctl04$h_idservizio':	'1808',
	'ctl00$ContentPlaceHolder1$rpServizi$ctl04$h_settimane':	'2',
	'ctl00$ContentPlaceHolder1$rpServizi$ctl04$h_bloccato':	'False',
	'ctl00$ContentPlaceHolder1$rpServizi$ctl04$h_attivo':	'True',
	# 'ctl00$ContentPlaceHolder1$rpServizi$ctl04$btnNomeServizio':	'Legalización+de+actas'
	'ctl00$ContentPlaceHolder1$hiServizio': '',
	'__VIEWSTATEENCRYPTED':''
}

parametrosDatosAdicionales = {
	'ctl00$ContentPlaceHolder1$acc_datiAddizionali1$btnContinua': 'Confirmación',
	'ctl00$ContentPlaceHolder1$acc_datiAddizionali1$txtNote': '',
	'__VIEWSTATEENCRYPTED':''
}

parametrosSeleccionDia = {
	'__VIEWSTATEENCRYPTED': ''
}

parametrosConfirmacionDia = {
	'ctl00$ContentPlaceHolder1$acc_Calendario1$repFasce$ctl01$btnConferma': 'Confirmación',
	'__VIEWSTATEENCRYPTED': ''
}

parametrosConfirmacionFinal = {
	'__VIEWSTATEENCRYPTED': '',
	'ctl00$ContentPlaceHolder1$btnFinalConf': 'Confirmación'
}


with requests.Session() as s:
	url = "https://prenotaonline.esteri.it/login.aspx?cidsede=100064&returnUrl=%2f%2f"
	r = s.get(url, headers = headers)
	soup = BeautifulSoup(r.content, 'html5lib')
	parametrosIniciales['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value'].encode("utf-8")
	parametrosIniciales['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value'].encode("utf-8")
	parametrosIniciales['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value'].encode("utf-8")
	
	print("Pressing first button...")
	r = s.post(url, data=parametrosIniciales, headers=headers)
	if(r.status_code == 200):
		print("Success!")

	print("Completing log-in form...")
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
	print("Obtained captcha: "+response['prediction'])


	parametrosLogin['loginCaptcha'] =  response['prediction']
	parametrosLogin['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value'].encode("utf-8")
	parametrosLogin['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value'].encode("utf-8")
	parametrosLogin['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value'].encode("utf-8")

	

	r = s.post(url, data=parametrosLogin, headers=headers)

	soup = BeautifulSoup(r.content, 'html5lib')

	loginValidation = soup.find('input', attrs={'name': 'ctl00$repFunzioni$ctl01$btnMenuItem'})

	if loginValidation:
		print("Successful log-in!")

	# After 100 same get or post request, server disconects the account.

	#---------------- SECCION HAGA SU CITA ---------------

	soup = BeautifulSoup(r.content, 'html5lib')

	parametrosCita['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value'].encode("ascii")
	parametrosCita['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value'].encode("ascii")
	parametrosCita['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value'].encode("ascii")

	headers["Referer"] = "https://prenotaonline.esteri.it/default.aspx"
	# headers["Content-Length"] = "1336"
	
	# #Atenti! se debe cambiar la URL porque las solicitudes cambian de destino una vez logeado.
	urlIn = "https://prenotaonline.esteri.it/default.aspx"
	#Click en "Haga su cita"
	r = s.post(urlIn, data=parametrosCita,headers=headers)

	#---------------- FIN SECCION HAGA SU CITA ---------------

	#---------------- SECCION TIPOS DE TURNO ---------------
	soup = BeautifulSoup(r.content, 'html5lib')

	parametrosTipoCita['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value'].encode("utf-8")
	parametrosTipoCita['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value'].encode("utf-8")
	parametrosTipoCita['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value'].encode("utf-8")
	
	# #Atenti! cambia de URL
	urlIn = "https://prenotaonline.esteri.it/acc_Prenota.aspx"
	headers["Referer"] = "https://prenotaonline.esteri.it/acc_Prenota.aspx"

	# #Click en tipo de turno
	r = s.post(urlIn, data=parametrosTipoCita,headers=headers)
	# print(r.content)

	#---------------- FIN SECCION TIPOS DE TURNO ---------------
	
	#---------------- SECCION DATOS ADICIONALES ---------------

	soup = BeautifulSoup(r.content, 'html5lib')

	parametrosDatosAdicionales['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value'].encode("utf-8")
	parametrosDatosAdicionales['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value'].encode("utf-8")
	parametrosDatosAdicionales['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value'].encode("utf-8")

	r = s.post(urlIn, data=parametrosDatosAdicionales,headers=headers)

	#---------------- FIN SECCION DATOS ADICIONALES ---------------

	#---------------- SECCION CALENDARIO ---------------

	soup = BeautifulSoup(r.content, 'html5lib')

	if soup.find('div', attrs={'id': 'calwrapper'}):
		print("Se ingresó al calendario de forma correcta.")


	# A LAS 20 EN PUNTO HACER EL REQUEST AL DIA CORRESPONDIENTE

	print("Esperando por turnos...")
	# Mientras el resultado de la siguiente linea sea falso, reenviar post request anterior:
	contador = 1
	while not soup.find('input', attrs={'class': 'pulsanteCalendario'}):
		try:
			time.sleep(2)
			r = s.post(urlIn, data=parametrosDatosAdicionales,headers=headers)
			soup = BeautifulSoup(r.content, 'html5lib')
			print("Por ahora nada... intento número: "+str(contador))
			contador = contador + 1
		except requests.exceptions.ConnectionError:
			print("Error de conexion")
	# soup.find('input', attrs={'class': 'pulsanteCalendario'})
	# Tener en cuenta la restricción de 100 reenvios de request (desconecta de la cuenta)

	# A partir de acá se salió del bucle anterior, lo cual indica que hay turnos disponibles
	print("Trunos disponibles!")


	# Nombre del input del calendario, se obtiene a partir de su clase 'pulsanteCalendario'
	inputName = soup.find('input', attrs={'class': 'pulsanteCalendario'})['name'].encode("utf-8")
	# Input de horarios
	divOrari = soup.find('div', attrs={'id': 'orari'})
	hiddenInputName = divOrari.find('input')['name'].encode("utf-8")
	
	# Seteo el valor (día) del input disponible en los parámetros del request
	parametrosSeleccionDia[inputName] = soup.find('input', attrs={'class': 'pulsanteCalendario'})['value'].encode("utf-8")
	# Setel de parámetro del hidden input del horario
	parametrosSeleccionDia[hiddenInputName] = divOrari.find('input')['value'].encode("utf-8")
	# Los tres de siempre
	parametrosSeleccionDia['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value'].encode("utf-8")
	parametrosSeleccionDia['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value'].encode("utf-8")
	parametrosSeleccionDia['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value'].encode("utf-8")

	# Post request para presionar el dia disponible
	r = s.post(urlIn, data=parametrosSeleccionDia, headers=headers)

	# --dia seleccionado--
	soup = BeautifulSoup(r.content, 'html5lib')

	# Input de horarios
	divOrari = soup.find('div', attrs={'id': 'orari'})
	hiddenInputName = divOrari.find('input')['name'].encode("utf-8")

	# Seteo de parámetro del hidden input del horario (antes se obtuvo el nombre, luego, el valor)
	parametrosConfirmacionDia[hiddenInputName] = divOrari.find('input')['value'].encode("utf-8")
	# Los tres de siempre
	parametrosConfirmacionDia['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value'].encode("utf-8")
	parametrosConfirmacionDia['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value'].encode("utf-8")
	parametrosConfirmacionDia['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value'].encode("utf-8")

	# Post request para confirmar el dia disponible
	r = s.post(urlIn, data=parametrosConfirmacionDia, headers=headers)

	#---------------- FIN SECCION CALENDARIO ---------------

	#---------------- SECCION CONFIRMACION FINAL ---------------
	soup = BeautifulSoup(r.content, 'html5lib')

	#SE MUESTRA EL CAPTCHA, SE LO INGRESA Y POR ÚLTIMO SE ENVÍA EL REQUEST FINAL
	#PARA ESTE PASO FALTAN DETERMINAR LOS PARÁMETROS DEL REQUEST FINAL. HAY QUE SOLICITAR UN TURNO SI O SI.
	urlCaptchaFinal = "https://prenotaonline.esteri.it/"+soup.find('img', attrs={'id': 'ctl00_ContentPlaceHolder1_confCaptcha'})['src']
	imrFinal = s.get(urlCaptchaFinal,headers = headers)
	# imFinal = Image.open(BytesIO(imrFinal.content))

	files = {
	    'file': ('image.png', BytesIO(imrFinal.content))
	}
	# Captcha prediction request to local server
	response = requests.post('http://127.0.0.1:5000/8', files=files).json()
	print("Obtained captcha: "+response['prediction'])

	#Seteo del captcha a los parámetros del post request
	parametrosConfirmacionFinal['ctl00_ContentPlaceHolder1_captchaConf'] = response['prediction']
	# Los tres de siempre
	parametrosConfirmacionFinal['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value'].encode("utf-8")
	parametrosConfirmacionFinal['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value'].encode("utf-8")
	parametrosConfirmacionFinal['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value'].encode("utf-8")

	# Post request para confirmar el turno
	r = s.post(urlIn, data=parametrosConfirmacionFinal, headers=headers)
	#---------------- FIN SECCION CONFIRMACION FINAL ---------------
	print(r.content)