import numpy as np
from tensorflow.keras.datasets import mnist

(x_train, _), (x_test, _) = mnist.load_data()

x_train = x_train.reshape(60000, 28,28,1).astype('float32')/255
x_test = x_test.reshape(10000, 28,28,1)/255.

print(x_train.shape,x_test.shape)

# 노이즈 추가
x_train_noised = x_train + np.random.normal(0, 0.1, size = x_train.shape)
x_test_noised = x_test + np.random.normal(0, 0.1, size = x_test.shape)
x_train_noised = np.clip(x_train_noised, a_min = 0, a_max = 1)
x_test_noised = np.clip(x_test_noised, a_min = 0, a_max = 1)

from tensorflow.keras.models import Sequential,Model
from tensorflow.keras.layers import Dense,Conv2D,Conv2DTranspose,BatchNormalization

def autoencoder(hidden_layer_size) :
    model = Sequential()
    model.add((Conv2D(filters=256,kernel_size=1,input_shape = (28,28,1),activation='relu')))
    model.add(BatchNormalization())
    model.add(Conv2D(filters=128,kernel_size=2,activation='relu'))
    model.add(BatchNormalization())
    model.add(Conv2D(filters=64,kernel_size=2,activation='relu'))
    model.add(Conv2D(filters=32,kernel_size=2,activation='relu'))
    model.add(Dense(units=16,activation='relu'))          
    model.add(Dense(units=hidden_layer_size,activation='relu'))   
    # model.add(Flatten())
    model.add(Dense(units=16,activation='relu'))
    model.add(Dense(units=32,activation='relu'))
    model.add(Conv2DTranspose(filters=64,kernel_size=2,activation='relu'))
    model.add(BatchNormalization())
    model.add(Conv2DTranspose(filters=128,kernel_size=2,activation='relu'))
    model.add(BatchNormalization())
    model.add(Conv2DTranspose(filters=256,kernel_size=2,activation='relu'))             
    model.add(Dense(units=1,activation='sigmoid'))
    return model

model = autoencoder(hidden_layer_size=8)

model.summary()

model.compile(optimizer='adam',loss='binary_crossentropy', metrics=['acc'])
model.fit(x_train,x_train_noised,epochs = 10)

output = model.predict(x_test_noised)

from matplotlib import pyplot as plt
import random

fig, ((ax1,ax2,ax3,ax4,ax5),(ax6,ax7,ax8,ax9,ax10),(ax11,ax12,ax13,ax14,ax15)) = plt.subplots(3,5,figsize=(20,7))

random_imeges = random.sample(range(output.shape[0]),5)

for i, ax in enumerate([ax1,ax2,ax3,ax4,ax5]):
    ax.imshow(x_test[random_imeges[i]].reshape(28,28),cmap = 'gray')
    if i ==0:
        ax.set_ylabel('INPUT', size = 20)
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])

for i, ax in enumerate([ax6,ax7,ax8,ax9,ax10]):
    ax.imshow(x_test_noised[random_imeges[i]].reshape(28,28),cmap = 'gray')
    if i ==0:
        ax.set_ylabel('NOISED', size = 20)
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])


for i, ax in enumerate([ax11,ax12,ax13,ax14,ax15]):
    ax.imshow(output[random_imeges[i]].reshape(28,28),cmap = 'gray')
    if i ==0:
        ax.set_ylabel('OUTPUT', size = 20)
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])

plt.tight_layout()
plt.show()