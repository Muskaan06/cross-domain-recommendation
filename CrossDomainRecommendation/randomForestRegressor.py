from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error
import pickle

df = pd.read_csv("merged_file.csv")

y = df.rating
X = df.drop("rating", axis=1)

# splitting dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
print("-----train shape-----")
print(X_train.shape)
print(y_train.shape)
print("-----test shape-----")
print(X_test.shape)
print(y_test.shape)

# hyperparameter tuning through cross validation
# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start=100, stop=200, num=5)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 110, num=11)]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]
# Method of selecting samples for training each tree
bootstrap = [True, False]
# Create the random grid
random_grid = {'n_estimators': 100,
               'max_features': 'sqrt',
               'max_depth': 10,
               'min_samples_split': 5,
               'min_samples_leaf': 1,
               'bootstrap': True}
print(random_grid)

# model training with evaluation
# random search CV
rf = RandomForestRegressor(verbose=10, n_estimators=100, max_features='sqrt', max_depth=10, min_samples_split=5, min_samples_leaf=1, bootstrap=True)
# rf_random = RandomizedSearchCV(estimator=rf, param_distributions=random_grid, n_iter=1, cv=3, verbose=10,
#                                random_state=42, n_jobs=-1, scoring='neg_root_mean_squared_error')
rf.fit(X_train, y_train)
print(rf.score(X_train, y_train))
# print(rf_random.best_params_)

# grid search CV


# save model
filename = 'finalized_model.sav'
pickle.dump(rf, open(filename, 'wb'))

# test evaluation
y_pred = rf.predict(X_test)
print("mean squared error: ", mean_squared_error(y_test, y_pred))
