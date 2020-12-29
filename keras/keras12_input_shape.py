import numpy as np
#1 데이터
x = np.array([range(100),range(301,401),range(1,101),range(501,601),range(801,901)])
y = np.array([range(711, 811), range(1,101)])
print(x.shape) # (5, 100)
print(y.shape) # (2, 100)

x_pred2 = np.array([100, 401, 101, 601, 901])
# x_pred2 = np.transpose(x_pred2)
print('x_pres2.shape : ', x_pred2.shape)
x_pred2 = x_pred2.reshape(1, 5) 
print('x_pres2.shape : ', x_pred2.shape) 

x = np.transpose(x)
y = np.transpose(y)
print(x.shape) #(100, 5)
print(y.shape) #(100, 2)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, random_state=66)

print(x_train.shape) # (80,5)
print(y_train.shape) # (80,2)

#2 모델구성
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential()
# model.add(Dense(10, input_dim=5)) 
model.add(Dense(10, input_shape=(5,))) 
# input_shape = 맨앞의 행을 뺀 나머지를 쓰면 된다 다차원에서 사용할때 사용
model.add(Dense(5))
model.add(Dense(5))
model.add(Dense(5))
model.add(Dense(2)) 

#3 컴파일 훈련
model.compile(loss='mse', optimizer='adam', metrics=['mae'])
model.fit(x_train,y_train, epochs=100, batch_size=1, validation_split=0.2, verbose=0)

#4 평가 예측
loss,mae = model.evaluate(x_test, y_test)
print('loss : ',loss)
print('mae : ', mae)

y_predict = model.predict(x_test) 
print(y_predict)



from sklearn.metrics import mean_squared_error
def RMSE(y_test, y_predict):
    return np.sqrt(mean_squared_error(y_test, y_predict))
print('RMSE : ', RMSE(y_test, y_predict ))

from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_predict)
print('R2: ', r2)

y_pred2 = model.predict(x_pred2) #새로운 predict를 사용해도 된다
print(y_pred2)
