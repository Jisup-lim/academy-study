from sys import platform
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier , GradientBoostingClassifier
from sklearn.model_selection import train_test_split, KFold,cross_val_score,GridSearchCV,RandomizedSearchCV
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier,plot_importance
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings

from xgboost.sklearn import XGBRegressor
warnings.filterwarnings('ignore')

# 1 데이터

dataset = load_diabetes()
x = dataset.data
y = dataset.target

x_train , x_test,y_train ,y_test = train_test_split( x, y, train_size = 0.8, random_state=104)

KFold = KFold(n_splits=5,shuffle=True) # (shuffle=False : 순차적)
st = datetime.datetime.now()

parameters = [
    {'n_estimoters':[100,200,300], 'learning_rate':[0.1,0.3,0.001,0.01], 'max_depth':[4,5,6]},
    {'n_estimoters':[90,100,110], 'learning_rate':[0.1,0.001,0.01], 'max_depth':[4,5,6],'colsample_bytree':[0.6,0.9,1]},
    {'n_estimoters':[100,110], 'learning_rate':[0.1,0.5,0.001], 'max_depth':[4,5,6],'colsample_bytree':[0.6,0.9,1],'colsample_bylevel':[0.6,0.7,0.9]}
]

#2 모델 구성

model = RandomizedSearchCV(XGBRegressor(eval_metric='mlogloss'), parameters, cv = KFold  ) 

score = cross_val_score(model, x_train,y_train,cv= KFold)


print(score)

et = datetime.datetime.now()

print(et-st)