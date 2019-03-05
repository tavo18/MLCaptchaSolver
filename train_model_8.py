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

LETTER_IMAGES_FOLDER = "/content/MLCaptchaSolver/dataset/examples8v2"
MODEL_FILENAME = "captcha_model_8.hdf5"
MODEL_LABELS_FILENAME = "model_labels_8.dat"

# initialize the data and labels
data = []
labels = []

# loop over the input images
for image_file in paths.list_images(LETTER_IMAGES_FOLDER):
    # Load the image and convert it to grayscale
    image = cv2.imread(image_file)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Resize the letter so it fits in a 20x20 pixel box
    #image = resize_to_fit(image, 20, 20)

    # Add a third channel dimension to the image to make Keras happy
    # image = np.expand_dims(image, axis=2)

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
model.add(Conv2D(20, (5, 5), padding="same", input_shape=(31, 26, 1), activation="relu"))
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
model.fit(X_train, Y_train, validation_data=(X_test, Y_test), batch_size=32, epochs=10, verbose=1)

# Train on 5998 samples, validate on 2000 samples
# Epoch 1/10
# 5998/5998 [==============================] - 20s 3ms/step - loss: 2.8304 - acc: 0.2321 - val_loss: 0.7964 - val_acc: 0.7420
# Epoch 2/10
# 5998/5998 [==============================] - 19s 3ms/step - loss: 0.3400 - acc: 0.8961 - val_loss: 0.1439 - val_acc: 0.9590
# Epoch 3/10
# 5998/5998 [==============================] - 19s 3ms/step - loss: 0.1107 - acc: 0.9653 - val_loss: 0.0626 - val_acc: 0.9880
# Epoch 4/10
# 5998/5998 [==============================] - 19s 3ms/step - loss: 0.0613 - acc: 0.9823 - val_loss: 0.0479 - val_acc: 0.9795
# Epoch 5/10
# 5998/5998 [==============================] - 19s 3ms/step - loss: 0.0358 - acc: 0.9915 - val_loss: 0.0371 - val_acc: 0.9870
# Epoch 6/10
# 5998/5998 [==============================] - 19s 3ms/step - loss: 0.0249 - acc: 0.9950 - val_loss: 0.0152 - val_acc: 0.9970
# Epoch 7/10
# 5998/5998 [==============================] - 19s 3ms/step - loss: 0.0177 - acc: 0.9977 - val_loss: 0.0120 - val_acc: 0.9970
# Epoch 8/10
# 5998/5998 [==============================] - 19s 3ms/step - loss: 0.0180 - acc: 0.9955 - val_loss: 0.0320 - val_acc: 0.9880
# Epoch 9/10
# 5998/5998 [==============================] - 19s 3ms/step - loss: 0.0303 - acc: 0.9930 - val_loss: 0.0085 - val_acc: 0.9980
# Epoch 10/10
# 5998/5998 [==============================] - 19s 3ms/step - loss: 0.0170 - acc: 0.9965 - val_loss: 0.0120 - val_acc: 0.9965
# <keras.callbacks.History at 0x7fb4f4f79dd8>

# Save the trained model to disk
model.save(MODEL_FILENAME)