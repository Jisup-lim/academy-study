# epoch 100
# validation_split, callback
# early_stopping 5
# Reduce LR 3
#  modelcheckpoint

import numpy as np
from tensorflow.keras import callbacks
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Dropout, Input
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, train_test_split
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from sklearn.datasets import load_boston

datasets = load_boston()
x = datasets.data
y = datasets.target

x_train, x_test, y_train,y_test = train_test_split(x, y, train_size = 0.8 , random_state = 104 )

#1. 데이터

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

#2 

# 함수형으로 만든 모델

def build_model(drop=0.5, optimizer='adam',activation1 = 'relu',activation2 = 'relu',activation3 = 'relu',a = 32,b=32,c=32):
    inputs = Input(shape=(13,), name='inputs')
    x = Dense(a,activation = activation1,name='hidden1')(inputs)
    x = Dropout(drop)(x)
    x = Dense(b,activation = activation2,name='hidden2')(x)
    x = Dropout(drop)(x)
    x = Dense(b,activation = activation2,name='hidden3')(x)
    x = Dropout(drop)(x)
    x = Dense(c,activation = activation3,name='hidden4')(x)
    x = Dropout(drop)(x)
    outputs = Dense(1,activation='relu',name='ouputs')(x)
    model = Model(inputs=inputs,outputs=outputs)
    model.compile(optimizer=optimizer,metrics=['mae'],loss='mse')
    return model

# 함수형으로 만든 하이퍼 파라미터

def  create_hyperparameters():
    batches = [4 ,8, 16]
    optimizers = ['rmsprop','adam','adadelta']
    dropout = [0.1, 0.2, 0.3, 0.4]
    activations = ['relu','tanh']
    nodes = [64, 128, 256]
    return {'batch_size' : batches, 'optimizer' : optimizers, 'drop': dropout,'activation1' : activations, 'activation2' : activations, 'activation3' : activations
            ,'a': nodes ,'b':nodes,'c':nodes} 
            

hyperparameters = create_hyperparameters()
model2 = build_model

from tensorflow.keras.wrappers.scikit_learn import KerasClassifier, KerasRegressor

# 여기서 epochs, validation, callback등 넣을수 있다
model2 = KerasRegressor(build_fn=build_model,verbose = 1)#,epochs= 3,validation_split = 0.2)


search = GridSearchCV(model2,hyperparameters,cv=3)

lr = ReduceLROnPlateau(monitor='val_loss',patience=25,factor=0.5,verbose=1) 
modelpath = '../Data/modelCheckPoint/k62_boston_{epoch:02d}-{val_loss:.4f}.hdf5' 
mc = ModelCheckpoint(filepath=modelpath,monitor='val_loss',save_best_only=True,mode='auto')
es = EarlyStopping(monitor='val_loss',patience=50,mode='auto')

# epochs, validation, callback등 fit에서도 먹힌다 (fit이 우선순위가 더 높다)
search.fit(x_train,y_train,verbose=1,epochs=100 ,validation_split= 0.2, callbacks=[mc,es,lr])

print(search.best_params_) 
print(search.best_estimator_)
print(search.best_score_) 

loss = search.score(x_test,y_test) 
print('loss : ', loss)

# {'optimizer': 'adam', 'drop': 0.4, 'batch_size': 20, 'activation': 'sigmoid'}
# <tensorflow.python.keras.wrappers.scikit_learn.KerasClassifier object at 0x000001D2DB370C40>
# 0.9788666566212972
# 500/500 [==============================] - 0s 892us/step - loss: 0.0707 - acc: 0.9841
# acc :  0.9840999841
