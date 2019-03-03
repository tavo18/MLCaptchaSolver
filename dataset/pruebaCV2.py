import numpy as np
import imutils
import cv2
import pickle
from PIL import Image
from io import BytesIO


image = cv2.imread("/home/tavo/MEGA/ProyectoBOT/captcha2.jpeg")
# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


height,width,c = image.shape
print(height, width)
cropped1 = image[0:int(height/2),int(width/10):int(width/10)*2]
cropped2 = image[0:int(height/2),int(width/10)*2:int(width/10)*3]
cropped3 = image[0:int(height/2),int(width/10)*3:int(width/10)*4]
cropped4 = image[0:int(height/2),int(width/10)*4:int(width/10)*5]
cropped5 = image[0:int(height/2),int(width/10)*5:int(width/10)*6]
cropped6 = image[0:int(height/2),int(width/10)*6:int(width/10)*7]
cropped7 = image[0:int(height/2),int(width/10)*7:int(width/10)*8]
cropped8 = image[0:int(height/2),int(width/10)*8:int(width/10)*9]
cv2.imshow("output",cropped1)
cv2.waitKey()

# cImg = []
# height,width,c = image.shape
# print(width,height)

# cropped1 = image[0:height,(width/5):(width/5)*2]
# cropped2 = image[0:height,(width/5)*2:(width/5)*3]
# cImg.append(image[(width/5):(width/5)*2, 0:height])
# # letra1.save("/home/tavo/MEGA/ProyectoBOT/dataset/ejemplos/"+str(i)+".png", "PNG")
# cImg.append(img.crop(((width/5)*2, 0, (width/5)*3, height)))
# cImg.append(img.crop(((width/5)*3, 0, (width/5)*4, height)))
# cImg.append(img.crop(((width/5)*4, 0, 100, height)))


# image = Image.open("/home/tavo/MEGA/ProyectoBOT/MLCaptchaSolver/test_captcha/0.png")
# width,height = image.size
# croppedI1 = image.crop(((width/5), 0, (width/5)*2, height))
# croppedI2 = image.crop(((width/5)*2, 0, (width/5)*3, height))

# croppedI1.show()