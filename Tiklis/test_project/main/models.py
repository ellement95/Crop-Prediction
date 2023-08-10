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