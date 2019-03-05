from keras.models import load_model
from helpers import resize_to_fit
from imutils import paths
import numpy as np
import imutils
import cv2
import pickle
import os, os.path
#from PIL import Image
#from io import BytesIO

MODEL_FILENAME = "captcha_model_8.hdf5"
MODEL_LABELS_FILENAME = "model_labels_8.dat"
CAPTCHA_IMAGE_FOLDER = "test_captcha/size8" 

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 


# Load up the model labels (so we can translate model predictions to actual letters)
with open(MODEL_LABELS_FILENAME, "rb") as f:
    lb = pickle.load(f)

# Load the trained neural network
model = load_model(MODEL_FILENAME)

def predict8(image):
	# define the list of letters in the captcha
    letter_images = []
    height,width,c = image.shape
    

    # 8 characters captchas:
    letter_images.append(image[13:int(height/2),int(width/10):int((width/10)*2.3)])
    letter_images.append(image[13:int(height/2),int(width/10)*2:int((width/10)*3.3)])
    letter_images.append(image[13:int(height/2),int(width/10)*3:int((width/10)*4.3)])
    letter_images.append(image[13:int(height/2),int(width/10)*4:int((width/10)*5.3)])
    letter_images.append(image[13:int(height/2),int(width/10)*5:int((width/10)*6.3)])
    letter_images.append(image[13:int(height/2),int(width/10)*6:int((width/10)*7.3)])
    letter_images.append(image[13:int(height/2),int(width/10)*7:int((width/10)*8.3)])
    letter_images.append(image[13:int(height/2),int(width/10)*8:int((width/10)*9.3)])    
    
    # Create a list to hold our predicted letters
    predictions = []

    # loop over the letters
    for letter_image in letter_images:

        # Turn the single image into a 4d list of images to make Keras happy
        # Add a third channel dimension to the image to make Keras happy
        # letter_image = np.expand_dims(letter_image, axis=2)
        letter_image = np.expand_dims(letter_image, axis=0)

        

        # Ask the neural network to make a prediction
        prediction = model.predict(letter_image)

        # Convert the one-hot-encoded prediction back to a normal letter
        letter = lb.inverse_transform(prediction)[0]
        predictions.append(letter)

    # Print the captcha's text
    captcha_text = "".join(predictions)
    return captcha_text
    # print("CAPTCHA text is: {}".format(captcha_text))