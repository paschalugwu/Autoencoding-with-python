# -*- coding: utf-8 -*-
"""Autoencoders

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e5LpS0-LXNx-uhwgcFY81xltrP287AVn

#Autoencoders
Autoencoders consist of 
1) Encoder: that extracts features
2) Decoder: that generates imaages from knowledge
This is for the reasons of generating more data for "fake detection and training", "denoising", "dimensional reduction", "image compression", and "recommendation systems".
"""

import tensorflow as tf
import keras
from keras import layers
from keras.datasets import mnist
import numpy as np
import matplotlib.pyplot as plt

#Download datasets
(x_train, _), (x_test, _) = mnist.load_data()

x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = np.reshape(x_train, (len(x_train), 28, 28, 1))
x_test = np.reshape(x_test, (len(x_test), 28, 28, 1))

#Create noisy examples
noise_factor = 0.5
x_train_noisy = x_train + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_train.shape) 
x_test_noisy = x_test + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_test.shape) 

x_train_noisy = np.clip(x_train_noisy, 0., 1.)
x_test_noisy = np.clip(x_test_noisy, 0., 1.)

#Display noisy images
sampleTestImages = [34, 376, 50, 70, 90, 110, 130, 150, 170, 220]
fig, figPlacement = plt.subplots(1, len(sampleTestImages))
fig.set_size_inches(20, 10)
examples = list(zip(sampleTestImages, figPlacement))
print('Shape of image is ', x_test[sampleTestImages[0]].shape)
for example in examples:
  example[1].imshow(tf.squeeze(x_test_noisy[example[0]], 2), cmap='gray')

#Create model
input_img = keras.Input(shape=(28, 28, 1))

x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)
x = layers.MaxPooling2D((2, 2), padding='same')(x)
x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(x)
encoded = layers.MaxPooling2D((2, 2), padding='same')(x)

x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(encoded)
up1 = layers.UpSampling2D((2, 2))(x)
x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(up1)
up2 = layers.UpSampling2D((2, 2))(x)
decoded = layers.Conv2D(1, (3, 3), activation='sigmoid', padding='same')(up2)

autoencoder = keras.Model(input_img, decoded)
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

#Train model
#NOTE: An epoch is when all the training data is used at once and is defined as the total number of iterations of all the training data in one cycle for training the machine learning model. Another way to define an epoch is the number of passes a training dataset takes around an algorithm.
autoencoder.fit(x_train_noisy, x_train,
                epochs=2,
                batch_size=128,
                shuffle=True,
                validation_data=(x_test_noisy, x_test))

#Display encoding examples
encoder = keras.Model(input_img, encoded)
encoded_imgs = encoder.predict(x_test_noisy)

sampleTestImages = [34, 376, 50, 70, 90, 110, 130, 150, 170, 220]
fig, figPlacement = plt.subplots(1, len(sampleTestImages))
fig.set_size_inches(20, 10)
examples = list(zip(sampleTestImages, figPlacement))
for example in examples:
  example[1].imshow(encoded_imgs[example[0], :, :, 0:5].reshape((7, 35)).T, cmap='gray')

#Display first level examples of decompression process
up1Model = keras.Model(input_img, up1)
up1_imgs = up1Model.predict(x_test_noisy)

sampleTestImages = [34, 376, 50, 70, 90, 110, 130, 150, 170, 220]
fig, figPlacement = plt.subplots(1, len(sampleTestImages))
fig.set_size_inches(20, 10)
examples = list(zip(sampleTestImages, figPlacement))
for example in examples:
  example[1].imshow(up1_imgs[example[0], :, :, 5].reshape((14, 14)), cmap='gray')

#Display second level examples of decompression process
up2Model = keras.Model(input_img, up2)
up2_imgs = up2Model.predict(x_test_noisy)

sampleTestImages = [34, 376, 50, 70, 90, 110, 130, 150, 170, 220]
fig, figPlacement = plt.subplots(1, len(sampleTestImages))
fig.set_size_inches(20, 10)
examples = list(zip(sampleTestImages, figPlacement))
for example in examples:
  example[1].imshow(up2_imgs[example[0], :, :, 20].reshape((28, 28)), cmap='gray')

#Display decoded examples
decoded_imgs = autoencoder.predict(x_test_noisy)

sampleTestImages = [34, 376, 50, 70, 90, 110, 130, 150, 170, 220]
fig, figPlacement = plt.subplots(1, len(sampleTestImages))
fig.set_size_inches(20, 10)
examples = list(zip(sampleTestImages, figPlacement))
for example in examples:
  example[1].imshow(decoded_imgs[example[0]].reshape((28, 28)), cmap='gray')

#Compare noisy images to denoised versions
decoded_imgs = autoencoder.predict(x_test_noisy)

sampleTestImages = [34, 376, 50, 70, 90, 110, 130, 150, 170, 220]
fig, figPlacement = plt.subplots(1, len(sampleTestImages))
fig.set_size_inches(20, 10)
examples = list(zip(sampleTestImages, figPlacement))
for example in examples:
  example[1].imshow(tf.squeeze(x_test_noisy[example[0]], 2), cmap='gray')

fig, figPlacement = plt.subplots(1, len(sampleTestImages))
fig.set_size_inches(20, 10)
examples = list(zip(sampleTestImages, figPlacement))
for example in examples:
  example[1].imshow(decoded_imgs[example[0]].reshape((28, 28)), cmap='gray')