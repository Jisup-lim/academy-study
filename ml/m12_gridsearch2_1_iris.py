from inspect import Parameter
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV # Gridserch 모델셀렉션에 있다
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from sklearn.metrics import accuracy_score
# from sklearn.svm import LinearSVC, SVC

# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
# from sklearn.linear_model import LogisticRegression
import warnings
import datetime
warnings.filterwarnings('ignore')

# 1 데이터

dataset = load_iris()
x = dataset.data
y = dataset.target

x_train , x_test,y_train ,y_test = train_test_split( x, y, train_size = 0.8, random_state=104)

KFold = KFold(n_splits=5,shuffle=True) # (shuffle=False : 순차적)


Parameters = [
    {'n_estimators':[100,200],'max_depth' : [10,12],'n_jobs' : [-1]},
    {'n_estimators':[100,200],'max_depth' : [6,8,10,12]},
    {'min_samples_leaf' : [3,5,7,10],'min_samples_split': [3,5]},
    {'n_estimators':[100,200],'min_samples_split': [2,3,5,10]},
    {'min_samples_leaf' : [3,5,7,10],'n_jobs' : [-1,2,3]}
    # ,{'n_estimators':[100,200],'max_depth' : [6,8,10,12],'min_samples_leaf' : [3,5,7,10],'min_samples_split': [2,3,5,10],'n_jobs' : [-1,2,3]}
]

#2 모델 구성

# model = SVC()

model = GridSearchCV(RandomForestClassifier(), Parameters, cv = KFold  ) 
# GridSearchCV 뒤에 모델(SVC)을  파라미터에 (감싸서) 맞춰서 돌린다 (파라미터 18 * kfold 횟수 5) 즉 총 90번이 돌아갔다.

#3 훈련
start_time = datetime.datetime.now()

model.fit(x_train, y_train)
end_time = datetime.datetime.now()
#4 평가 예측

print('최적의 매개변수 : ', model.best_estimator_) # model.best_estimator_ : 어떤것이 가장 좋은것(매개변수)인지 나온다 

y_pred = model.predict(x_test)
print("최종정답률 : ",accuracy_score(y_test,y_pred))

print("최종정답률 : ", model.score(x_test,y_test)) # GridSearchCV 가 모델자체가 된다



print('걸린시간 : ', end_time - start_time)
# 최적의 매개변수 :  RandomForestClassifier(max_depth=10, n_jobs=-1)
# 최종정답률 :  1.0
# 최종정답률 :  1.0

# import datetime


