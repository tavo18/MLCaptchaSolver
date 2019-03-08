import requests
import cv2


FOLDER = "test_captcha/size8/"
# image = cv2.imread(FOLDER+str(0)+".png")

image = open(FOLDER+str(0)+".png", 'rb')

files = {
    'file': ('image.png', image),
}

url = 'http://127.0.0.1:5000/'
# params ={'query': image}
response = requests.post(url, files=files).json()
print(response['prediction'])
# response['prediction'] is actually the desired captcha
