#!/usr/bin/env python3

from lenet import LeNet
from sklearn.cross_validation import train_test_split
from sklearn import datasets
from keras.optimizers import SGD
from keras.utils import np_utils
import numpy as np
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--save-model", type=int, default=-1,
                help="(optional) save the model to disk")
ap.add_argument("-l", "--load-model", type=int, default=-1,
                help="(optional) load the pre-trained model from disk")
ap.add_argument("-w", "--weights", type=str,
                help="(optional) path to weights file")
args = vars(ap.parse_args())

# grab the MNIST dataset
print("[INFO] downloading MNIST...")
dataset = datasets.fetch_mldata("MNIST Original")

# reshape the MNIST dataset from a flat list of 784-dim vectors, to
# 28x28 pixel image, then scale the data to the range [0, 1.0]
# and construct the training and testing splits
data = dataset.data.reshape((dataset.data.shape[0], 28,28))
data = data[: np.newaxis, :, :]
(trainData, testData, trainLabels, testLabels) = train_test_split(
    data/255.0, dataset.target.astype("int"), test_size=0.33)

# transform the training and testing labels in to vectors in the range [0, classes]
# this generates a vector for each label, where the index of the label is set to 
# '1' and all other entries to '0'; in the case of MNIST, there are 10 class labels
trainLabels = np_utils.to_categorical(trainLabels, 10)
testLabels = np_utils.to_categorical(testLabels, 10)

# init the optimizer and model
print("[INFO] compiling model...")
opt = SGD(lr=0.01)
model = LeNet.build(width=28, height=28, depth=1, classes=10, 
                    weightsPath=args["weights"] if args["load_model"] > 0 else None)
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

# only train and evaluate the model if we *are not* loading a pre-existing model
if args["load_model"] < 0:
    print("[INFO] training...")
    model.fit(trainData, trainLabels, batch_size=128, nb_epoch=20, verbose=1)
    # show the accuracy on the testing set
    print("[INFO] evaluating...")
    (loss, accuracy) = model.evaluate(testData, testLabels, batch_size=128, verbose=1)
    print("[INFO] accuracy: {:.2f}%".format(accuracy*100))

# check to see if the model should be saved to file
if args["save_model"] > 0:
    print("[INFO] dumping weights to file...")
    model.save_weights(args["weights"], overwrite=True)
    
# randomly select a few testing digits
for i in np.random.choice(np.arange(0, len(testLabels)), size=(10,)):
    # classify the digit
    probs = model.predict(testData[np.newaxis, i])
    prediction = probs.argmax(axis=1)
    # resize the image from 28x28 to 96x96 so we can see it better
    image = (testData[i][0]*255).astype("uint8")
    image = cv2.merge(image*3)
    image = cv2.resize(image, (96,96), interpolation=cv2.INTER_LINEAR)
    cv2.putText(image, str(prediction[0]), (5,20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2)
    
    #show the image and prediciton
    print("[INFO] Predicted: {}, Actual: {}".format(prediction[0],
            np.argmax(testLabels[i])))
    cv2.imshow("Digit", image)
    cv2.waitKey(0)
    
