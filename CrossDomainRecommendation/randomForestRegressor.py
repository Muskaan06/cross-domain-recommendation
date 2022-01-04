from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV,RandomizedSearchCV
from pprint import pprint
from sklearn.metrics import accuracy_score,mean_squared_error,mean_absolute_error


df = pd.read_csv("merged_file.csv")

y = df.rating
X = df.drop("rating",axis=1)

#splitting dataset
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2)
print("-----train shape-----")
print(X_train.shape)
print(y_train.shape)
print("-----test shape-----")
print(X_test.shape)
print(y_test.shape)

#hyperparameter tuning through cross validation
# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 200, num = 5)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]
# Method of selecting samples for training each tree
bootstrap = [True, False]
# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}
pprint(random_grid)

#model training with evaluation
#random search CV
rf = RandomForestRegressor(verbose=10)
rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 3, cv = 3, verbose=10, random_state=42, n_jobs = -1,scoring='neg_root_mean_squared_error')
rf_random.fit(X_train, y_train)
print(rf_random.best_params_)

#grid search CV


#test evaluation
y_pred = rf_random.predict(X_test)
print("mean squared error: ",mean_squared_error(y_train,y_pred))












