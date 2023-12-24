# -*- coding: utf-8 -*-
"""v3_ARIMA_population_old.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17jZ490Ue8Ur8Go7rhO9zTYOFIBFt5gyX
"""

# Base Modules
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# ARIMA
from statsmodels.tsa.arima_model import ARIMA

# Error rate
from sklearn.metrics import mean_squared_error

# Additions
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

data = pd.read_csv('beipu.csv')

data.head()

df = data[['month', 'old']]

df.head()

df['month'] = pd.to_datetime(df['month'])

df.info()

df.head()

df.plot(x='month', y='old')
plt.show()

X_train = df[df['month'] < '2020-01-01']
X_valid = df[df['month'] >= '2020-01-01']

# X_train = df[df['month'] < '2021-07-01']
# X_valid = df[df['month'] >= '2019-01-01']

print("X_train Shape", X_train.shape)
print("X_valid Shape", X_valid.shape)

ori_X_train = X_train.copy()
X_train = X_train[['month', 'old']]
X_valid = X_valid[['month', 'old']]
X_valid.columns = ['month', 'val_old']
X_train.columns = ['month', 'train_old']

X_train.set_index('month', inplace=True)
X_valid.set_index('month', inplace=True)

index_60_months = pd.date_range(X_train.index[-1], freq='m', periods=84)

index_60_months

model_arima = ARIMA(X_train, order=(4,2,1))

model_arima_fit = model_arima.fit(disp=-1)

forecast = model_arima_fit.forecast(84)[0]

forecast = pd.Series(forecast, index=index_60_months)
forecast = forecast.rename("Forecast")

fig, ax = plt.subplots(figsize=(25,10))
chart = sns.lineplot(x='month', y='old', data=ori_X_train)

forecast.plot(ax=ax, color='red', marker='o', legend=True)
X_train.plot(ax=ax, color='blue', marker='o', legend=True)
X_valid.plot(ax=ax, color='orange', marker='o', legend=True)

# 設定字 及 字體大小
plt.title('Prediction Result', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('month', fontsize=20)
plt.ylabel('old', fontsize=20)

plt.show()

"""Result"""

def RMSE(y, y_pred):
    return mean_squared_error(y, y_pred)**0.5

print('Validation RMSE:', RMSE(X_valid['val_old'].values, forecast[:len(X_valid)].values))









df.shape

df_fcast = forecast.to_frame()

df_fcast.shape

df.head()

df.set_index("month", inplace=True)

df_fcast.head()

df_fcast.rename(columns=({"ARIMA":"total"}), inplace=True)

output_df = pd.DataFrame()

# output_df = pd.concat([df, df_fcast], axis=0)
output_df = pd.concat([df_fcast], axis=0)

output_df.head()

output_df.rename_axis("month", inplace=True)

output_df.tail()

output_df.info()

output_df

output_df.reset_index(inplace=True)

output_df.head()

output_df['month'] = output_df['month'].dt.strftime("%Y-%m")

output_df.set_index("month", inplace=True)

output_df.to_csv("beipu_84_total.csv")