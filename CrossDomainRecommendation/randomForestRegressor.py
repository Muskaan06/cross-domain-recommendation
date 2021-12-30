from sklearn.model_selection import cross_val_score,train_test_split
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# quietly deep-reload tqdm

df = pd.read_csv("merged_file.csv")

y = df.rating
X = df.drop("rating",axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2)
# print("\nX_train:\n")
# print(X_train.head())
# print(X_train.shape)
#
# print("\nX_test:\n")
# print(X_test.head())
# print(X_test.shape)

#check for any null values
X_test[X_test.isnull().any(axis=1)]

# #remove null values
# X_train = X_train.dropna()

# # To reset the indices
# X_train = X_train.reset_index(drop = True)

# #remove null values
# X_test = X_test.dropna()

# # To reset the indices
# X_test = X_test.reset_index(drop = True)

# create regressor object
regressor = RandomForestRegressor(max_features='sqrt', n_estimators=20, oob_score=True, verbose=2,random_state=10)

# fit the regressor with x and y data
regressor.fit(X_train, y_train)

Y_pred = regressor.predict(X_test)

# Calculate the absolute errors
errors = abs(Y_pred - y_test)
# Print out the mean absolute error (mae)
print('Mean Absolute Error:', round(np.mean(errors), 2), 'degrees.')

# Calculate mean absolute percentage error (MAPE)
mape = 100 * (errors / y_test.shape[0])
# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')


