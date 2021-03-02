from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Sequential

vgg16 = VGG16(weights='imagenet', include_top=False, input_shape=(32, 32, 3))

print(vgg16.weights)


vgg16.trainable = False
vgg16.summary()
print(len(vgg16.weights)) # 26
print(len(vgg16.trainable_weights)) # 0

model = Sequential()
model.add(vgg16)
model.add(Flatten())
model.add(Dense(10))
model.add(Dense(5))
model.add(Dense(1))#, activation='softmax'))

model.summary()

print("가중치의 수 : ", len(model.weights)) # 26 -> 32
print("동결된 후 훈련되는 가중치의 수 : ", len(model.trainable_weights)) # 0 -> 6

import pandas as pd

pd.set_option('max_colwidth',-1)
layers = [(layer,layer.name, layer.trainable) for layer in model.layers] 
aaa = pd.DataFrame(layers, columns= ['Layer Type', 'Layer name', 'Layer Trainable'])
print(aaa)