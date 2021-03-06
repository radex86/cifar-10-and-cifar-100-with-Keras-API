# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qmLfMro7BEi6EwY0jPQz0GDcB6PeZfO9
"""

#CFIR10 dataset 
# ------------------------------packages----------------------------------------
# Importing the Important pakages
import tensorflow as tf 
from tensorflow.keras.datasets import mnist, fashion_mnist, cifar10,cifar100 
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, Flatten, Input
from tensorflow.keras.layers import Conv2D, MaxPool2D, BatchNormalization, GlobalMaxPooling2D
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing.image import ImageDataGenerator


# importing the support packages
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

#-------------------------------Preprocessing-----------------------------------
#Loading the data 
(X_trx, y_trx),(X_tsx, y_tsx) = cifar10.load_data()

print(X_trx.shape, ":" ,y_trx.shape)

#Preview a sample
plt.imshow(X_trx[0])


#Normalizing the data
X_trx, X_tsx = X_trx/255.0, X_tsx/255.0

plt.imshow(X_tsx[0])

K=len(list(set(np.squeeze(y_trx).astype(np.int32))))

#Reduce the deminsionality of y_trx and y_tsx
y_trx = np.squeeze(y_trx)
y_tsx = np.squeeze(y_tsx)


#Improving with data augmentation
batch_size=32
data_gen = ImageDataGenerator(height_shift_range=0.1,width_shift_range=0.2,horizontal_flip=True, vertical_flip=True)

trx_gen = data_gen.flow(X_trx, y_trx, batch_size)
step_per_epochs=  X_trx.shape[0] // batch_size


#---------------------------------Buliding the Model---------------------------- 

# First Layer
i=Input(shape=X_trx[0].shape)
x=Conv2D(32,kernel_size= (3,3),activation='relu', padding='same')(i)
x=BatchNormalization()(x)
x=Conv2D(32,kernel_size= (3,3),activation='relu', padding='same')(i)
x=BatchNormalization()(x)
x=MaxPool2D(pool_size=(2,2))(x)

# Second Layer
x=Conv2D(64, kernel_size=(3,3),activation='relu', padding='same')(x)
x=BatchNormalization()(x)
x=Conv2D(64, kernel_size=(3,3),activation='relu', padding='same')(x)
x=BatchNormalization()(x)
x=MaxPool2D(pool_size=(2,2))(x)

# Third Layer
x=Conv2D(128, kernel_size=(3,3),activation='relu', padding='same')(x)
x=BatchNormalization()(x)
x=Conv2D(128, kernel_size=(3,3),activation='relu', padding='same')(x)
x=BatchNormalization()(x)
x=MaxPool2D(pool_size=(2,2))(x)

#FDD Layers
x=Flatten()(x)
x=Dense(1024, activation='relu')(x)
x=Dropout(0.5)(x)

#output Layer
x=Dense(K, activation='softmax')(x)
model = Model(i,x)

model.summary()

# executing the Model
model.compile(loss='sparse_categorical_crossentropy',optimizer='Nadam', metrics='accuracy')

# adding callbaks
callback = EarlyStopping(monitor='loss', patience=3)

model.fit(trx_gen,validation_data=(X_tsx,y_tsx), steps_per_epoch=step_per_epochs, epochs=50, callbacks=[callback])

r = model.history.history
r.keys()

# get the Predictions and accuracy 
pred = model.predict(X_tsx).argmax(axis=1)
acc = sum(pred == y_tsx)/len(pred)
print (f" cifar-10 Testing Accuracy: {acc}")

#ploting the accuracy
plt.plot(r['accuracy'], label= 'accuracy')
plt.plot(r['val_accuracy'], label='val_accuracy')
plt.legend()

plt.plot(r['accuracy'], label= 'accuracy')
plt.plot(r['val_accuracy'], label='val_accuracy')
plt.legend()









