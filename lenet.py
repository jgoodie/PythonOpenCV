#!/usr/bin/env python3
from keras.models import Sequential
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dense

class LeNet:
    @staticmethod
    def build(width, height, depth, classes, weightsPath=None):
        # init the model
        model = Sequential()
        # first set of CONV => RELU => POOL
        # the CONV layer will learn 20 convolution filters each of size 5x5
        # Since MNIST is 28x28 and black/white(gray) height is 28 width is 28 and depth is 1 (gray)
        #model.add(Convolution2D(20,5,5,border_mode="same",input_shape=(depth, height, width)))
        model.add(Conv2D(20,(5,5),input_shape=(depth, height, width), padding="same"))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
        # 2nd CONV => RELU => POOL
        # CONV is now 50. It's common to see the number of CONV filters increase in 
        # deeper layers of the network
        model.add(Convolution2D(50,5,5,border_mode="same"))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
        # Fully-connected layers or dense layers of the LeNet
        # set of FC => RELU layers
        model.add(Flatten())
        model.add(Dense(500))
        model.add(Activation("relu"))
        # softmax classifier
        model.add(Dense(classes))
        model.add(Activation("softmax"))
        # if a weights path is supplied (indicating that the model was
        # pre-trained, then load the weights
        if weightsPath is not None:
            model.load_weights(weightsPath)
        # return the constructed network architecture
        return(model)
    
