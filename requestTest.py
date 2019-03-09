import requests
import cv2


FOLDER_8 = "test_captcha/size8/"
FOLDER_4 = "test_captcha/size4/"

image = open(FOLDER_4+str(0)+".png", 'rb')

files = {
    'file': ('image.png', image),
}

url = 'http://127.0.0.1:5000/4' #/8 for 8sized, /4 for 4sized

response = requests.post(url, files=files).json()
print(response['prediction'])
# response['prediction'] is actually the desired captcha
