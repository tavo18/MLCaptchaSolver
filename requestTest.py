import requests
import cv2


FOLDER = "test_captcha/size8/"
image = cv2.imread(FOLDER+str(0)+".png")

url = 'http://127.0.0.1:5000/'
params ={'query': image}
response = requests.get(url, params)
response.json()