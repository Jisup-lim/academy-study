from sys import platform
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np

#1

datasets = load_boston()

x_train, x_test, y_train,y_test = train_test_split(datasets.data, datasets.target, train_size = 0.8 , random_state = 104 )


#2

model  = DecisionTreeRegressor(max_depth=4)

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

# [0.04870916 0.         0.         0.         0.04215833 0.29299352
#  0.         0.01155186 0.         0.         0.00262558 0.0103936
#  0.59156795]
# r2 :  0.7826092386908275