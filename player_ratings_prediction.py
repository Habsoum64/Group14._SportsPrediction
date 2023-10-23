# -*- coding: utf-8 -*-
"""Player_Ratings_Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KTx67p7I0U_J58SYtiStWGOI4tDUcFC2
"""

import numpy as np
import pandas as pd

df = pd.read_csv('players_21.csv')

# Listing the columns with a high number of null values (over 30%)
column_names = list(df.columns.values)
nulls = []

for c in column_names:
    percentage_null = (df[c].isnull().sum() / len(df[c])) * 100

    if percentage_null >= 30.0:
        nulls.append(c)
        print(f"Null values in '{c}' column : {percentage_null:.2f}%")

# Dropping the columns with a lot of null values
data = df.drop(nulls, axis=1)

# Imputing & transforming the data

# ** Isolating numerical & categorical data
numerical = data.select_dtypes(exclude=['object'])
categorical = data.select_dtypes(include=['object'])

# ** Factorizing categorical values (turning them into numbers)
cat_columns = list(categorical.columns.values)
for col in cat_columns:
    categorical[col], b = pd.factorize(categorical[col])

# ** Filling blanks in the numerical columns (imputing)
numerical.fillna(numerical.mean(), inplace=True)

numerical.info()

categorical.info()

# Putting the new dataset together
categorical = categorical.reset_index(drop=True)
numerical = numerical.reset_index(drop=True)

data = pd.concat([categorical, numerical], axis=1)

# Picking the appropriate attributes for the model (1/2)
X = data.drop('overall', axis=1)
y = data['overall']

X.drop([
    'dob', 'short_name', 'long_name', 'club_name', 'club_joined', 'player_url',
    'player_face_url', 'club_logo_url', 'wage_eur', 'sofifa_id', 'international_reputation'
],
    axis=1, inplace=True)

# Importing the models
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.kernel_ridge import KernelRidge
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

# Fitting the models
lin_reg = LinearRegression()
lin_reg.fit(X, y)

rf_reg = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf_reg.fit(X, y)

kmn_reg = KernelRidge(kernel='rbf')
kmn_reg.fit(X, y)

xgb_reg = XGBRegressor(n_estimators=100, n_jobs=-1)
xgb_reg.fit(X, y)

gb_reg = GradientBoostingRegressor(n_estimators=100)
gb_reg.fit(X, y)

bagging_reg = BaggingRegressor(estimator=LinearRegression(), n_estimators=100, n_jobs=-1)
bagging_reg.fit(X, y)

# Feature importance for RFRegressor
feature_importances = rf_reg.feature_importances_
sorted_feature_importances = np.argsort(feature_importances)[::-1]

# Print the most important features
for i in sorted_feature_importances[:15]:
    print(X.columns[i])

# Feature importance for GBRegressor

feature_importances = gb_reg.feature_importances_
sorted_feature_importances = np.argsort(feature_importances)[::-1]

# Print the most important features
for i in sorted_feature_importances[:15]:
    print(X.columns[i])

# Feature importance for XGBRegressor
feature_importances = xgb_reg.feature_importances_
sorted_feature_importances = np.argsort(feature_importances)[::-1]

# Print the most important features
for i in sorted_feature_importances[:15]:
    print(X.columns[i])

# *** Identifying columns with high a correlation to the overall rating
corr_matrix = X.corrwith(y)
corr_matrix.sort_values(ascending=False)

low_corr = corr_matrix[abs(corr_matrix) < 0.5].index.tolist()
high_corr = []
for c in X.columns.values:
    if c not in low_corr:
        high_corr.append(c)

# Final selection of features for the prediction
pred_columns = [
    'potential', 'passing', 'dribbling', 'defending', 'physic',
    'movement_reactions', 'power_shot_power', 'mentality_composure',
    'value_eur', 'release_clause_eur'
]
X = data[pred_columns]

# Scaling the data
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X = scaler.fit_transform(X)

# Re-Fitting the models
lin_reg = LinearRegression()
lin_reg.fit(X, y)

rf_reg = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf_reg.fit(X, y)

kmn_reg = KernelRidge(kernel='rbf')
kmn_reg.fit(X, y)

xgb_reg = XGBRegressor(n_estimators=100, n_jobs=-1)
xgb_reg.fit(X, y)

gb_reg = GradientBoostingRegressor(n_estimators=100)
gb_reg.fit(X, y)

bagging_reg = BaggingRegressor(estimator=LinearRegression(), n_estimators=100, n_jobs=-1)
bagging_reg.fit(X, y)

# Importing metrics for evaluation
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Evaluating the accuracy of each model
print("Accuracy Scores for each model: \n")

y_pred = lin_reg.predict(X)
print(lin_reg.__class__.__name__ + ":")
print("Mean Absolute error: " + str(mean_absolute_error(y_pred, y)))
print("Mean squared error: " + str(mean_squared_error(y_pred, y)))
print("R-squared Test: " + str(r2_score(y_pred, y)) + '\n')

y_pred = rf_reg.predict(X)
print(rf_reg.__class__.__name__ + ":")
print("Mean Absolute error: " + str(mean_absolute_error(y_pred, y)))
print("Mean squared error: " + str(mean_squared_error(y_pred, y)))
print(rf_reg.__class__.__name__ + ": " + str(r2_score(y_pred, y)) + '\n')

y_pred = kmn_reg.predict(X)
print(kmn_reg.__class__.__name__ + ":")
print("Mean Absolute error: " + str(mean_absolute_error(y_pred, y)))
print("Mean squared error: " + str(mean_squared_error(y_pred, y)))
print("R-squared Test: " + str(r2_score(y_pred, y)))

y_pred = xgb_reg.predict(X)
print(xgb_reg.__class__.__name__ + ":")
print("Mean Absolute error: " + str(mean_absolute_error(y_pred, y)))
print("Mean squared error: " + str(mean_squared_error(y_pred, y)))
print("R-squared Test: " + str(r2_score(y_pred, y)) + '\n')

y_pred = gb_reg.predict(X)
print(gb_reg.__class__.__name__ + ":")
print("Mean Absolute error: " + str(mean_absolute_error(y_pred, y)))
print("Mean squared error: " + str(mean_squared_error(y_pred, y)))
print("R-squared Test: " + str(r2_score(y_pred, y)) + '\n')

y_pred = bagging_reg.predict(X)
print(bagging_reg.__class__.__name__ + ":")
print("Mean Absolute error: " + str(mean_absolute_error(y_pred, y)))
print("Mean squared error: " + str(mean_squared_error(y_pred, y)))
print("R-squared Test: " + str(r2_score(y_pred, y)) + '\n')

# Looking for the best number of estimators for the prefered models (RandomForest, GradientBoosting, and XGB regressors)
best_n_rf = 0
best_n_gb = 0
best_n_xgb = 0

best_score1 = 0
best_score2 = 0
best_score3 = 0

# *** For RandomForest ***
for n1 in range(150, 180):
    rf = RandomForestRegressor(n_estimators=n1, random_state=42, n_jobs=-1)
    rf.fit(X, y)
    pred = rf.predict(X)
    score = r2_score(pred, y)

    if score > best_score1:
        best_score1 = score
        best_n_rf = n1

print("Best n_estimator for RFRegressor: " + str(best_n_rf))
print("Score: " + str(best_score1) + "\n")

# *** For GradientBoosting ***
for n2 in range(150, 180):
    gb = GradientBoostingRegressor(n_estimators=n2)

    gb.fit(X, y)
    pred = gb.predict(X)
    score = r2_score(pred, y)

    if score > best_score2:
        best_score2 = score
        best_n_gb = n2

print("Best n_estimator for GBRegressor: " + str(best_n_gb))
print("Score: " + str(best_score2) + "\n")

# *** For XGB ***
for n3 in range(150, 180):
    xgb = XGBRegressor(n_estimators=n3, n_jobs=-1)

    xgb.fit(X, y)
    pred = xgb.predict(X)
    score = r2_score(pred, y)

    if score > best_score3:
        best_score3 = score
        best_n_xgb = n3

print("Best n_estimator for XGBRegressor: " + str(best_n_xgb))
print("Score: " + str(best_score3) + "\n")

# Cross validation Training - RandomForest model
from sklearn.model_selection import KFold

kfold = KFold(n_splits=5, shuffle=True)
rf_reg = RandomForestRegressor(n_estimators=best_n_rf, random_state=42, n_jobs=-1)
rf_mae_scores = []
rf_r2_scores = []

for train_index, test_index in kfold.split(X):
    Xtrain, Xtest = X[train_index], X[test_index]
    ytrain, ytest = y[train_index], y[test_index]

    rf_reg.fit(Xtrain, ytrain)
    y_pred = rf_reg.predict(Xtest)

    mae_scor = mean_absolute_error(y_pred, ytest)
    r2_scor = r2_score(y_pred, ytest)

    rf_mae_scores.append(mae_scor)
    rf_r2_scores.append(r2_scor)

avg_mae = np.mean(rf_mae_scores)
avg_r2 = np.mean(rf_r2_scores)

print('Average Cross Validation scores:')
print("MAE: " + str(avg_mae))
print("R2: " + str(avg_r2))

# Cross validation testing - Voting Regressor Model
from sklearn.ensemble import VotingRegressor

models = [
    ('rf', RandomForestRegressor(n_estimators=best_n_rf, random_state=42)),
    ('xgb', XGBRegressor(n_estimators=best_n_xgb)),
    ('gbr', GradientBoostingRegressor(n_estimators=best_n_gb))
]

voting_reg = VotingRegressor(estimators=models, n_jobs=-1)
voting_mae_scores = []
voting_r2_scores = []

for train_index, test_index in kfold.split(X):
    Xtrain, Xtest = X[train_index], X[test_index]
    ytrain, ytest = y[train_index], y[test_index]

    voting_reg.fit(Xtrain, ytrain)
    y_pred = voting_reg.predict(Xtest)

    mae_scor = mean_absolute_error(y_pred, ytest)
    r2_scor = r2_score(y_pred, ytest)

    voting_mae_scores.append(mae_scor)
    voting_r2_scores.append(r2_scor)

avg_mae = np.mean(voting_mae_scores)
avg_r2 = np.mean(voting_r2_scores)

print('Average Cross Validation scores:')
print("MAE: " + str(avg_mae))
print("R2: " + str(avg_r2))

# Loading and treating the FIFA22 dataset
df2 = pd.read_csv('/content/drive/My Drive/Intro to AI/Midsem Project/players_22.csv')

# Data Selection
data2 = df2[pred_columns]
num = data2.select_dtypes(exclude=['object'])
cat = data2.select_dtypes(include=['object'])

# Data processing
cat_cols = list(cat.columns.values)
for col in cat_cols:
    cat[col], b = pd.factorize(cat[col])

num.fillna(num.mean(), inplace=True)

# New dataset
cat = cat.reset_index(drop=True)
num = num.reset_index(drop=True)
data2 = pd.concat([cat, num], axis=1)

# Prediction variables
X = scaler.fit_transform(data2)
y = df2['overall']

# Accuracy of the model on the FIFA22 dataset
print("Accuracy Scores for the Random Forest model on the FIFA 22 dataset: ")
y_pred = rf_reg.predict(X)
print("R-squared test: " + str(r2_score(y_pred, y)))
print("Mean Absolute Error: " + str(mean_absolute_error(y_pred, y)))

# Accuracy of the model on the FIFA22 dataset
print("Accuracy Scores for the Voting Regressor model on the FIFA 22 dataset: ")
y_pred = voting_reg.predict(X)
print("R-squared test: " + ": " + str(r2_score(y_pred, y)))
print("Mean Absolute Error: " + ": " + str(mean_absolute_error(y_pred, y)))

# Saving the model & scaler in files (for later use)
import pickle

with open('rf_reg.pkl', 'wb') as f:
    pickle.dump(rf_reg, f)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
