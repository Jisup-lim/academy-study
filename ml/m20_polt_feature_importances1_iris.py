from sys import platform
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np

#1

datasets = load_iris()
x_train, x_test, y_train,y_test = train_test_split(datasets.data, datasets.target, train_size = 0.8 , random_state = 104 )


#2

model  = DecisionTreeClassifier(max_depth=4)

#3

model.fit(x_train,y_train)

#4

acc = model.score(x_test,y_test)

print(model.feature_importances_)
print('acc : ',acc)

def plot_feature_importances_dataset(model):
    n_features = datasets.data.shape[1]
    plt.barh(np.arange(n_features),model.feature_importances_,
            align='center')
    plt.yticks(np.arange(n_features),datasets.feature_names)
    plt.xlabel("Feature Importances")
    plt.ylim(-1, n_features)

plot_feature_importances_dataset(model)
plt.show()

# [0.01699235 0.         0.04451513 0.93849252]
# 1.0