# Classifier = 분류 EX) model = ~~~~~~Classifier


import numpy as np
import sklearn
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from sklearn.metrics import accuracy_score

from sklearn.svm import LinearSVC, SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# 1 데이터

dataset = load_wine()
x = dataset.data
y = dataset.target

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, random_state=104)

scaler = MinMaxScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)



#2 모델 구성

# model = LinearSVC()
# model = SVC()
# model = KNeighborsClassifier()
# model = DecisionTreeClassifier()
# model = RandomForestClassifier()
model = LogisticRegression()

#3 훈현

model.fit(x_train, y_train)

#4 평가 예측


y_pred = model.predict(x_test)
# print(x_test,"'s result : ",y_pred)


result = model.score(x_test, y_test)
print('modle_socore : ',result)

acc = accuracy_score(y_test,y_pred)
print('accuracy_score : ',acc)

# =====LinearSVC=====
# modle_socore :  0.9722222222222222
# accuracy_score :  0.9722222222222222

# =====SVC=====
# modle_socore :  0.9444444444444444
# accuracy_score :  0.9444444444444444

# =====KNeighborsClassifier=====
# modle_socore :  0.9166666666666666
# accuracy_score :  0.9166666666666666

# =====DecisionTreeClassifier=====
# modle_socore :  0.8611111111111112
# accuracy_score :  0.8611111111111112

# ======RandomForestClassifier=====
# modle_socore :  0.9444444444444444
# accuracy_score :  0.9444444444444444

# =====LogisticRegression=====
# modle_socore :  0.9166666666666666
# accuracy_score :  0.9166666666666666

# =====Tensorflow=====
# [1.0]
