# Regressor = 회귀모델 EX) model = ~~~~~~Regressor 단 LogisticRegression는 분류모델


import numpy as np
from sklearn.datasets import load_diabetes
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from sklearn.metrics import accuracy_score, r2_score

from sklearn.svm import LinearSVC, SVC,LinearSVR,SVR
from sklearn.neighbors import KNeighborsClassifier,KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier,RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression

dataset = load_diabetes()
x = dataset.data
y = dataset.target

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, random_state=104)

scaler = MinMaxScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)



#2 모델 구성

# model = LinearRegression()
# model = KNeighborsRegressor()
model = DecisionTreeRegressor()
# model = RandomForestRegressor()

#3 훈현

model.fit(x_train, y_train)

#4 평가 예측


y_pred = model.predict(x_test)
# print(x_test,"'s result : ",y_pred)


result = model.score(x_test, y_test)
print('modle_socore : ',result)

r2 = r2_score(y_test,y_pred)
print('r2_score : ',r2)

# =====LinearRegression=====

# modle_socore :  0.5620438671817145
# r2_score :  0.5620438671817145

# =====KNeighborsRegressor=====

# modle_socore :  0.49669170779211047
# r2_score :  0.49669170779211047

# =====DecisionTreeRegressor=====

# modle_socore :  0.051320777111981575
# r2_score :  0.051320777111981575

# =====RandomForestRegressor=====

# modle_socore :  0.5260507700261986
# r2_score :  0.5260507700261986

# =====Tensorflow=====
# R2:  0.5755343121533955