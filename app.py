from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import pickle
import numpy as np
from keras.models import load_model
from imutils import paths
import imutils
import cv2
import os, os.path
from PIL import Image

app = Flask(__name__)
api = Api(app)

MODEL_FILENAME_8 = "captcha_model_8.hdf5"
MODEL_FILENAME_4 = "captcha_model2.hdf5"
MODEL_LABELS_FILENAME = "model_labels_8.dat"
CAPTCHA_IMAGE_FOLDER = "test_captcha/size8" 

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 


# Load up the model labels (so we can translate model predictions to actual letters)
with open(MODEL_LABELS_FILENAME, "rb") as f:
    lb = pickle.load(f)

# Load the trained neural network model for 8sized captchas
model = load_model(MODEL_FILENAME_8)
model._make_predict_function()

# Load the trained neural network model for 4sized captchas
model4 = load_model(MODEL_FILENAME_4)
model4._make_predict_function()

# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('query')


class PredictCaptcha8(Resource):
    def post(self):
        # use parser and find the user's query
        pil_image = Image.open(request.files['file'])
        image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # vectorize the user's query and make a prediction
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
        # predictions.append(image.shape)
        # predictions.append(letter_images[0].shape)

        # output = predictions

        # loop over the letters
        for letter_image in letter_images:



        #     # Turn the single image into a 4d list of images to make Keras happy
        #     # Add a third channel dimension to the image to make Keras happy
        #     # letter_image = np.expand_dims(letter_image, axis=2)
            letter_image = np.expand_dims(letter_image, axis=0)

            

        #     # Ask the neural network to make a prediction
            prediction = model.predict(letter_image)

        #     # Convert the one-hot-encoded prediction back to a normal letter
            letter = lb.inverse_transform(prediction)[0]
            predictions.append(letter)

        captcha_text = ''.join(predictions)
        # # create JSON object
        
        
        return {'prediction': captcha_text}

class PredictCaptcha4(Resource):
    def post(self):
        # use parser and find the user's query
        pil_image = Image.open(request.files['file'])
        image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # vectorize the user's query and make a prediction
        letter_images = []
        height,width,c = image.shape
        

        # 4 characters captchas:
        letter_images.append(image[0:height,int((width/5)):int((width/5))*2])
        letter_images.append(image[0:height,int((width/5))*2:int((width/5))*3])
        letter_images.append(image[0:height,int((width/5))*3:int((width/5))*4])
        letter_images.append(image[0:height,int((width/5))*4:100])

        
        # Create a list to hold our predicted letters
        predictions = []
        # predictions.append(image.shape)
        # predictions.append(letter_images[0].shape)

        # output = predictions

        # loop over the letters
        for letter_image in letter_images:



        #     # Turn the single image into a 4d list of images to make Keras happy
        #     # Add a third channel dimension to the image to make Keras happy
        #     # letter_image = np.expand_dims(letter_image, axis=2)
            letter_image = np.expand_dims(letter_image, axis=0)

            

        #     # Ask the neural network to make a prediction
            prediction = model4.predict(letter_image)

        #     # Convert the one-hot-encoded prediction back to a normal letter
            letter = lb.inverse_transform(prediction)[0]
            predictions.append(letter)

        captcha_text = ''.join(predictions)
        # # create JSON object
        
        
        return {'prediction': captcha_text}


# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(PredictCaptcha8, '/8')
api.add_resource(PredictCaptcha4, '/4')


if __name__ == '__main__':
    app.run(debug=True)