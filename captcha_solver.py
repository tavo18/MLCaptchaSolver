from keras.models import load_model
from helpers import resize_to_fit
from imutils import paths
import numpy as np
import imutils
import cv2
import pickle
from PIL import Image
from io import BytesIO

MODEL_FILENAME = "captcha_model.hdf5"
MODEL_LABELS_FILENAME = "model_labels.dat"
CAPTCHA_IMAGE_FOLDER = "test_captcha/size4" # size8 for 8sized captchas


# Load up the model labels (so we can translate model predictions to actual letters)
with open(MODEL_LABELS_FILENAME, "rb") as f:
    lb = pickle.load(f)

# Load the trained neural network
model = load_model(MODEL_FILENAME)

# Grab some random CAPTCHA images to test against.
captcha_image_files = list(paths.list_images(CAPTCHA_IMAGE_FOLDER))

# loop over the image paths
for image_file in captcha_image_files:
    # Load the image and convert it to grayscale
    image = cv2.imread(image_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # define the list of letters in the captcha
    letter_images = []
    height,width = image.shape
    
    letter_images.append(image[0:height,int((width/5)):int((width/5))*2])
    letter_images.append(image[0:height,int((width/5))*2:int((width/5))*3])
    letter_images.append(image[0:height,int((width/5))*3:int((width/5))*4])
    letter_images.append(image[0:height,int((width/5))*4:100])

    # 8 characters captchas:
    # letter_image_regions.append(image[0:int(height/2),int(width/10):int(width/10)*2])
    # letter_image_regions.append(image[0:int(height/2),int(width/10)*2:int(width/10)*3])
    # letter_image_regions.append(image[0:int(height/2),int(width/10)*3:int(width/10)*4])
    # letter_image_regions.append(image[0:int(height/2),int(width/10)*4:int(width/10)*5])
    # letter_image_regions.append(image[0:int(height/2),int(width/10)*5:int(width/10)*6])
    # letter_image_regions.append(image[0:int(height/2),int(width/10)*6:int(width/10)*7])
    # letter_image_regions.append(image[0:int(height/2),int(width/10)*7:int(width/10)*8])
    # letter_image_regions.append(image[0:int(height/2),int(width/10)*8:int(width/10)*9])    
    
    # Create a list to hold our predicted letters
    predictions = []

    # loop over the letters
    for letter_image in letter_images:

        # Turn the single image into a 4d list of images to make Keras happy
        # Add a third channel dimension to the image to make Keras happy
        letter_image = np.expand_dims(letter_image, axis=2)
        letter_image = np.expand_dims(letter_image, axis=0)

        

        # Ask the neural network to make a prediction
        prediction = model.predict(letter_image)

        # Convert the one-hot-encoded prediction back to a normal letter
        letter = lb.inverse_transform(prediction)[0]
        predictions.append(letter)

    # Print the captcha's text
    captcha_text = "".join(predictions)
    print("CAPTCHA text is: {}".format(captcha_text))

# First attempt using simple B&W preprocessing: 7/10
# 
# CAPTCHA text is: pckr
# CAPTCHA text is: qlfm
# CAPTCHA text is: jmp1
# CAPTCHA text is: lntm
# CAPTCHA text is: ulbr
# CAPTCHA text is: r2mh
# CAPTCHA text is: 8b3q
# CAPTCHA text is: gypj
# CAPTCHA text is: df8u
# CAPTCHA text is: qtl8