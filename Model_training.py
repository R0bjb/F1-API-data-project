import numpy as np
import pandas
import xgboost as xgb
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor


def define_x_y(dataset):
    X = dataset.drop(columns='lap_duration')
    Y = dataset['lap_duration']
    return X,Y

def test_train_split(X,Y):
    X_train,X_test,Y_train,Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=42)
    return X_train, X_test, Y_train, Y_test
parameters = {}
def build_model(X_train, Y_train, X_test):
    model = XGBRegressor()

    model.fit(X_train, Y_train)
    y_pred = model.predict(X_test)
    return y_pred
