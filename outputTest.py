import cv2
from predictor import predict8

FOLDER = "test_captcha/size8/"
image = cv2.imread(FOLDER+str(0)+".png")

print(predict8(image))