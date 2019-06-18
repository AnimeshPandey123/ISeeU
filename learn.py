# Convolutional Neural Network
# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import keras as keras
from keras.preprocessing import image
from keras.models import load_model
# Installing Theano
# pip install --upgrade --no-deps git+git://github.com/Theano/Theano.git

# Installing Tensorflow
# pip install tensorflow

# Installing Keras
# pip install --upgrade keras


class TrainModel():
    """docstring for ClassName"""
    classifier = Sequential()

    def train(self):
        self.classifier = Sequential()

        # Step 1 - Convolution
        self.classifier.add(
            Conv2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'))

        # Step 2 - Pooling
        self.classifier.add(MaxPooling2D(pool_size=(2, 2)))

        # Adding a second convolutional layer
        self.classifier.add(Conv2D(32, (3, 3), activation='relu'))
        self.classifier.add(MaxPooling2D(pool_size=(2, 2)))

        # Step 3 - Flattening
        self.classifier.add(Flatten())

        # Step 4 - Full connection
        self.classifier.add(Dense(units=128, activation='relu'))
        self.classifier.add(Dense(units=1, activation='sigmoid'))

        # Compiling the CNN
        self.classifier.compile(
            optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        return self.classifier

    def withImage(self):
        train_datagen = ImageDataGenerator(rescale=1. / 255,
                                           shear_range=0.2,
                                           zoom_range=0.2,
                                           horizontal_flip=True)

        test_datagen = ImageDataGenerator(rescale=1. / 255)

        training_set = train_datagen.flow_from_directory('dataset/training_set',
                                                         target_size=(64, 64),
                                                         batch_size=32,
                                                         class_mode='binary')

        test_set = test_datagen.flow_from_directory('dataset/test_set',
                                                    target_size=(64, 64),
                                                    batch_size=32,
                                                    class_mode='binary')
        self.classifier.fit_generator(training_set,
                                      steps_per_epoch=50,
                                      epochs=25,
                                      validation_data=test_set,
                                      validation_steps=500,
                                      callbacks=[AfterEpoch()]
                                      )
        return self.classifier

    def predictImage(self, path):
        test_image = image.load_img(path, target_size=(64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = self.classifier.predict(test_image)
        resultProb = self.classifier.predict_proba(test_image)
        # training_set.class_indices
        # print(result)
        # return result

        if result[0][0] == 1:
            prediction = 'dog'
        else:
            prediction = 'cat'
        return prediction

    def saveModel(self):
        self.classifier.save('newer.h5')
        return self.classifier

    def loadModel(self):
        keras.backend.clear_session()
        self.classifier = None
        self.classifier = load_model('newer.h5')
        return self.classifier


class AfterEpoch(keras.callbacks.Callback):

    def on_epoch_end(self, epoch, logs={}):
        with open('log.txt', 'a+') as f:
            f.write('%02d %.3f\n' % (epoch, logs['loss']))
