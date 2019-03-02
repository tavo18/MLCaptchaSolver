import cv2
import pickle
import os.path
import numpy as np
from imutils import paths
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Flatten, Dense
from helpers import resize_to_fit

LETTER_IMAGES_FOLDER = "/content/MLCaptchaSolver/MLCaptchaSolver/dataset/examples"
MODEL_FILENAME = "captcha_model.hdf5"
MODEL_LABELS_FILENAME = "model_labels.dat"

# initialize the data and labels
data = []
labels = []

# loop over the input images
for image_file in paths.list_images(LETTER_IMAGES_FOLDER):
    # Load the image and convert it to grayscale
    image = cv2.imread(image_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Resize the letter so it fits in a 20x20 pixel box
    #image = resize_to_fit(image, 20, 20)

    # Add a third channel dimension to the image to make Keras happy
    image = np.expand_dims(image, axis=2)

    # Grab the name of the letter based on the folder it was in
    label = image_file.split(os.path.sep)[-2]

    # Add the letter image and it's label to our training data
    data.append(image)
    labels.append(label)

# scale the raw pixel intensities to the range [0, 1] (this improves training)
data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)

# Split the training data into separate train and test sets
(X_train, X_test, Y_train, Y_test) = train_test_split(data, labels, test_size=0.25, random_state=0)

# Convert the labels (letters) into one-hot encodings that Keras can work with
lb = LabelBinarizer().fit(Y_train)
Y_train = lb.transform(Y_train)
Y_test = lb.transform(Y_test)

# Save the mapping from labels to one-hot encodings.
# We'll need this later when we use the model to decode what it's predictions mean
with open(MODEL_LABELS_FILENAME, "wb") as f:
    pickle.dump(lb, f)

# Build the neural network!
model = Sequential()

# First convolutional layer with max pooling
model.add(Conv2D(20, (5, 5), padding="same", input_shape=(44, 20, 1), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# Second convolutional layer with max pooling
model.add(Conv2D(50, (5, 5), padding="same", activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# Hidden layer with 500 nodes
model.add(Flatten())
model.add(Dense(500, activation="relu"))

# Output layer with 32 nodes (one for each possible letter/number we predict)
model.add(Dense(36, activation="softmax"))

# Ask Keras to build the TensorFlow model behind the scenes
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# Train the neural network
model.fit(X_train, Y_train, validation_data=(X_test, Y_test), batch_size=32, epochs=12, verbose=1)

#EXPECTED OUTPUT

# Train on 2849 samples, validate on 950 samples
# Epoch 1/12
# 2849/2849 [==============================] - 10s 3ms/step - loss: 3.5873 - acc: 0.0305 - val_loss: 3.5839 - val_acc: 0.0242
# Epoch 2/12
# 2849/2849 [==============================] - 9s 3ms/step - loss: 3.5823 - acc: 0.0284 - val_loss: 3.5854 - val_acc: 0.0326
# Epoch 3/12
# 2849/2849 [==============================] - 9s 3ms/step - loss: 3.5833 - acc: 0.0355 - val_loss: 3.5858 - val_acc: 0.0242
# Epoch 4/12
# 2849/2849 [==============================] - 9s 3ms/step - loss: 3.5735 - acc: 0.0340 - val_loss: 3.5515 - val_acc: 0.0242
# Epoch 5/12
# 2849/2849 [==============================] - 9s 3ms/step - loss: 2.6718 - acc: 0.2468 - val_loss: 1.5501 - val_acc: 0.4863
# Epoch 6/12
# 2849/2849 [==============================] - 9s 3ms/step - loss: 0.8729 - acc: 0.7220 - val_loss: 0.5403 - val_acc: 0.8095
# Epoch 7/12
# 2849/2849 [==============================] - 9s 3ms/step - loss: 0.3704 - acc: 0.8940 - val_loss: 0.2564 - val_acc: 0.9253
# Epoch 8/12
# 2849/2849 [==============================] - 9s 3ms/step - loss: 0.2049 - acc: 0.9365 - val_loss: 0.1385 - val_acc: 0.9611
# Epoch 9/12
# 2849/2849 [==============================] - 9s 3ms/step - loss: 0.1247 - acc: 0.9681 - val_loss: 0.1035 - val_acc: 0.9716
# Epoch 10/12
# 2849/2849 [==============================] - 9s 3ms/step - loss: 0.0877 - acc: 0.9821 - val_loss: 0.1079 - val_acc: 0.9579
# Epoch 11/12
# 2849/2849 [==============================] - 9s 3ms/step - loss: 0.0601 - acc: 0.9853 - val_loss: 0.0606 - val_acc: 0.9884
# Epoch 12/12
# 2849/2849 [==============================] - 9s 3ms/step - loss: 0.0427 - acc: 0.9937 - val_loss: 0.0800 - val_acc: 0.9747
# <keras.callbacks.History at 0x7f0626518898>

# Save the trained model to disk
model.save(MODEL_FILENAME)