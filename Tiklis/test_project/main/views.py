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
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file to the database using the File model
            file = form.cleaned_data['file']
            obj = File.objects.create(file=file)
            # Additional processing or computations can be performed here
            # For example, you can pass the 'obj' or its ID to the template
            # to display or manipulate it as needed
            
            # Read the data from the file into a DataFrame
            df = pd.read_csv(file)

            # Data preprocessing
            X_train, X_test, y_train, y_test = preprocess_data(df)
            
            # Perform regression analysis here
            # Train the regression model and make predictions
            
            return render(request, "main/prediction_result.html", {'file_obj': obj})
    else:
        form = FileUploadForm()

    return render(request, "main/predict.html", {'form': form})

def weather(response):
    return render(response,"main/weather.html",{})

def crops(response):
    return render(response,"main/crops.html",{})
            
def create(response):
	if response.method == "POST":
		form = CreateNewList(response.POST)

		if form.is_valid():
			n = form.cleaned_data["name"]
			t = ToDoList(name=n)
			t.save()

		return HttpResponseRedirect("/%i" %t.id)
	else:
		form = CreateNewList()
	return render(response, "main/create.html", {"form":form})

def test(request):
	return render(request,'main/test.html')