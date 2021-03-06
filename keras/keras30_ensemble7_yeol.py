# 열이 다른 모델 (가능)

import numpy as np
from numpy import array
from sklearn.model_selection import train_test_split

#1

x1 = array([[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,10],[10,11],[20,30],[30,40],[40,50]])
x2 = array([[10,20,30],[20,30,40],[30,40,50],[40,50,60],[50,60,70],[60,70,80],[70,80,90],[80,90,100],[90,100,110],[100,110,120],[2,3,4],[3,4,5],[4,5,6]])
y1 = array([[10,20,30],[20,30,40],[30,40,50],[40,50,60],[50,60,70],[60,70,80],[70,80,90],[80,90,100],[90,100,110],[100,110,120],[2,3,4],[3,4,5],[4,5,6]])
y2 = array([4,5,6,7,8,9,10,11,12,13,50,60,70])


x1_predict = array([55,65])
x2_predict = array([65,75,85])

print(x1.shape) # (13,2)
print(x2.shape) # (13,3)
print(y1.shape) # (13,3)
print(y2.shape) # (13, )

x1 = x1.reshape(-1, 2, 1)
x2 = x2.reshape(13, 3, 1)
y1 = y1.reshape(13, -1)
y2 = y2.reshape(-1, 1)

print(x1.shape) # (13,2)
print(x2.shape) # (13,3)
print(y1.shape) # (13,3)
print(y2.shape) # (13, )

# x1_train, x1_test, x2_train, x2_test = train_test_split(x1, x2, train_size=0.8, random_state=104)
x1_train, x1_test, y1_train, y1_test = train_test_split(x1, y1, train_size=0.8, random_state=104)

# y1_train, y1_test, y2_train, y2_test = train_test_split(y1, y2, train_size=0.8, random_state=104)
x2_train, x2_test, y2_train, y2_test = train_test_split(x2, y2, train_size=0.8, random_state=104)

# x1_train, x1_val, x2_train, x2_val, y_train, y_val = train_test_split(x1_train, x2_train, y_train, train_size=0.8, random_state=104)

# 3차원일때  MinMaxScaler를 사용할수 없기떄문에 2차원으로 만들고 스케일링후 다시 3차원으로 만든다음에 돌린다

# from sklearn.preprocessing import MinMaxScaler

# x1_predict = x1_predict.reshape(-1, 3)
# x2_predict = x2_predict.reshape(-1, 3)


# scaler = MinMaxScaler()
# scaler.fit(x1_train)
# x1_train = scaler.transform(x1_train)
# x1_test = scaler.transform(x1_test)
# x1_predict = scaler.transform(x1_predict)

# scaler.fit(x2_train)
# x2_train = scaler.transform(x2_train)
# x2_test = scaler.transform(x2_test)
# x2_predict = scaler.transform(x2_predict)

# # print(x_train.shape) #(9, 3)
# # print(x_test.shape) #(4,3)

# # x = x.reshape(x.shape[0], x.shape[1], 1)
# x1_train = x1_train.reshape(-1, 3, 1)
# x1_test = x1_test.reshape(-1, 3, 1)

# x2_train = x2_train.reshape(-1, 3, 1)
# x2_test = x2_test.reshape(-1, 3, 1)


#2 
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Input, LSTM, concatenate

input1 = Input(shape=(2,1))
LSTM1 = LSTM(356, activation='relu')(input1)
dence1 = Dense(356)(LSTM1)
dence1 = Dense(128)(dence1)
dence1 = Dense(128)(dence1)
dence1 = Dense(128)(dence1)

input2 = Input(shape=(3,1))
LSTM2 = LSTM(356,activation='relu')(input2)
dence4 = Dense(128)(LSTM2)
dence5 = Dense(128)(dence4)


merge1 = concatenate([dence1, dence5])
middlel1 = Dense(64)(merge1)
middlel2 = Dense(64)(middlel1)
middlel3 = Dense(64)(middlel1)

output1 = Dense(64)(middlel1)
output1 = Dense(32)(output1)
output1 = Dense(3)(output1)

output2 = Dense(64)(middlel1)
output2 = Dense(32)(output2)
output2 = Dense(1)(output2)

model = Model(inputs = [input1, input2], outputs = [output1,output2])

# model.summary()

#3
model.compile(loss='mse', optimizer='adam', metrics=['mae'])
model.fit([x1_train, x2_train], [y1_train,y2_train],epochs=190, batch_size=1, validation_steps=0.2, verbose=1)

#4
loss=model.evaluate([x1_test,x2_test],[y1_test,y2_test], batch_size=1)
print(loss)


# print(x2_predict.shape) # 
# print(x1_predict.shape) # 

x1_predict = x1_predict.reshape(1, 2, 1)
x2_predict = x2_predict.reshape(1, 3, 1)

y_pred = model.predict([x1_predict,x2_predict])


print(y_pred)

# [423.3583068847656, 0.3187046945095062, 423.0396423339844, 0.4329011142253876, 16.127267837524414]
# [array([[76.13658, 77.89354, 80.39232]], dtype=float32), array([[137.19846]], dtype=float32)]     

# np.dtype('int32') : 32비트 LE 정수, np.int32와 동일 . floating points 32 : 부동소수형 참고함 (https://wikidocs.net/33275) , (https://kongdols-room.tistory.com/53)

