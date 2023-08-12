from django.db import models

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
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

class CropPricePrediction(models.Model):
    def convert_date_and_time(df):
        # Convert 'DATE' column to datetime
        df['DATE'] = pd.to_datetime(df['DATE'])

        # Extract date features
        df['YEAR'] = df['DATE'].dt.year
        df['MONTH'] = df['DATE'].dt.month
        df['DAY'] = df['DATE'].dt.day

        # Drop the original 'DATE' column if not needed
        df.drop('DATE', axis=1, inplace=True)

        # Convert 'TIME' column to time
        df['TIME'] = pd.to_datetime(df['TIME']).dt.time

        # Extract time features
        df['HOUR'] = df['TIME'].apply(lambda x: x.hour)
        df['MINUTE'] = df['TIME'].apply(lambda x: x.minute)
        df['SECOND'] = df['TIME'].apply(lambda x: x.second)

        # Drop the original 'TIME' column if not needed
        df.drop('TIME', axis=1, inplace=True)

        return df
    
    @staticmethod
    def prediction_model(row):
        # Convert the list into a DataFrame
        column_names = ['DATE', 'COMMODITY', 'VARIETY', 'CLASSIFICATION', 'CATEGORY', 'MIN PRICE', 'MAX PRICE', 'TIME']
        data = [row]
        df = pd.DataFrame(data, columns=column_names)
        
        # Apply the convert_date_and_time function
        df = CropPricePrediction.convert_date_and_time(df)

        # Prepare data
        X = df.drop(['MIN PRICE', 'MAX PRICE'], axis=1)  # Features
        y_min = df['MIN PRICE']  # Target variable: MIN PRICE
        y_max = df['MAX PRICE']  # Target variable: MAX PRICE

        # Convert categorical columns to numerical using Label Encoding
        label_encoders = {}
        for col in ['COMMODITY', 'VARIETY', 'CLASSIFICATION', 'CATEGORY']:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            label_encoders[col] = le

        # Create Random Forest Regressor models for MIN PRICE and MAX PRICE
        rf_min = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_min.fit(X, y_min)

        rf_max = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_max.fit(X, y_max)
        
        return rf_min, rf_max
        
    def predict_price(label_encoders, rf_min, rf_max, user_input):
        # Get user inputs
        date = input("Enter date (YYYY-MM-DD): ")
        commodity = input("Enter commodity: ")
        variety = input("Enter variety: ")
        classification = input("Enter classification: ")
        category = input("Enter category: ")
        time = input("Enter time: ")

        # Preprocess user inputs
        user_input = pd.DataFrame({
            'DATE': [date],
            'COMMODITY': [label_encoders['COMMODITY'].transform([commodity])[0]],
            'VARIETY': [label_encoders['VARIETY'].transform([variety])[0]],
            'CLASSIFICATION': [label_encoders['CLASSIFICATION'].transform([classification])[0]],
            'CATEGORY': [label_encoders['CATEGORY'].transform([category])[0]],
            'TIME': [time]
        })

        # Convert 'DATE' column to datetime
        user_input['DATE'] = pd.to_datetime(user_input['DATE'])

        # Extract date features
        user_input['YEAR'] = user_input['DATE'].dt.year
        user_input['MONTH'] = user_input['DATE'].dt.month
        user_input['DAY'] = user_input['DATE'].dt.day

        # Drop the original 'DATE' column if not needed
        user_input.drop('DATE', axis=1, inplace=True)

        # Convert 'TIME' column to time
        user_input['TIME'] = pd.to_datetime(user_input['TIME']).dt.time

        # Extract time features
        user_input['HOUR'] = user_input['TIME'].apply(lambda x: x.hour)
        user_input['MINUTE'] = user_input['TIME'].apply(lambda x: x.minute)
        user_input['SECOND'] = user_input['TIME'].apply(lambda x: x.second)

        # Drop the original 'TIME' column if not needed
        user_input.drop('TIME', axis=1, inplace=True)

        # Make predictions for MIN PRICE and MAX PRICE
        predicted_min_price = rf_min.predict(user_input)
        predicted_max_price = rf_max.predict(user_input)

        # Print descriptive output
        print("\nCrop Price Predicted for:")
        print(f"Commodity: {commodity}")
        print(f"Variety: {variety}")
        print(f"Classification: {classification}")
        print(f"Category: {category}")
        print(f"Date: {date}")
        print(f"Time: {time}")

        print("\nPredicted Prices:")
        print(f"Predicted MIN PRICE: {predicted_min_price[0]}")
        print(f"Predicted MAX PRICE: {predicted_max_price[0]}")
        
        return predicted_min_price, predicted_max_price