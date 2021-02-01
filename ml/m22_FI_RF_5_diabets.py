from sys import platform
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier,RandomForestRegressor
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#1

datasets = load_diabetes()

x_train, x_test, y_train,y_test = train_test_split(datasets.data, datasets.target, train_size = 0.8 , random_state = 104 )


#2

model  = RandomForestRegressor(max_depth=4)

#3

model.fit(x_train,y_train)

#4

acc = model.score(x_test,y_test)

print(model.feature_importances_)
print('r2 : ',acc)

def plot_feature_importances_dataset(model):
    n_features = datasets.data.shape[1]
    plt.barh(np.arange(n_features),model.feature_importances_,
            align='center')
    plt.yticks(np.arange(n_features),datasets.feature_names)
    plt.xlabel("Feature Importances")
    plt.ylim(-1, n_features)

plot_feature_importances_dataset(model)
plt.show()

# [0.02923558 0.00256604 0.40354239 0.0763502  0.02725245 0.03312221
#  0.02856914 0.01260643 0.34261698 0.04413856]
# r2 :  0.529216012903976