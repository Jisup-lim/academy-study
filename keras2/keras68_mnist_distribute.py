# GPU의 분산처리

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
from tensorflow.keras.callbacks import EarlyStopping

(x_train, y_train), (x_test,  y_test) = mnist.load_data()


x_train = x_train.reshape(60000, 28, 28, 1).astype('float32')/255.
x_test = x_test.reshape(10000, 28, 28, 1).astype('float32')/255.


from tensorflow.keras.utils import to_categorical

y_test = to_categorical(y_test)
y_train = to_categorical(y_train)




# 2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D,Flatten, Dropout

import tensorflow as tf

strategy = tf.distribute.MirroredStrategy(cross_device_ops=\
    tf.distribute.HierarchicalCopyAllReduce()
    )
with strategy.scope():
    model = Sequential()
    model.add(Conv2D(128, (2,2),padding='same', strides=2, activation='relu', input_shape=(28,28,1)))
    model.add(MaxPooling2D(pool_size=2))
    model.add(Conv2D(128, (2,2),padding='same', strides=1))
    model.add(MaxPooling2D(pool_size=1))
    model.add(Conv2D(128, (2,2)))
    model.add(Conv2D(128, (2,2)))
    model.add(Flatten())
    model.add(Dense(128))
    model.add(Dropout(0.4))
    model.add(Dense(64))
    model.add(Dropout(0.2))
    model.add(Dense(64,activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(10,activation='softmax'))
    model.summary()

    #3

    model.compile(loss='categorical_crossentropy',optimizer='adam',metrics='acc')

early_stopping = EarlyStopping(monitor='val_loss',patience=5,mode='auto')
hist = model.fit(x_train, y_train, epochs=50,batch_size=16,validation_split=0.2,verbose=1,callbacks=[early_stopping])

#4
loss = model.evaluate(x_test,y_test)
print(loss[0])
print(loss[1])

