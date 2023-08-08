import csv
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Create your views here.

def home(response):
	return render(response, "main/home.html", {})

def preprocess_data(df):
    # 1. Data Cleaning
    # Handle missing data (you can choose an appropriate imputation method):
    #df.fillna(df.mean(), inplace=True)

    # 2. Feature Selection/Extraction
    selected_features = df[["DATE", "PRICE (LOW)", "PRICE (HIGH)"]]

    # 3. Feature Scaling/Normalization
    # Scale the numerical features using StandardScaler:
    scaler = StandardScaler()
    selected_features = scaler.fit_transform(selected_features)

    # 4. Splitting the Data
    # Assuming you have a target variable 'target_column' in your DataFrame:
    target = df['target_column']
    X_train, X_test, y_train, y_test = train_test_split(selected_features, target, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test

def predict(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['upload']
            
            file = uploaded_file.read().decode('utf-8')
            csv_reader = csv.reader(file.splitlines(), delimiter=',')
            next(csv_reader)

            for row in csv_reader:
                 if len(row) >= 9:
                    time_variable = row[8].strip()
                    CropData.objects.create(
                        date=row[0],
                        commodity=row[1],
                        variety=row[2],
                        classification=row[3],
                        category=row[4],
                        high_price=row[5],
                        low_price=row[6],
                        yield_value=row[7],
                        time_variable=time_variable
                    )
                 else:
                    print("something wrong", row)
            return render(request, 'upload_success.html')
    else:
        form = UploadFileForm()
    return render(request, "main/predict.html", {'form': form})

def weather(response):
    return render(response,"main/weather.html",{})

def crops(response):
    return render(response,"main/crops.html",{})
            

def test(request):
	return render(request,'main/test.html')