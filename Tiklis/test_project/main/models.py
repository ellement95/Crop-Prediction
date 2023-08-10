from django.db import models

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
from datetime import datetime 

# Create your models here.

class File(models.Model):
    file = models.FileField(upload_to='files/')

class CropData(models.Model):
    date = models.DateField()
    commodity = models.CharField(max_length=100, default='Unknown')
    variety = models.CharField(max_length=100)
    classification = models.CharField(max_length=100, default='Crop')
    category = models.CharField(max_length=100, default='Default Category')
    high_price = models.FloatField()
    low_price = models.FloatField()
    time_variable = models.TimeField()
    
    def __str__(self):
        return f"{self.date} - {self.commodity} - {self.variety}"

# class CropPricePrediction(models.Model):
#     @staticmethod
#     def preprocess_data(df):
#         # converting date and time
#         df['DATE'] = pd.to_datetime(df['DATE'])
#         df['TIME'] = pd.to_datetime(df['TIME']).dt.time
        
#         # Extract relevant features from the timestamp columns
#         df['YEAR'] = df['date'].dt.year
#         df['MONTH'] = df['date'].dt.month
#         df['DAY'] = df['date'].dt.day
#         df['HOUR'] = df['time_variable'].apply(lambda x: x.hour)
#         df['MINUTE'] = df['time_variable'].apply(lambda x: x.minute)
#         df['SECOND'] = df['time_variable'].apply(lambda x: x.second)

#         # Select categorical columns for one-hot encoding
#         categorical_columns = ['commodity', 'classification', 'category']

#         # Apply one-hot encoding to categorical columns
#         encoder = OneHotEncoder(drop='first', sparse=False)
#         encoded_categorical = encoder.fit_transform(df[categorical_columns])

#         # Create a DataFrame for encoded categorical features
#         encoded_df = pd.DataFrame(encoded_categorical, columns=encoder.get_feature_names_out(input_features=categorical_columns))

#         # Combine encoded categorical features with numerical features
#         X = pd.concat([df[['YEAR', 'MONTH', 'DAY',  'HOUR', 'MINUTE', 'SECOND']], encoded_df], axis=1)

#         y_min = df['MIN PRICE']  # Target: Minimum Price
#         y_max = df['MAX PRICE']  # Target: Maximum Price

#         # Split the data into training and testing sets
#         X_train, X_test, y_min_train, y_min_test, y_max_train, y_max_test = train_test_split(X, y_min, y_max, test_size=0.2, random_state=42)

#         return X_train, X_test, y_min_train, y_min_test, y_max_train, y_max_test
    
#     @staticmethod
#     def train_and_predict(X_train, X_test, y_min_train, y_min_test, y_max_train, y_max_test):
#         # Initialize StandardScaler
#         scaler = StandardScaler()

#         # Fit scaler on training data and transform all the splits
#         X_train_scaled = scaler.fit_transform(X_train)
#         X_test_scaled = scaler.transform(X_test)

#         # Initialize RandomForestRegressor models for minimum and maximum prices
#         model_min = RandomForestRegressor(random_state=42)
#         model_max = RandomForestRegressor(random_state=42)

#         # Train the models
#         model_min.fit(X_train_scaled, y_min_train)
#         model_max.fit(X_train_scaled, y_max_train)

#         # Make predictions
#         y_min_pred = model_min.predict(X_test_scaled)
#         y_max_pred = model_max.predict(X_test_scaled)

#         # Evaluate the models using Mean Squared Error
#         mse_min = mean_squared_error(y_test, y_min_pred)
#         mse_max = mean_squared_error(y_test, y_max_pred)

#         return mse_min, mse_max
    
#     @staticmethod
#     def get_user_input_data(user_input):
#         try:
#             date = datetime.strptime(user_input['date'], '%m/%d/%Y').date()
#         except ValueError:
#             raise ValueError("Invalid date format")
        
#         commodity = user_input['commodity']
#         classification = user_input['classification']
#         category = user_input['category']
#         time_variable = user_input['time_variable']
        
#         return {
#             'date': date,
#             'commodity': commodity,
#             'classification': classification,
#             'category': category,
#             'time_variable': time_variable
#         }